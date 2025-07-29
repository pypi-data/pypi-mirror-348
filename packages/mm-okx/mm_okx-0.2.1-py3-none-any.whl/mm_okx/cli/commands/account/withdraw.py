from decimal import Decimal
from pathlib import Path

from mm_std import print_json

from mm_okx.clients.account import AccountClient, AccountConfig


async def run(*, account: Path, ccy: str, amt: Decimal, fee: Decimal, to_addr: str, chain: str | None = None) -> None:
    client = AccountClient(AccountConfig.from_toml_file(account))
    res = await client.withdraw(ccy=ccy, amt=amt, fee=fee, to_addr=to_addr, chain=chain)
    print_json(res)
