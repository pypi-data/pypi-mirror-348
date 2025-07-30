import uuid
from dataclasses import asdict
from typing import AsyncGenerator

from pulsar_sdk_py.enums import TierKeys, ChainKeys
from pulsar_sdk_py.websocket.base import WebSocketClient
from pulsar_sdk_py.websocket.websocket_types import (
    BalancesMessage,
    TimeseriesData,
    TimeseriesMessage,
    WalletBalancesData,
)
from pulsar_sdk_py.dataclasses.schemas import (
    Timeseries,
    WalletNFTs,
    WalletTokens,
    WalletIntegrations,
    WalletRequestSettings,
)


class WalletBalancesClient:
    __ws_client: WebSocketClient

    def __init__(self, ws_client: WebSocketClient):
        self.__ws_client = ws_client

    async def get_wallet_balances(
        self,
        wallet_addr: str,
        chain: ChainKeys,
        ignore_cache: bool = False,
        wallet_request_settings: WalletRequestSettings = WalletRequestSettings(),
    ) -> AsyncGenerator[WalletIntegrations | WalletNFTs | WalletTokens | None, None]:
        request_id = str(uuid.uuid4())

        data_dict: WalletBalancesData = {"address": wallet_addr, "chain": chain, "ignore_cache": ignore_cache}
        if wallet_request_settings:
            self.__convert_sets_to_lists(wallet_request_settings)
            for key, value in asdict(wallet_request_settings).items():
                data_dict[key] = value

        msg: BalancesMessage = {
            "method": "COMMAND",
            "command": {
                "key": "WALLET_BALANCES",
                "data": data_dict,
            },
            "request_id": request_id,
        }
        finished_event_type = "WALLET_BALANCES_FINISHED"
        async for response in self.__ws_client.handle_response(
            request_id=request_id,
            msg=msg,
            finished_event_type=finished_event_type,
        ):
            yield response

    async def get_wallet_timeseries(
        self,
        wallet_addr: str,
        chain: ChainKeys,
        tier: TierKeys,
        wallet_request_settings: WalletRequestSettings = WalletRequestSettings(),
    ) -> AsyncGenerator[Timeseries, None]:
        request_id = str(uuid.uuid4())

        data_dict: TimeseriesData = {"address": wallet_addr, "chain": chain, "tier": tier}
        if wallet_request_settings:
            self.__convert_sets_to_lists(wallet_request_settings)
            for key, value in asdict(wallet_request_settings).items():
                data_dict[key] = value
        msg: TimeseriesMessage = {
            "method": "COMMAND",
            "command": {
                "key": "GET_WALLET_TIMESERIES",
                "data": data_dict,
            },
            "request_id": request_id,
        }
        finished_event_type = "GET_WALLET_TIMESERIES_FINISHED"
        async for response in self.__ws_client.handle_response(
            request_id=request_id,
            msg=msg,
            finished_event_type=finished_event_type,
        ):
            yield response

    def __convert_sets_to_lists(self, wallet_request_settings: WalletRequestSettings):
        wallet_request_settings.hide_nfts = list(wallet_request_settings.hide_nfts)  # type: ignore
        wallet_request_settings.hide_tokens = list(wallet_request_settings.hide_tokens)  # type: ignore
        wallet_request_settings.hide_recipes = list(wallet_request_settings.hide_recipes)  # type: ignore
        wallet_request_settings.hide_integrations = list(wallet_request_settings.hide_integrations)  # type: ignore
