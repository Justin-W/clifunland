import json
from pprint import pformat

import click
from gherkin.parser import Parser

from clifunzone import click_utils
from clifunzone.reflection_utils import varsdict


# from gherkin.pickles.compiler import compile  #as gherkin_compile



@click.group(context_settings=click_utils.CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version='1.0.0')
@click.option('--debug/--silent', '-d/-s', 'debug', default=False)
# @click.option('--debug', '-d', 'debug', flag_value=True, default=True)
# @click.option('--silent', '-s', 'debug', flag_value=False)
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
def info(input, verbose, **kwargs):
    """
    Provides info about the input. Requires valid input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        parser = Parser()
        feature_text = f.read()
        feature = parser.parse(feature_text)
        # click.echo(feature)
        # pickles = compile(feature, "path/to/the.feature")
        # click.echo(pickles)

        d = {}
        d.update({'feature': feature})

        info = {
            'keys': feature.keys(),
        }
        if 'scenarioDefinitions' in feature:
            scenarios = [s['name'] for s in feature['scenarioDefinitions']]
            info.update({'scenarios': scenarios})
        d.update({'info': info})

        if verbose:
            d['_object'] = {
                'type': type(feature),
                # 'repr': repr(feature),
                # 'vars': sorted(vars(feature)),
                # 'dir': sorted(dir(feature)),
                'members': sorted(varsdict(feature).keys())
            }
        # click.echo(d)
        # click.echo(sorted(d.items()))
        if verbose:
            s = pformat(d)
        else:
            s = json.dumps(d, indent=2, sort_keys=True)
        click.echo(s)


def main():
    cli()


if __name__ == '__main__':
    main()
