from typing import Dict
from desk.types import NetworkOption, ChainOption


BROKER = "DESK-SDK"

BASE_URLS: Dict[NetworkOption, str] = {
    "mainnet": "https://api.happytrading.global",
    "mainnetBase": "https://api.happytrading.global",
    "mainnetArbitrum": "https://api.happytrading.global",
    "mainnetBsc": "https://api.happytrading.global",
    "base": "https://api.happytrading.global",
    "arbitrum": "https://api.happytrading.global",
    "bsc": "https://api.happytrading.global",
}

CRM_URLS: Dict[NetworkOption, str] = {
    "mainnet": "https://api.desk.exchange",
    "mainnetBase": "https://api.desk.exchange",
    "mainnetArbitrum": "https://api.desk.exchange",
    "mainnetBsc": "https://api.desk.exchange",
    "base": "https://api.desk.exchange",
    "arbitrum": "https://api.desk.exchange",
    "bsc": "https://api.desk.exchange",
}

WSS_URLS: Dict[NetworkOption, str] = {
    "mainnet": "wss://ws-api.happytrading.global/ws",
    "mainnetBase": "wss://ws-api.happytrading.global/ws",
    "mainnetArbitrum": "wss://ws-api.happytrading.global/ws",
    "mainnetBsc": "wss://ws-api.happytrading.global/ws",
    "base": "wss://ws-api.happytrading.global/ws",
    "arbitrum": "wss://ws-api.happytrading.global/ws",
    "bsc": "wss://ws-api.happytrading.global/ws",
}

CHAIN_ID: Dict[NetworkOption | ChainOption, int] = {
    "mainnet": 8453,
    "mainnetBase": 8453,
    "mainnetArbitrum": 42161,
    "mainnetBsc": 56,
    "base": 8453,
    "arbitrum": 42161,
    "bsc": 56,
}
