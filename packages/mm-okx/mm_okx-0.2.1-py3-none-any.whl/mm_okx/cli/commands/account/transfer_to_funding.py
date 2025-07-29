from decimal import Decimal
from pathlib import Path

from mm_std import print_json

from mm_okx.clients.account import AccountClient, AccountConfig


async def run(account: Path, ccy: str, amt: Decimal) -> None:
    client = AccountClient(AccountConfig.from_toml_file(account))
    res = await client.transfer_to_funding(ccy, amt)
    print_json(res)
