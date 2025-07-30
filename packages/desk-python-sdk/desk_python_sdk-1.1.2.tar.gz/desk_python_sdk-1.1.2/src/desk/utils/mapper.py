from web3 import Web3
from desk.constant.contract import CONTRACT_ADDRESS


def get_contract_address(chain_id: int):
    return CONTRACT_ADDRESS[int(chain_id)]


def map_token_profile(data: dict, chain_id: int):
    token_profile = {}
    for asset in data:
        # skip 'CREDIT'
        if asset["asset"] == "CREDIT":
            continue

        each_asset = {
            "asset": asset["asset"],
            "collateral_id": asset["collateral_id"],
            "decimals": asset["decimals"],
            "collat_factor_bps": asset["collat_factor_bps"],
            "borrow_factor_bps": asset["borrow_factor_bps"],
            "price_feed_id": asset["price_feed_id"],
            "discount_rate_bps": asset["discount_rate_bps"],
            "withdrawal_base_fee": asset["withdrawal_base_fee"],
            "priority": asset["priority"]
        }

        address_found = False
        for token in asset["token_addresses"]:
            if int(token["chain_id"]) == int(chain_id):
                each_asset["address"] = token["address"]
                address_found = True
                break

        if address_found:
            # via token name
            token_profile[asset["asset"]] = each_asset
            token_profile[asset["asset"].lower()] = each_asset
            # via token address
            token_profile[each_asset["address"]] = each_asset
            token_profile[each_asset["address"].lower()] = each_asset
            token_profile[Web3.to_checksum_address(
                each_asset["address"])] = each_asset
    return token_profile
