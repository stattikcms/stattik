import asyncio

import click

from .netlify import netlify

@click.group()
def deploy():
    pass

deploy.add_command(netlify)