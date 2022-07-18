#!/usr/bin/env python3

import sys
import subprocess

import rich_click as click
from click_default_group import DefaultGroup

CONTEXT_SETTINGS=dict(ignore_unknown_options=False, allow_extra_args=True)

@click.group(cls=DefaultGroup,  default='git', context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
def cli():
    pass

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def git(ctx):
    args = ['git'] + sys.argv[1:]
    print(args)
    print(' '.join(args))
    c = subprocess.run(args)
    sys.exit(c.returncode)


@cli.command(context_settings=CONTEXT_SETTINGS)
def commit():
    print('commiting')
    args = sys.argv[1:]


if __name__ == '__main__':
	cli()



