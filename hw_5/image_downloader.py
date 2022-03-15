import asyncio
import aiohttp
import aiofiles

import hashlib
from datetime import datetime
import sys


image_hashes = set()


async def next_image(url: str, session: aiohttp.ClientSession):
    while True:
        async with session.get(url) as response:
            image = await response.read()
            hash = hashlib.sha256(image).hexdigest()

            if hash not in image_hashes:
                image_hashes.add(hash)
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-4]
                async with aiofiles.open(f'artifacts/image_{timestamp}.jpg', 'wb') as file:
                    await file.write(image)
                return


async def main(url: str, n: int):
    async with aiohttp.ClientSession() as session:
        for _ in range(n):
            await next_image(url, session)


if __name__ == '__main__':
    url = 'https://thishorsedoesnotexist.com/'
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    asyncio.run(main(url, n))
