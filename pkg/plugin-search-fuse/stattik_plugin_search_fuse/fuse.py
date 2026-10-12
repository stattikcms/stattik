import os
import errno
import shutil
from pathlib import Path

from loguru import logger

import json

from bs4 import BeautifulSoup

from stattik.site import Site

class FuseIndexer:
    async def index(self):
        site = Site.instance
        db = site.database

        pages = await db['Page'].all()

        entries = []

        for page in pages:
            entries.append(await self.index_page(page))

        #print(entries)
        #print(json.dumps(entries))

        dst_path = Path("dist/search/index.json")

        try:
            os.remove(dst_path)
        except OSError:
            pass

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dst_path, "w") as myfile:
            myfile.write(json.dumps(entries))


    async def index_page(self, page):
        #print(page.__dict__)
        html = page.content
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        #print(text)

        return {
            'url': str(page.url),
            'title': page.title,
            'description': page.description,
            'content': text
        }