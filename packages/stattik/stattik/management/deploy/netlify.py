import os
import asyncio
import shutil
import requests

import click

@click.command()
def netlify():
    """Push the schema."""
    asyncio.run(_netlify())

async def _netlify():
    #print('netlify')
    NETLIFY_SITE_ID = os.environ.get('NETLIFY_SITE_ID')
    NETLIFY_TOKEN = os.environ.get('NETLIFY_TOKEN')

    headers = { 
        "Content-Type": "application/zip",
        "Authorization": "Bearer " + NETLIFY_TOKEN
    }

    # make_archive makes a zip file of a folder
    shutil.make_archive('dist', 'zip', './dist')

    # Open the zip file just created, and read the binary contents
    data = open('dist.zip','rb').read()

    # The api URL to post the zip file to
    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys"

    # Using requests library, post the binary data
    r = requests.request('POST', url, headers=headers, data=data)

    # Finally, delete the zip file
    os.remove('dist.zip')