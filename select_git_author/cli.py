"""
CLI to select interactively the git author
"""

import os
import sys
import subprocess

from typing import List

import click
import questionary
import click_prompt

CONTEXT_SETTINGS = dict(ignore_unknown_options=True,
                        allow_extra_args=True,
                        allow_interspersed_args=True)

NEW_AUTHOR_OPTION = 'Add new author'

def git_authors() -> List[str]:
    """
    Get a list of possible git authors from the git configuration
    """
    git_author_file = os.path.expanduser('~/.git_authors')
    if os.path.isfile(git_author_file):
        with open(git_author_file, 'r') as f:
            lines = f.readlines()
        if not lines:
            raise Exception(f'{git_author_file} should should not be empty')
        return [l.strip() for l in lines]
    return []

def query_new_author() -> str:
    """
    Prompts the user for a new author entry
    """
    name = questionary.text("What's the author's full name").ask()
    email = questionary.text("What's the author's e-mail address?").ask()
    author = f'{name} <{email}>'
    git_author_file = os.path.expanduser('~/.git_authors')
    if questionary.confirm(f'Do you want to store {author} to {git_author_file}?').ask():
        with open(git_author_file, 'a') as f:
            f.write(author + os.linesep)
    return author

@click.command(context_settings=CONTEXT_SETTINGS)
@click_prompt.choice_option('--author',
              type=click.Choice(git_authors() + [NEW_AUTHOR_OPTION]))
def cli(author, set_commitor: bool):
    if author == NEW_AUTHOR_OPTION:
        author = query_new_author()
    args = ['/usr/bin/git'] +  ['commit', '--author', f'"{author}"'] + sys.argv[2:]
    completed_process = subprocess.run(' '.join(args), shell=True)
    sys.exit(completed_process.returncode)
