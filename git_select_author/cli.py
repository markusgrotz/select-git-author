#!/usr/bin/env python3
from typing import List

import os
import sys
import subprocess

import click
import questionary

CONTEXT_SETTINGS=dict(ignore_unknown_options=True, allow_extra_args=True, allow_interspersed_args=True)
NEW_AUTHOR_OPTION = 'Add new author'

class QuestionaryOption(click.Option):
    """
    Prompts user the option

    ..see::
    https://stackoverflow.com/questions/54311067/using-a-numeric-identifier-for-value-selection-in-click-choice
    """
    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

    def prompt_for_value(self, ctx):
        if len(self.type.choices) == 1:
            return self.type.choices[0]
        return questionary.select(self.prompt, choices=self.type.choices).unsafe_ask()


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

def query_new_author() -> str:
    name = questionary.text("What's the author's full name").ask()
    email = questionary.text("What's the author's  e-mail address?").ask()
    author = f'{name} <{email}>'
    git_author_file = os.path.expanduser('~/.git_authors')
    if questionary.confirm(f'Do you want to store {author} to {git_author_file}?').ask():
        with open(git_author_file, 'a') as f:
            f.write(author)
    return author




@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--author', prompt=True, type=click.Choice(git_authors() + [NEW_AUTHOR_OPTION]), cls=QuestionaryOption)
def cli(author):
    if author == NEW_AUTHOR_OPTION:
        author = query_new_author()
        
    args = ['/usr/bin/git'] +  ['commit', '--author', f'"{author}"'] + sys.argv[2:] 
    c = subprocess.run(' '.join(args), shell=True)
    sys.exit(c.returncode)

