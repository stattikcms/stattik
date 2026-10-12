import asyncio
from functools import wraps

import cProfile

import click

from .assemble import assemble as _assemble
from .build import build as _build
from .bake import bake as _bake

from .render import render as _render
from .index import index as _index
from .clean import clean as _clean

from .develop import develop as _develop
from .serve import serve as _serve

from .deploy import deploy

def async_cmd(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    return asyncio.run(func(*args, **kwargs))
  return wrapper

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        develop()

cli.add_command(deploy)

@cli.command()
@click.pass_context
def assemble(ctx):
    asyncio.run(_assemble())

@cli.command()
@click.pass_context
def build(ctx):
    asyncio.run(_build())

@cli.command()
@click.pass_context
def bake(ctx):
    asyncio.run(_bake())

@cli.command()
@click.pass_context
def render(ctx):
    asyncio.run(_render())

@cli.command()
@click.pass_context
def index(ctx):
    asyncio.run(_index())

@cli.command()
@click.pass_context
def develop(ctx):
    _develop()

@cli.command()
@click.pass_context
def serve(ctx):
    _serve()

@cli.command()
@click.pass_context
def clean(ctx):
    _clean('dist')
