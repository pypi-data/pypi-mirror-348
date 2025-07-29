import base64
import hmac
import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast
from urllib.parse import urlencode

from mm_std import Result, http_request
from pydantic import BaseModel, Field

type JsonType = dict[str, Any]


class Currency(BaseModel):
    ccy: str
    chain: str
    can_dep: bool = Field(..., alias="canDep")
    can_wd: bool = Field(..., alias="canWd")
    max_fee: Decimal = Field(..., alias="maxFee")
    min_fee: Decimal = Field(..., alias="minFee")
    max_wd: Decimal = Field(..., alias="maxWd")
    min_wd: Decimal = Field(..., alias="minWd")


class Balance(BaseModel):
    ccy: str
    avail: Decimal
    frozen: Decimal


class DepositAddress(BaseModel):
    ccy: str
    chain: str
    addr: str


class Withdrawal(BaseModel):
    ccy: str
    chain: str
    amt: Decimal
    wd_id: str = Field(..., alias="wdId")


class WithdrawalHistory(BaseModel):
    wd_id: str = Field(..., alias="wdId")
    chain: str
    ccy: str
    amt: Decimal
    fee: Decimal
    state: int
    tx_id: str = Field(..., alias="txId")
    to: str
    ts: int


class DepositHistory(BaseModel):
    dep_id: str = Field(..., alias="depId")
    ccy: str
    chain: str
    to: str
    amt: Decimal
    ts: int
    tx_id: str = Field(..., alias="txId")
    state: int
    actual_dep_blk_confirm: int = Field(..., alias="actualDepBlkConfirm")


class Transfer(BaseModel):
    trans_id: str = Field(..., alias="transId")
    ccy: str
    client_id: str = Field(..., alias="clientId")
    from_: str = Field(..., alias="from")
    amt: str
    to: str


