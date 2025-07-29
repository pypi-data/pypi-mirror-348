from pathlib import Path

from mm_std import print_json

from mm_okx.clients.account import AccountClient, AccountConfig


async def run(account: Path, ccy: str | None = None, wd_id: str | None = None) -> None:
    client = AccountClient(AccountConfig.from_toml_file(account))
    res = await client.get_withdrawal_history(ccy=ccy, wd_id=wd_id)
    print_json(res)
