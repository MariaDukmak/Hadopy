import sys
import subprocess
import click
from multiprocessing import Pool

# bin/hadoop jar share/hadoop/tools/lib/hadoop-*streaming*.jar -file ~/mapper.py -mapper ~/mapper.py -file ~/reducer.py -reducer ~/reducer.py -input ~/tmp -output ~/output
# cat columbus.txt | ./mapper_lf.py | sort -n | ./reduce_lf.py

@click.command()
@click.option('--mapper', '--m', prompt='Mapper command', help='Mapper command, for example "python mapper.py"')
@click.option('--reducer', '--r', prompt='Reducer command', help='Reducer command, for example "python reducer.py"')
@click.option('--n_threads', prompt="Number of threads", help="Number of threads to use")
def cli(mapper, reducer, n_threads):
    line_split = sys.stdin.read().split('\n')
    with Pool(n_threads) as pool:
        pool.map(
            lambda lines: subprocess.Popen(mapper.split(' '),
                                           tdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           stdin=),
            [line_split[i::n_threads] for i in range(n_threads)]
        )
        mapped = subprocess.Popen(mapper.split(' '),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  stdin=sys.stdin)

    # Unfortunately "sorted" was already taken
    ordered = subprocess.Popen(['sort'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             stdin=mapped.stdout)

    reduced = subprocess.Popen(reducer.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               stdin=ordered.stdout)

    click.secho(reduced.communicate()[0].decode())


if __name__ == "__main__":
    cli()
