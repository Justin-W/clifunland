import json
import logging
from pprint import pformat

import click

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


def main():
    cli()


if __name__ == '__main__':
    main()
