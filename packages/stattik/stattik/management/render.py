import sys
import asyncio

from timeit import default_timer as timer

import emoji

from stattik.site import Site

async def render():
    site = Site.instance

    start = timer()

    await site.render()

    end = timer()
    elapsed = end - start

    count = await site.page_count
    
    print(emoji.emojize(f"Rendered {count} pages in {str(round(elapsed, 2))} seconds :thumbs_up:"))

if __name__ == "__main__":
    asyncio.run(render())
