from operator import mod
import sys, os
import asyncio
import shutil
import importlib
from importlib import resources
from pathlib import Path

from timeit import default_timer as timer

import emoji

from stattik.site import Site

async def bake():
    start = timer()

    site = await Site.produce()
    await site.begin()

    '''
    if os.path.isdir("./static"):
        shutil.copytree("./static", "./dist", dirs_exist_ok=True)
    '''

    site_static = Path(site.root, 'static')

    if os.path.isdir(site_static):
        shutil.copytree(site_static, "./dist", dirs_exist_ok=True)

    if hasattr(site, 'apps'):
        for module_name in site.apps:
            #print("Module name:  ", module_name)
            module = importlib.import_module(f"{module_name}.static")
            #print("Module:  ", module)
            root = os.path.dirname(module.__file__)
            dist = Path(os.getcwd(), './dist')
            walk(resources.files(module), root, dist)

    end = timer()
    elapsed = end - start

    #count = await site.page_count
    
    #print(emoji.emojize(f"Indexed {count} pages in {str(round(elapsed, 2))} seconds :thumbs_up:"))

skiplist = [
    '__pycache__',
    '__init__.py'
]

def walk(traversable, root, dist):
    if traversable.name in skiplist:
        return
    #print(traversable)
    rel_path = traversable.relative_to(root)
    #print('REL:  ', rel_path)

    dst_path = dist / rel_path
    #print('DEST:  ', dst_path)
    
    if traversable.is_dir():
        if not str(rel_path) == '.':
            #dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.mkdir(parents=True, exist_ok=True)

        for child in traversable.iterdir():
            walk(child, root, dist)

    elif traversable.is_file():
        with traversable.open("rb") as src:
            with open(dst_path, "wb") as dst:
                count = os.path.getsize(traversable)
                os.copy_file_range(src.fileno(), dst.fileno(), count, 0)

if __name__ == "__main__":
    asyncio.run(bake())
