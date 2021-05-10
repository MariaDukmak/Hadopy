import sys
import click

# bin/hadoop jar share/hadoop/tools/lib/hadoop-*streaming*.jar -file ~/mapper.py -mapper ~/mapper.py -file ~/reducer.py -reducer ~/reducer.py -input ~/tmp -output ~/output
# cat columbus.txt | ./mapper_lf.py | sort -n | ./reduce_lf.py

@click.command()
@click.option('--mapper', '--m', prompt='Path to mapper program', help='Path to mapper program')
@click.option('--reducer', '--r', prompt='Path to reducer program', help='Path to reducer program')
def parse(mapper, reducer):
    click.secho(f"{mapper=}, {reducer=}", fg="blue", bold=True)
    print(sys.stdin)


if __name__ == "__main__":
    parse()
