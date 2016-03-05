import json
import logging
from pprint import pformat

import click
import re

from clifunzone import click_utils
from clifunzone import dict_utils
from clifunzone import txt_utils


def debug_context(**kwargs):
    ctx = click.get_current_context()

    click_utils.inherit_parent_params(ctx, ('debug',))

    debug_ = ctx.params['debug']

    if debug_:
        click.echo('Debug mode: %s' % ('enabled' if debug_ else 'disabled'))
        click_utils.echo_context(ctx)
        click_utils.echo_kwargs(kwargs)

        subcommand = ctx.invoked_subcommand
        click.echo('subcommand: %s' % subcommand)


@click.group(context_settings=click_utils.CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version='1.0.0')
@click.option('--debug/--silent', '-d/-s', 'debug', default=False)
# @click.option('--debug', '-d', 'debug', flag_value=True, default=True)
# @click.option('--silent', '-s', 'debug', flag_value=False)
def cli(debug):
    """
    Provides CLI commands for interacting with text data/files.
    """
    ctx = click.get_current_context()
    if debug:
        click_utils.echo_context(ctx)

    subcommand = ctx.invoked_subcommand
    if subcommand is None:
        click.echo('I was invoked without a subcommand...')
    else:
        if debug:
            click.echo('I was invoked with subcommand: %s.' % subcommand)

    try:
        debug_context(**{})
    except:
        logging.exception('debug_context error')


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
@click.option('--json', '-oj', 'output_format', flag_value='json',
              help='renders the output as JSON.')
@click.option('--python', '--dict', '-od', 'output_format', flag_value='dict',
              help='renders the output as a python dictionary.')
@click.option('--xml', '-ox', 'output_format', flag_value='xml',
              help='renders the output as XML.')
@click.option('--flatten', '--flat', '-f', 'flat', is_flag=True, type=click.BOOL,
              help='enables a flattened (vs. nested) hierarchical structure for the output.')
@click.option('--verbose', '-v', is_flag=True, type=click.BOOL,
              help='enables more detailed output.')
def info(input, output_format, verbose, flat, **kwargs):
    """
    Provides info about the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = f.read()
        d = {}
        d.update({'content': txt_utils.get_info(data)})
        # if verbose:
        #     d['_object'] = {
        #         'type': type(data),
        #         'members': sorted(varsdict(data).keys())
        #     }
        if flat:
            d = dict_utils.flatten(d)

        if not output_format:
            output_format = 'json'
        if output_format == 'dict':
            s = pformat(d)
        elif output_format == 'json':
            s = json.dumps(d, indent=2, sort_keys=True)
        # elif output_format == 'xml':
        else:
            raise NotImplementedError('Unsupported output format: %s' % output_format)
        click.echo(s)


@cli.command(short_help='outputs lorem ipsum text')
def lorem(**kwargs):
    """
    Outputs 'lorem ipsum' text.
    """
    s = txt_utils.lorem_ipsum()
    click.echo(s)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--whitespace', '--space', '-ss', 'split_scope', flag_value='whitespace',
              help='splits the input at any whitespace.')
@click.option('--words', '-sw', 'split_scope', flag_value='word',
              help='splits the input at word boundaries.')
@click.option('--sentence', 'split_scope', flag_value='sentence',
              help='splits the input at sentence boundaries.')
@click.option('--separator', '-sep', type=click.STRING,
              help='the token separator to use for the output. Default is a newline.')
def split(input, split_scope, separator, **kwargs):
    """
    Splits the input into tokens.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = f.read()

        if not split_scope:
            split_scope = 'whitespace'
        if split_scope == 'whitespace':
            tokens = data.split()
        elif split_scope == 'word':
            tokens = txt_utils.get_words(data)
        # elif split_scope == 'sentence':
        #     tokens = txt_utils.get_sentences(data)
        else:
            raise NotImplementedError('Unsupported split scope: %s' % split_scope)
        if separator:
            click.echo(separator.join(tokens))
        else:
            for s in tokens:
                click.echo(s)


