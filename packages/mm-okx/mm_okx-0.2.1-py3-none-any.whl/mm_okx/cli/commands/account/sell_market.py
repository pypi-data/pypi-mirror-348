from decimal import Decimal
from pathlib import Path

from mm_std import print_json

from mm_okx.clients.account import AccountClient, AccountConfig


async def run(account: Path, inst_id: str, sz: Decimal) -> None:
    client = AccountClient(AccountConfig.from_toml_file(account))
    res = await client.sell_market(inst_id, sz)
    print_json(res)
