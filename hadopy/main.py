"""Everything."""

import sys
import subprocess
import click
from multiprocessing import Pool, cpu_count
from typing import List

Command = List[str]
ENCODING = 'utf-8'


def command_worker(text: str, command: Command) -> str:
    """
        Use the given command on the given text and return the output pipe.

        :param text: String of text
        :param command: Terminal command to pipe the text through
        :return: output piped from the command
    """
    return subprocess.run(command,
                          stdout=subprocess.PIPE,
                          input=text,
                          encoding=ENCODING
                          ).stdout


@click.command()
@click.option('--mapper', '--m', help='Mapper command, for example "python mapper.py"')
@click.option('--reducer', '--r', help='Reducer command, for example "python reducer.py"')
@click.option('--n_threads', help="Number of threads to use", default=cpu_count())
@click.option('--sort', '--s', help="Sort the output", default=True)
def cli(mapper, reducer, n_threads, sort):
    """
    If you want to map reduce parallel but hadoop is overkill,
    with Hadopy you can run map reduce in python.
    """
    if mapper or reducer:
        working_text = sys.stdin.read()

        if mapper:
            mapper: Command = mapper.split(' ')
            split_text = working_text.split('\n')

            with Pool(n_threads) as pool:
                working_text = ''.join(pool.starmap(
                    command_worker,
                    map(lambda i: ('\n'.join(split_text[i::n_threads]), mapper), range(n_threads))
                ))

        if reducer:
            reducer: Command = reducer.split(' ')
            if sort:
                working_text = '\n'.join(sorted(working_text.split('\n')))

            working_text = command_worker(working_text, reducer)

        sys.stdout.write(working_text)
    else:
        click.secho("Use either --mapper or --reducer, otherwise hadopy will be of no use, "
                    "\nuse --help for more info.", fg='red')


if __name__ == "__main__":
    cli()
