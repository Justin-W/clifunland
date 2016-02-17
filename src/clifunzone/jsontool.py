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
        click_utils.echo_context(ctx)

    subcommand = ctx.invoked_subcommand
    # click.echo('Subcommand: {}'.format(subcommand))
    if subcommand is None:
        click.echo('I was invoked without a subcommand...')
    else:
        if debug:
            click.echo('I am about to invoke subcommand: %s.' % subcommand)


@cli.command()
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


@cli.command(name='repr')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
def reprcommand(input, **kwargs):
    """
    Provides the python repr() representation of the parsed input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = json.load(f)
        s = repr(data)
        click.echo(s)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
def info(input, **kwargs):
    """
    Provides info about the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = json.load(f)
        d = {
            'type': type(data),
            'length': len(data),
            # 'repr': repr(data),
            'keys': data.keys()
        }
        # click.echo('type={}'.format(t))
        # click.echo('len={}'.format(len(data)))
        # click.echo('keys={}'.format(', '.join(data.keys())))
        click.echo(d)
        # click.echo('iter={}'.format(', '.join(iter(data))))
        # click.echo('dir={}'.format(dir(data)))
        # click.echo('repr={}'.format(repr(data)))


@cli.command(name='format')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input."
                   " Or '-' to use stdin (e.g. piped input).")
@click.option('--compact', '-c', 'style', flag_value='compact',
              help='output format style that minimizes the output.'
                   ' overrides the indent and separator options.')
@click.option('--pretty', '-p', 'style', flag_value='pretty',
              help='output format style that generates human readable output.'
                   ' overrides the indent and separator options.')
@click.option('--flat', '-f', 'style', flag_value='flat',
              help='output format style that generates multi-line, non-indented output.'
                   ' overrides the indent and separator options.')
@click.option('--indent', type=click.IntRange(min=0),
              help='Default is None. Must be a non-negative integer.'
                   ' Maps to the corresponding argument of the json.dumps() function.')
@click.option('--skip-keys', '--skip', '--ignore-key-errors', '-ike', 'skip_keys', type=click.BOOL)
@click.option('--sort-keys', '--sorted/--unsorted', '--sort', '-s', 'sort_keys', default=False,
              help='causes the keys of each element to be output in sorted order.')
@click.option('--ensure-ascii/--ensure-ascii-off', '-ea+/-ea-', default=True,
              help='Default is True.'
                   ' Maps to the corresponding argument of the json.dumps() function.')
@click.option('--check-circular/--check-circular-ff', '-cc+/-cc-', default=True,
              help='Default is True.'
                   ' Maps to the corresponding argument of the json.dumps() function.')
@click.option('--allow-nan/--allow-nan-off', '-nan+/-nan-', default=True,
              help='Default is True.'
                   ' Maps to the corresponding argument of the json.dumps() function.')
@click.option('--item-separator', '-is', default=', ', help='the item separator')
@click.option('--dict-separator', '-ds', default=': ', help='the dictionary/element separator')
def formatcommand(input, style, indent, skip_keys, sort_keys, ensure_ascii, check_circular, allow_nan,
                  item_separator, dict_separator, **kwargs):
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