@cli.command(short_help='removes portions of the input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--delimiter', '-d', type=click.STRING,
              help='the token delimiter to use when splitting the input. Default is a newline.')
@click.option('--value1', '-v1', 'values1', type=click.STRING, multiple=True,
              help='A value (e.g. a word or regex pattern) to match against the tokens in the parsed input.'
                   ' Repeatable. (Can be specified multiple times.)'
                   ' If repeated, a token that matches any of the given values is considered a match.')
@click.option('--value2', '-v2', 'values2', type=click.STRING, multiple=True,
              help='A value (e.g. a word or regex pattern) to match against the tokens in the parsed input.'
                   ' Repeatable. (Can be specified multiple times.)')
@click.option('--regex', '-r', is_flag=True, type=click.BOOL,
              help="causes all 'search' values (-v1 and -v2) to be processed as regex patterns.")
@click.option('--regex-ignore-case', '-ri', 'regex_ignore_case', is_flag=True, type=click.BOOL,
              help='causes regex operations to be performed case-insensitively.')
def distance(input, delimiter, values1, values2, regex, regex_ignore_case, **kwargs):
    """
    Calculates distance metrics for 2 sets of 'search' values against a sequence of tokens.

    The token sequence is obtained by splitting the delimited input.

    If a 'search' set contains multiple values, the values are treated as a "(value1 OR value2 OR ... OR valueN)"
    (i.e. logical OR). I.e. A token need only 'match' any 1 of the supplied values in a 'search' set
    for that token to be considered a match for the set.

    If multiple tokens 'match' each set, the distance metrics are computed for all combinations of the locations
    from each set of matches. (I.e. The cartesian product of the two sets.)

    Examples:

        \b
        Example: Simple 1x2 (tiny input):
        $ echo 'Lorem ipsum dolor sit amet' | python -m clifunzone.txttool split -sw | python -m clifunzone.txttool distance -v1 Lorem -v2 sit -v2 amet
        {'max': 4, 'mean': 3.5, 'min': 3}

        \b
        Example: Simple 1x2 (larger input):
        $ python -m clifunzone.txttool lorem | python -m clifunzone.txttool split -sw | python -m clifunzone.txttool distance -v1 Lorem -v2 sit -v2 amet
        {'max': 852, 'mean': 483.5, 'min': 3}

        \b
        Example: Simple 2x2:
        $ python -m clifunzone.txttool lorem | python -m clifunzone.txttool split -sw | python -m clifunzone.txttool distance -v1 lorem -v1 dolor -v2 consectetur -v2 adipiscing
        {'max': 889, 'mean': 467.0740740740741, 'min': 3}

        \b
        Example: Regex 1x1:
        $ python -m clifunzone.txttool lorem | python -m clifunzone.txttool split -sw | python -m clifunzone.txttool distance -r -v1 '^Pellentesque$' -v2 '^Vivamus'
        {'max': 528, 'mean': 222.66666666666666, 'min': 24}

        \b
        Example: Regex 1x1 (case insensitive):
        $ python -m clifunzone.txttool lorem | python -m clifunzone.txttool split -sw | python -m clifunzone.txttool distance -r -ri -v1 '^Pellentesque$' -v2 '^Vivamus'
        {'max': 910, 'mean': 287.1212121212121, 'min': 21}
    """
    if not input:
        input = '-'
    if not delimiter:
        delimiter = '\n'
    with click.open_file(input, mode='rb') as f:
        data = f.read()

        tokens = data.split(delimiter)
        flags = re.IGNORECASE if regex_ignore_case else None
        output = txt_utils.find_distances(values1, values2, tokens, regex=regex, regex_flags=flags)
        click.echo(output)


def main():
    cli()


if __name__ == '__main__':
    main()
