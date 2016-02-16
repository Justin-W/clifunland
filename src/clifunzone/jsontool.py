import json

import click

import click_utils


def process(**kwargs):
    ctx = click.get_current_context()

    # debug_ = ctx.params.get('debug') or ctx.parent.params.get('debug') if ctx.parent else False
    # if debug_:
    #     click_utils.echo_context(ctx)

    click_utils.inherit_parent_params(ctx, ('debug',))

    debug_ = ctx.params['debug']

    if debug_:
        click.echo('Debug mode: %s' % ('enabled' if debug_ else 'disabled'))
        click_utils.echo_context(ctx)
        click_utils.echo_kwargs(kwargs)

    subcommand = ctx.invoked_subcommand
    if subcommand == 'info':
        pass


@click.group(context_settings=click_utils.CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version='1.0.0')
@click.option('--debug/--silent', '-d/-s', 'debug', default=False)
# @click.option('--debug', '-d', 'debug', flag_value=True, default=True)
# @click.option('--silent', '-s', 'debug', flag_value=False)
def cli(debug):
    ctx = click.get_current_context()
    if debug:
        echo_context(ctx)

    subcommand = ctx.invoked_subcommand
    # click.echo('Subcommand: {}'.format(subcommand))
    if subcommand is None:
        click.echo('I was invoked without a subcommand...')
    else:
        if debug:
            click.echo('I am about to invoke subcommand: %s.' % subcommand)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input to be echoed. Or '-' to use stdin (e.g. piped input).")
def echo(input, **kwargs):
    """
    Echo the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input to be echoed. Or '-' to use stdin (e.g. piped input).")
@click.option('--compact', '-c', 'style', flag_value='compact',
              help='output format style that minimizes the output.'
                   ' overrides the indent and separator options.')
@click.option('--pretty', '-p', 'style', flag_value='pretty',
              help='output format style that generates human readable output.'
                   ' overrides the indent and separator options.')
@click.option('--flat', '-f', 'style', flag_value='flat',
              help='output format style that generates multi-line, non-indented output.'
                   ' overrides the indent and separator options.')
# @click.option('--compact', '-c', type=click.BOOL,
#               help='shortcut that overrides the indent and separators options to generate the most compact output possible.')
# @click.option('--pretty', '-p', type=click.BOOL,
#               help='shortcut that overrides the indent and separators options to generate more readable output.')
@click.option('--indent', '-in', type=click.IntRange(min=0))
# @click.option('--indent', '-in', help="'None', or a non-negative integer.")
@click.option('--skip-keys', '--skip', '--ignore-key-errors', '-ike', 'skip_keys', type=click.BOOL)
@click.option('--sort-keys', '--sort', '-s', type=click.BOOL)
@click.option('--ensure-ascii/--ensure-ascii=0', '-ea/-ea=0', '-ea+/-ea-', default=True)
@click.option('--check-circular/--check-circular=0', '-cc/-cc=0', '-cc+/-cc-', default=True)
@click.option('--allow-nan/--allow-nan=0', '-nan/-nan=0', '-nan+/-nan-', default=True)
@click.option('--item-separator', '-is', default=', ', help='the item separator')
@click.option('--dict-separator', '-ds', default=': ', help='the dictionary/element separator')
def format(input,
           style,
           indent,
           skip_keys, sort_keys,
           ensure_ascii, check_circular, allow_nan,
           item_separator, dict_separator,
           **kwargs):
    """
    Formats the JSON input. See the docs of the json.dumps() function (in python's builtin json module) for details.
    """
    if style == 'compact':
        separators = (',', ':')
        indent = None
    elif style == 'pretty':
        # separators = (',', ':')
        separators = None
        indent = 2
    elif style == 'flat':
        separators = (',', ': ')
        indent = 0
    elif item_separator or dict_separator:
        if not item_separator:
            item_separator = ', '
        if not dict_separator:
            dict_separator = ': '
        separators = (item_separator, dict_separator)
    else:
        separators = None

    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        # s = f.read()
        # json.loads(s)
        data = json.load(f)
        # s = json.dumps(data, skipkeys=skip_keys, sort_keys=sort_keys,
        #                ensure_ascii=ensure_ascii, check_circular=check_circular,
        #                allow_nan=allow_nan, indent=indent, separators=separators,
        #                encoding='utf-8', default=None, **kw)
        s = json.dumps(data, skipkeys=skip_keys, sort_keys=sort_keys,
                       ensure_ascii=ensure_ascii, check_circular=check_circular,
                       allow_nan=allow_nan, indent=indent, separators=separators)
        click.echo(s)


def main():
    cli()


if __name__ == '__main__':
    # main(default_map={
    #     'info': {
    #         'input': 'rfxml_parse.input.01.xml'
    #     }
    # })
    main()