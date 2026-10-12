import sys
import asyncio

from timeit import default_timer as timer

import emoji

from stattik.site import Site


async def bake():
    start = timer()

    site = await Site.produce()
    await site.begin()
    await site.bake()

    end = timer()
    elapsed = end - start

    print(emoji.emojize(f"Baked site in {str(round(elapsed, 2))} seconds :thumbs_up:"))


if __name__ == "__main__":
    asyncio.run(bake())
