import asyncio
import aiohttp

from datetime import datetime
import sys


async def next_image(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        image = await response.read()
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-4]
        with open(f'artifacts/image_{timestamp}.jpg', 'wb') as file:
            file.write(image)


async def main(url: str, n: int):
    async with aiohttp.ClientSession() as session:
        for _ in range(n):
            await next_image(url, session)


if __name__ == '__main__':
    url = 'https://thishorsedoesnotexist.com/'
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    asyncio.run(main(url, n))