class AccountClient:
    def __init__(self, api_key: str, passphrase: str, secret_key: str, proxy: str | None) -> None:
        self.api_key = api_key
        self.passphrase = passphrase
        self.secret_key = secret_key
        self.base_url = "https://www.okx.com"
        self.proxy = proxy

    async def get_currencies(self, ccy: str | None = None) -> Result[list[Currency]]:
        res = None
        try:
            res = await self._send_get("/api/v5/asset/currencies", {"ccy": ccy})
            return Result.ok([Currency(**c) for c in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_funding_balances(self, ccy: str | None = None) -> Result[list[Balance]]:
        res = None
        try:
            res = await self._send_get("/api/v5/asset/balances", {"ccy": ccy})
            balances = [Balance(ccy=item["ccy"], avail=item["availBal"], frozen=item["frozenBal"]) for item in res["data"]]

            return Result.ok(balances, {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_trading_balances(self, ccy: str | None = None) -> Result[list[Balance]]:
        res = None
        try:
            res = await self._send_get("/api/v5/account/balance", {"ccy": ccy})
            balances = [Balance(ccy=i["ccy"], avail=i["availBal"], frozen=i["frozenBal"]) for i in res["data"][0]["details"]]
            return Result.ok(balances, {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_deposit_address(self, ccy: str) -> Result[list[DepositAddress]]:
        res = None
        try:
            res = await self._send_get("/api/v5/asset/deposit-address", {"ccy": ccy})
            return Result.ok([DepositAddress(**a) for a in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_deposit_history(self, ccy: str | None = None) -> Result[list[DepositHistory]]:
        res = None
        try:
            res = await self._send_get("/api/v5/asset/deposit-history", {"ccy": ccy})
            return Result.ok([DepositHistory(**d) for d in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_withdrawal_history(self, ccy: str | None = None, wd_id: str | None = None) -> Result[list[WithdrawalHistory]]:
        res = None
        try:
            res = await self._send_get("/api/v5/asset/withdrawal-history", {"ccy": ccy, "wdId": wd_id})
            return Result.ok([WithdrawalHistory(**h) for h in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def withdraw(
        self, *, ccy: str, amt: Decimal, fee: Decimal, to_addr: str, chain: str | None = None
    ) -> Result[list[Withdrawal]]:
        res = None
        params = {"ccy": ccy, "amt": str(amt), "dest": "4", "toAddr": to_addr, "fee": str(fee), "chain": chain}
        try:
            res = await self._send_post("/api/v5/asset/withdrawal", params)
            result = [Withdrawal(**w) for w in res["data"]]
            if result:
                return Result.ok(result, {"response": res})
            if res.get("code") == "58207":
                return Result.err("withdrawal_address_not_whitelisted", {"response": res})
            return Result.err("error", {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def transfer_to_funding(self, ccy: str, amt: Decimal) -> Result[list[Transfer]]:
        res = None
        try:
            res = await self._send_post(
                "/api/v5/asset/transfer", {"ccy": ccy, "amt": str(amt), "from": "18", "to": "6", "type": "0"}
            )
            return Result.ok([Transfer(**t) for t in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def transfer_to_trading(self, ccy: str, amt: Decimal) -> Result[list[Transfer]]:
        res = None
        try:
            res = await self._send_post(
                "/api/v5/asset/transfer", {"ccy": ccy, "amt": str(amt), "from": "6", "to": "18", "type": "0"}
            )
            return Result.ok([Transfer(**t) for t in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def transfer_to_parent(self, ccy: str, amount: Decimal) -> Result[list[Transfer]]:
        # type = 3: subaccount to master account (Only applicable to APIKey from subaccount)
        res = None
        try:
            res = await self._send_post(
                "/api/v5/asset/transfer", {"ccy": ccy, "amt": str(amount), "from": "6", "to": "6", "type": "3"}
            )
            return Result.ok([Transfer(**t) for t in res["data"]], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def buy_market(self, inst_id: str, sz: Decimal) -> Result[str]:
        """
        Place a market order, side=buy
        :param inst_id: for example, BTC-ETH
        :param sz: for example, Decimal("0.123")
        """
        res = None
        params = {"instId": inst_id, "tdMode": "cash", "side": "buy", "ordType": "market", "sz": str(sz)}
        try:
            res = await self._send_post("/api/v5/trade/order", params)
            return Result.ok(res["data"][0]["ordId"], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def sell_market(self, inst_id: str, sz: Decimal) -> Result[str]:
        """
        Place a market order, side=sell
        :param inst_id: for example, BTC-ETH
        :param sz: for example, Decimal("0.123")
        """
        res = None
        params = {"instId": inst_id, "tdMode": "cash", "side": "sell", "ordType": "market", "sz": str(sz)}
        try:
            res = await self._send_post("/api/v5/trade/order", params)
            return Result.ok(res["data"][0]["ordId"], {"response": res})
        except Exception as e:
            return Result.err(e, {"response": res})

    async def get_order_history(self, instrument_id: str = "") -> JsonType:
        url = "/api/v5/trade/orders-history-archive?instType=SPOT"
        if instrument_id:
            url += f"&instId={instrument_id}"
        return await self._request("GET", url)

    async def _send_get(self, request_path: str, query_params: dict[str, object] | None = None) -> JsonType:
        return await self._request("GET", request_path, query_params=query_params)

    async def _send_post(self, request_path: str, body: dict[str, Any] | str = "") -> JsonType:
        return await self._request("POST", request_path, body=body)

    async def _request(
        self, method: str, request_path: str, *, body: dict[str, Any] | str = "", query_params: dict[str, object] | None = None
    ) -> JsonType:
        method = method.upper()
        if method == "GET" and query_params:
            request_path = add_query_params_to_url(request_path, query_params)
        timestamp = get_timestamp()
        message = pre_hash(timestamp, method, request_path, body)
        signature = sign(message, self.secret_key)
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature.decode(),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
        }
        params = None
        if isinstance(body, dict):
            params = body
        res = await http_request(self.base_url + request_path, method=method, data=params, headers=headers, proxy=self.proxy)
        return cast(JsonType, res.parse_json_body())


def pre_hash(timestamp: str, method: str, request_path: str, body: JsonType | str) -> str:
    if isinstance(body, dict):
        body = json.dumps(body)
    return timestamp + method.upper() + request_path + body


def sign(message: str, secret_key: str) -> bytes:
    mac = hmac.new(bytes(secret_key, encoding="utf8"), bytes(message, encoding="utf-8"), digestmod="sha256")
    d = mac.digest()
    return base64.b64encode(d)


def get_timestamp() -> str:
    return datetime.now(tz=UTC).isoformat(sep="T", timespec="milliseconds").removesuffix("+00:00") + "Z"


def add_query_params_to_url(url: str, params: dict[str, object]) -> str:
    return f"{url}?{urlencode(params)}" if params else url
