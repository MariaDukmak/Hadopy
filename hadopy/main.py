import sys
import subprocess
import click
from multiprocessing import Pool, cpu_count
from typing import List

Command = List[str]
ENCODING = 'ascii'

# bin/hadoop jar share/hadoop/tools/lib/hadoop-*streaming*.jar -file ~/mapper.py -mapper ~/mapper.py -file ~/reducer.py -reducer ~/reducer.py -input ~/tmp -output ~/output
# cat columbus.txt | ./mapper_lf.py | sort -n | ./reduce_lf.py
# cat example/products.txt | python main.py --mapper "python example/mapper.py" --reducer "python example/reducer.py"


def mapper_worker(text: str, mapper: Command) -> str:
    return subprocess.run(mapper,
                          stdout=subprocess.PIPE,
                          input=text,
                          encoding=ENCODING
                          ).stdout


def reducer_worker(texts: List[str], reducer: Command) -> str:
    concatenated = '\n'.join(sorted(filter(lambda x: '\t' in x, '\n'.join(texts).split('\n'))))

    return subprocess.run(reducer,
                          stdout=subprocess.PIPE,
                          input=concatenated,
                          encoding=ENCODING
                          ).stdout


@click.command()
@click.option('--mapper', '--m', prompt='Mapper command', help='Mapper command, for example "python mapper.py"')
@click.option('--reducer', '--r', prompt='Reducer command', help='Reducer command, for example "python reducer.py"')
@click.option('--n_threads', help="Number of threads to use", default=cpu_count())
def cli(mapper, reducer, n_threads):
    mapper: Command = mapper.split(' ')
    reducer: Command = reducer.split(' ')

    line_split = sys.stdin.read().split('\n')

    with Pool(n_threads) as pool:
        mapped = pool.starmap(
            mapper_worker,
            map(lambda i: ('\n'.join(line_split[i::n_threads]), mapper), range(n_threads))
        )

    sys.stdout.write(reducer_worker(mapped, reducer))


if __name__ == "__main__":
    cli()
