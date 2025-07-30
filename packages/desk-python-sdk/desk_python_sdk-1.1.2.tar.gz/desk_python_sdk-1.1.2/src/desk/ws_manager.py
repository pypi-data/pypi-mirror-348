from collections import defaultdict
import json
import logging
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple
from websocket import WebSocketApp
import threading

from desk.types import Subscription, WsMessage

ActiveSubscription = NamedTuple("ActiveSubscription", [(
    "callback", Callable[[Any], None]), ("subscription_id", int)])


class WebSocketManager(threading.Thread):
    def __init__(self, ws_url: str):
        super().__init__()
        self.subscription_id_counter = 0
        self.ws_ready = False
        self.url = ws_url
        self.ws: Optional[WebSocketApp] = None

        self.managed_subscriptions: List[Tuple[Subscription, Callable[[
            Any], None], int]] = []

        self.active_subscriptions: Dict[str,
                                        List[ActiveSubscription]] = defaultdict(list)

        self.ping_sender = threading.Thread(target=self.send_ping)
        self.stop_event = threading.Event()
        self.reconnect_delay = 5

    def run(self):
        while not self.stop_event.is_set():
            logging.info(
                f"WebSocketManager: Initializing WebSocketApp for {self.url}")
            self.ws = WebSocketApp(
                self.url,
                on_message=self.on_message,
                on_open=self.on_open,
                on_close=self.on_close,
                on_error=self.on_error
            )
            try:
                self.ws.run_forever(
                    suppress_origin=True, reconnect=1, ping_interval=20, ping_timeout=10)
            except Exception as e:
                logging.error(f"WebSocketManager: run_forever crashed: {e}")

            if self.stop_event.is_set():
                logging.info(
                    "WebSocketManager: Stop event set, exiting run loop.")
                break

            logging.info(
                f"WebSocketManager: run_forever exited. Will attempt to reconnect after {self.reconnect_delay} seconds.")
            stopped_during_wait = self.stop_event.wait(self.reconnect_delay)
            if stopped_during_wait:
                logging.info(
                    "WebSocketManager: Stop event set during reconnect wait, exiting run loop.")
                break

    def send_ping(self):
        while not self.stop_event.wait(50):
            if not (self.ws and self.ws.sock and self.ws.sock.connected):
                logging.debug("Websocket not connected, skipping ping.")
                continue
            if not self.ws_ready:
                logging.debug(
                    "Websocket connected but not ready (on_open not called/completed), skipping ping.")
                continue

            try:
                self.ws.send(json.dumps({"method": "ping"}))
            except Exception as e:
                logging.error(f"Error sending ping: {e}")

    def stop(self):
        logging.info("WebSocketManager: Stopping...")
        self.stop_event.set()
        if self.ws:
            self.ws.close()
        if self.ping_sender.is_alive():
            self.ping_sender.join()
        logging.info("WebSocketManager: Stopped.")

    def on_message(self, _ws, message):
        if message == "Websocket connection established.":
            logging.debug(f"Received: {message}")
            return

        try:
            ws_msg = json.loads(message)
        except json.JSONDecodeError:
            logging.error(
                f"Failed to decode JSON from WebSocket message: {message}")
            return

        if isinstance(ws_msg, dict) and 'error' in ws_msg:
            logging.error(
                f"Received error message from WebSocket: {ws_msg.get('error')}. Closing current connection to trigger reconnect.")
            if self.ws:
                self.ws.close()
            return

        if not isinstance(ws_msg, dict) or 'type' not in ws_msg:
            logging.warning(
                f"Received WebSocket message without 'type' field or not a dict: {message}")
            return

        identifier = ws_msg['type']
        if identifier is None:
            logging.debug(
                "Websocket not handling empty message (identifier is None)")
            return

        active_callbacks = self.active_subscriptions.get(identifier, [])
        if not active_callbacks:
            logging.warning(
                f"Websocket message from an unexpected or unsubscribed subscription: type='{identifier}', message='{message}'")
        else:
            for active_subscription_details in active_callbacks:
                try:
                    active_subscription_details.callback(ws_msg)
                except Exception as e:
                    logging.error(
                        f"Error in subscription callback for type '{identifier}', id {active_subscription_details.subscription_id}: {e}", exc_info=True)

    def on_open(self, _wsapp):
        logging.info("WebSocketManager: Connection opened.")
        self.ws_ready = True
        self.active_subscriptions.clear()

        for sub_dict, callback_fn, sub_id in list(self.managed_subscriptions):
            logging.info(
                f"WebSocketManager: Re-activating subscription for type '{sub_dict['type']}' with ID {sub_id}")
            identifier = sub_dict['type']

            current_subs_for_id = [
                active_sub for active_sub in self.active_subscriptions.get(identifier, []) if active_sub.subscription_id != sub_id
            ]
            current_subs_for_id.append(ActiveSubscription(callback_fn, sub_id))
            self.active_subscriptions[identifier] = current_subs_for_id

            try:
                if self.ws:
                    self.ws.send(json.dumps(
                        {"method": "subscribe", "subscription": sub_dict}))
                else:
                    logging.error(
                        "self.ws is None in on_open during resubscribe attempt")
            except Exception as e:
                logging.error(
                    f"Error sending subscribe message for type '{identifier}' ID {sub_id} during on_open: {e}")
                self.active_subscriptions[identifier] = [
                    active_sub for active_sub in self.active_subscriptions.get(identifier, []) if active_sub.subscription_id != sub_id
                ]
                if not self.active_subscriptions[identifier]:
                    del self.active_subscriptions[identifier]

    def on_close(self, _ws, close_status_code, close_msg):
        logging.info(
            f"WebSocket closed with status {close_status_code}: {close_msg}")
        self.ws_ready = False

    def on_error(self, _ws, error):
        logging.error(f"WebSocket error: {error}")

    def subscribe(
        self, subscription: Subscription, callback: Callable[[Any], None], subscription_id: Optional[int] = None
    ) -> int:
        if subscription_id is None:
            self.subscription_id_counter += 1
            subscription_id = self.subscription_id_counter

        self.managed_subscriptions = [
            s for s in self.managed_subscriptions if s[2] != subscription_id
        ]
        self.managed_subscriptions.append(
            (subscription, callback, subscription_id))
        logging.info(
            f"Subscription for type '{subscription['type']}' ID {subscription_id} added to managed list.")

        if self.ws_ready and self.ws and self.ws.sock and self.ws.sock.connected:
            logging.debug(
                f"Attempting to immediately activate subscription for '{subscription['type']}' ID {subscription_id}")
            identifier = subscription['type']

            current_subs_for_id = [
                active_sub for active_sub in self.active_subscriptions.get(identifier, []) if active_sub.subscription_id != subscription_id
            ]
            current_subs_for_id.append(
                ActiveSubscription(callback, subscription_id))
            self.active_subscriptions[identifier] = current_subs_for_id

            try:
                self.ws.send(json.dumps(
                    {"method": "subscribe", "subscription": subscription}))
                logging.debug(
                    f"Sent subscribe for '{subscription['type']}' ID {subscription_id}")
            except Exception as e:
                logging.error(
                    f"Error sending subscribe message for '{subscription['type']}' ID {subscription_id}: {e}")
                self.active_subscriptions[identifier] = [
                    active_sub for active_sub in self.active_subscriptions.get(identifier, []) if active_sub.subscription_id != subscription_id
                ]
                if not self.active_subscriptions[identifier]:
                    del self.active_subscriptions[identifier]
        else:
            logging.info(
                f"WebSocket not ready. Subscription for '{subscription['type']}' ID {subscription_id} will be activated on next connection.")
        return subscription_id

    def unsubscribe(self, subscription: Subscription, subscription_id: int) -> bool:
        logging.info(
            f"Attempting to unsubscribe from type '{subscription['type']}' ID {subscription_id}.")

        initial_managed_len = len(self.managed_subscriptions)
        self.managed_subscriptions = [
            s for s in self.managed_subscriptions if s[2] != subscription_id
        ]
        removed_from_managed = len(
            self.managed_subscriptions) != initial_managed_len
        if removed_from_managed:
            logging.debug(
                f"Removed subscription ID {subscription_id} from managed list.")
        else:
            logging.debug(
                f"Subscription ID {subscription_id} not found in managed list.")

        if self.ws_ready and self.ws and self.ws.sock and self.ws.sock.connected:
            identifier = subscription['type']
            active_subs_for_identifier = self.active_subscriptions.get(
                identifier, [])

            new_active_subs_for_identifier = [
                x for x in active_subs_for_identifier if x.subscription_id != subscription_id
            ]

            if len(new_active_subs_for_identifier) != len(active_subs_for_identifier):
                logging.debug(
                    f"Deactivating subscription ID {subscription_id} for type '{identifier}'.")
                if not new_active_subs_for_identifier:
                    del self.active_subscriptions[identifier]
                    logging.debug(
                        f"No more active subscriptions for type '{identifier}'.")
                else:
                    self.active_subscriptions[identifier] = new_active_subs_for_identifier

                try:
                    self.ws.send(json.dumps(
                        {"method": "unsubscribe", "subscription": subscription}))
                    logging.debug(
                        f"Sent unsubscribe for '{subscription['type']}' ID {subscription_id}")
                    return True
                except Exception as e:
                    logging.error(
                        f"Error sending unsubscribe message for '{subscription['type']}' ID {subscription_id}: {e}")
                    return False
            else:
                logging.debug(
                    f"Subscription ID {subscription_id} for type '{identifier}' was not active on current WebSocket.")
                return removed_from_managed

        logging.info(
            f"WebSocket not ready. Unsubscribe for '{subscription['type']}' ID {subscription_id} processed for managed list only.")
        return removed_from_managed
