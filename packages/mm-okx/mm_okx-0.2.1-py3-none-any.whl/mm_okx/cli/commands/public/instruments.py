from mm_std import print_json

from mm_okx.clients.public import PublicClient


async def run(inst_type: str, proxy: str | None) -> None:
    client = PublicClient(proxy=proxy)
    res = await client.get_instruments_raw(inst_type)
    print_json(res)
