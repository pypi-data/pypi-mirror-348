from mm_std import print_json

from mm_okx.clients.public import PublicClient


async def run(inst_id: str, proxy: str | None) -> None:
    client = PublicClient(proxy=proxy)
    res = await client.get_ticker_raw(inst_id)
    print_json(res)
