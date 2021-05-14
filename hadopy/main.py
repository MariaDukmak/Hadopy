"""Everything."""

import sys
import subprocess
import click
from multiprocessing import Pool, cpu_count
from typing import List

Command = List[str]
ENCODING = 'utf-8'


def mapper_worker(text: str, mapper: Command) -> str:
    """
    Use the given mapper command on the given text.

    :param text: String of text
    :param mapper: Terminal command to pipe the text through
    :return: Mapped string of text
    """
    return subprocess.run(mapper,
                          stdout=subprocess.PIPE,
                          input=text,
                          encoding=ENCODING
                          ).stdout


def reducer_worker(texts: List[str], reducer: Command, sort: bool) -> str:
    """
    Concatenate the given texts and sort the lines and apply the reducer command on it.

    :param sort: Sort mapper output
    :param texts: String of text
    :param reducer: Terminal command to pipe the text through
    :return: Reduced string of text
    """

    if sort:
        concatenated = '\n'.join(sorted(filter(lambda x: len(x) > 1, '\n'.join(texts).split('\n'))))
    else:
        concatenated = '\n'.join(filter(lambda x: len(x) > 1, '\n'.join(texts).split('\n')))

    return subprocess.run(reducer,
                          stdout=subprocess.PIPE,
                          input=concatenated,
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
    if mapper is None:
        click.secho('Please specify a mapper command for example `--mapper "python mapper.py"`', fg='red')
        sys.exit()
    elif reducer is None:
        click.secho('Please specify a reducer command for example `--reducer "python reducer.py"`', fg='red')
        sys.exit()
    else:
        mapper: Command = mapper.split(' ')
        reducer: Command = reducer.split(' ')

        line_split = sys.stdin.read().split('\n')

        with Pool(n_threads) as pool:
            mapped = pool.starmap(
                mapper_worker,
                map(lambda i: ('\n'.join(line_split[i::n_threads]), mapper), range(n_threads))
            )

        sys.stdout.write(reducer_worker(mapped, reducer, sort))


if __name__ == "__main__":
    cli()
