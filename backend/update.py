import asyncio
from common.response.response_one_c import OneCParser
from common.response.response_b24 import Bitrix24


async def main():
    await Bitrix24().get_objects()
    await OneCParser().create_products("offers0_1.xml")


if __name__ == "__main__":
    asyncio.run(main())
