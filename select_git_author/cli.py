"""
CLI to select interactively the git author
"""

import os
import sys
import subprocess

from typing import List
from typing import Tuple

import click
import questionary
import click_prompt

CONTEXT_SETTINGS = dict(ignore_unknown_options=True,
                        allow_extra_args=True,
                        allow_interspersed_args=True)

NEW_AUTHOR_OPTION = 'Add new author'


def main():
    cli()

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


def parse_name_mail(text: str) -> Tuple[str, str]:
    name, email = text.rsplit('<', maxsplit=1)
    email = email.split('>')[0]
    name = name.strip()
    return name, email

@click.command(context_settings=CONTEXT_SETTINGS)
@click_prompt.choice_option('--author',
              type=click.Choice(git_authors() + [NEW_AUTHOR_OPTION]))
@click.option('--set-commitor/--no-commitor', default=True)
def cli(author, set_commitor: bool):
#def cli(author):
    if author == NEW_AUTHOR_OPTION:
        author = query_new_author()
        
    name, email = parse_name_mail(author)
        
    env = os.environ.copy()
    
    env['GIT_AUTHOR_NAME'] = name
    env['GIT_AUTHOR_EMAIL'] = email
    
    if set_commitor:
        env['GIT_COMMITTER_NAME'] = name
        env['GIT_COMMITTER_EMAIL'] = email


    args = ['git', 'commit', '--author', f'"{author}"'] + sys.argv[1:]
    completed_process = subprocess.run(args, env=env)
    sys.exit(completed_process.returncode)
