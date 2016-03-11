import json
from collections import Counter
from pprint import pformat

import click
from gherkin.parser import Parser

from clifunzone import click_utils
from clifunzone.reflection_utils import varsdict
from clifunzone.walk_items import walk_items


# from gherkin.pickles.compiler import compile  #as gherkin_compile


@click.group(context_settings=click_utils.CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version='1.0.0')
@click.option('--debug/--silent', '-d/-s', 'debug', default=False)
def cli(debug):
    """
    Provides CLI commands for interacting with Gherkin data/files (.feature format).
    """
    pass


@cli.command(short_help='echo the unparsed input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
def echo(input, **kwargs):
    """
    Echo the (unparsed) input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--verbose', '-v', is_flag=True, type=click.BOOL,
              help='enables more detailed output.')
@click.option('--pyformat', '-py', is_flag=True, type=click.BOOL,
              help='enables python-style output (instead of JSON).')
def info(input, verbose, pyformat, **kwargs):
    """
    Provides info about the input. Requires valid input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        parser = Parser()
        feature_text = f.read()
        feature = parser.parse(feature_text)

        metrics = {}
        steps = [a[-1] for d, k, v, a in walk_items(feature) if k == 'type' and v == 'Step']
        scenarios = [a[-1] for d, k, v, a in walk_items(feature) if k == 'type' and v == 'Scenario']
        # tables = [a[-1] for d, k, v, a in walk_items(feature) if k == 'type' and v == 'DataTable']
        ctr_type = Counter((v for d, k, v in walk_items(feature, ancestors=False) if k == 'type'))
        ctr_kw = Counter((v for d, k, v in walk_items(feature, ancestors=False) if k == 'keyword'))
        metrics.update({'count': {
            'Keywords': ctr_kw,
            'Types': ctr_type,
        }})
        metrics.update({'content': {
            'Scenarios': [d['name'] for d in scenarios],
            'Steps': [d['text'] for d in steps],
        }})
        data = metrics

        if verbose:
            data['_object'] = {
                'type': type(feature),
                'members': sorted(varsdict(feature).keys())
            }
        if pyformat:
            s = pformat(data)
        else:
            s = json.dumps(data, indent=2, sort_keys=True)
        click.echo(s)


def main():
    cli()


if __name__ == '__main__':
    main()
