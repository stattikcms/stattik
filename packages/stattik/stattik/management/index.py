import sys
import asyncio

from timeit import default_timer as timer

import emoji

from stattik.site import Site

async def index():
    start = timer()

    site = await Site.produce()
    await site.begin()
    await site.index()

    end = timer()
    elapsed = end - start

    #count = await site.page_count
    
    #print(emoji.emojize(f"Indexed {count} pages in {str(round(elapsed, 2))} seconds :thumbs_up:"))

if __name__ == "__main__":
    asyncio.run(index())
