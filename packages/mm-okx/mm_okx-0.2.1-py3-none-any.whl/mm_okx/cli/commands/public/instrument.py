from mm_std import print_json

from mm_okx.clients.public import PublicClient


async def run(inst_id: str, inst_type: str, proxy: str | None) -> None:
    client = PublicClient(proxy=proxy)
    res = await client.get_instrument_raw(inst_id, inst_type)
    print_json(res)
