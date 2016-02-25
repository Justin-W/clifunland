import json
import sys
from pprint import pformat

import click

import click_utils
import json_utils
from dict_utils import flatten, filter_none_values
from reflection_utils import varsdict


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
    """
    Provides CLI commands for interacting with JSON data/files.
    """
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


@cli.command(name='repr', short_help='show the repr() of the parsed input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
def reprcommand(input, **kwargs):
    """
    Provides the python repr() representation of the parsed input. Requires valid input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = json_utils.load_ordered(f)
        s = repr(data)
        click.echo(s)


@cli.command(short_help='validate the input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--silent', '-s', is_flag=True, type=click.BOOL,
              help='disables the normal console output.')
def validate(input, silent, **kwargs):
    """
    Validates whether the input is syntactically valid and well-formed.
    """
    debug_ = click.get_current_context().parent.params['debug']
    if debug_:
        click.echo('Debug mode: %s' % ('enabled' if debug_ else 'disabled'))
        click.echo('input: %s' % input)
        click.echo('silent: %s' % silent)
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        b = json_utils.contains_valid_json(f)
        if not silent:
            click.echo(b)
        if not b:
            sys.exit(1)  # exit with a failure code of 1


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
        data = json_utils.load_ordered(f)
        d = {
            'length': len(data),
            'keys': sorted(data.keys())
        }
        if verbose:
            d['_object'] = {
                'type': type(data),
                # 'repr': repr(data),
                # 'vars': sorted(vars(data)),
                # 'dir': sorted(dir(data)),
                'members': sorted(varsdict(data).keys())
            }
        # click.echo(d)
        # click.echo(sorted(d.items()))
        if verbose:
            s = pformat(d)
        else:
            s = json.dumps(d, indent=2, sort_keys=True)
        click.echo(s)


@cli.command(short_help='merges JSON fragments under a single parent')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--root', '-r', default='root', help='the name of the new root element')
def mergelines(input, root, **kwargs):
    """
    Merges multiple (valid) JSON fragments into a single JSON.

    For piped input, each line is is assumed to be a separate json fragment.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        s = f.read()
        s = s.strip()
        lines = s.split('\n')
        s = '{"%s": [\n%s\n]}' % (root, ',\n'.join(lines))
        # data = json_utils.loads_ordered(s)
        click.echo(s)


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
@click.option('--lines', '-l', 'style', flag_value='lines',
              help='special output format style that puts each child element of the root element on a separate line.'
                   ' useful in combination with other CLI commands (e.g. grep, head, tail, etc.).')
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
    (Re)formats the JSON input. Requires valid input.

    Supports several predefined, named format 'styles' (e.g. -p, -c, -f, -l),
    as well as various 'low-level' formatting options/parameters.

    Many common formatting scenarios can be satisfied by applying a single 'named style' option.
    However, usage scenarios with atypical and/or inflexible formatting requirements can instead
    use the low-level formatting options to achieve a wide variety of customized formats.

    Note that the 'named' format styles are mutually exclusive (with the other named styles
    and in many cases also with the various low-level formatting options).
    Usually, only a single 'named style' option will be used (i.e. with no other options),
    or else 1+ 'low-level' formatting options will be used (i.e. with no 'named style' options).
    When 'conflicting' options are used simultaneously, the tool will usually ignore the conflicts and do its best.
    E.g. If you use both the 'pretty' and 'compact' options simultaneously, it will ignore one of those two options.

    See the docs of the json.dumps() function (in python's built-in json module) for additional details
    about the various low-level formatting options.
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
        # json_utils.loads_ordered(s)
        data = json_utils.load_ordered(f)
        if style == 'lines':
            if len(data) != 1:
                raise ValueError('"lines" style requires that the input must contain a single root element.')
            root = data.keys()[0]
            header = '{"%s": [\n' % root
            child_line_separator = '\n,\n'
            footer = ']}'  # '\n]}'
            click.echo(header)
            lines = [json.dumps(child, indent=None, separators=(',', ':')) for child in data[root]]
            click.echo(child_line_separator.join(lines))
            click.echo(footer)
        else:
            s = json.dumps(data, skipkeys=skip_keys, sort_keys=sort_keys,
                           ensure_ascii=ensure_ascii, check_circular=check_circular,
                           allow_nan=allow_nan, indent=indent, separators=separators)
            click.echo(s)


@cli.command(name='flatten', short_help='flattens deeply nested JSON input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input."
                   " Or '-' to use stdin (e.g. piped input).")
@click.option('--separator', '-s', type=click.STRING, help='the key/element separator. Default is "__".')
@click.option('--sort-keys', '--sorted/--unsorted', '--sort', 'sort_keys', default=False,
              help='causes the keys of each element to be output in sorted order.')
@click.option('--compact', '-c', 'style', flag_value='compact',
              help='output format style that minimizes the output.'
                   ' for more options, use the jsontool.format command.')
@click.option('--pretty', '-p', 'style', flag_value='pretty',
              help='output format style that generates human readable output.'
                   ' for more options, use the jsontool.format command.')
@click.option('--flat', '-f', 'style', flag_value='flat',
              help='output format style that generates multi-line, non-indented output.'
                   ' for more options, use the jsontool.format command.')
def flattencommand(input, separator, sort_keys, style, **kwargs):
    """
    Flattens JSON input with nested or hierarchical structure into a flat (depth 1) hierarchy. Requires valid input.

    Examples:

        \b
        Example: Basic usage:
        $ echo '{"a":{"b":null,"c":"null","d":"","e":{"f":null},"g":{},"h":[]}}' | python jsontool.py flatten -c
        {"a__b":null,"a__c":"null","a__d":"","a__e__f":null,"a__h":[]}
    """
    if style == 'compact':
        dumps_separators = (',', ':')
        dumps_indent = None
    elif style == 'pretty':
        dumps_separators = None
        dumps_indent = 2
    elif style == 'flat':
        dumps_separators = (',', ': ')
        dumps_indent = 0
    else:
        dumps_separators = None
        dumps_indent = None

    if not input:
        input = '-'
    if separator is None:
        separator = '__'
    with click.open_file(input, mode='rb') as f:
        data = json_utils.load_ordered(f)
        data = flatten(data, separator)
        s = json.dumps(data, indent=dumps_indent, separators=dumps_separators, sort_keys=sort_keys)
        click.echo(s)


@cli.command(short_help='removes portions of the input')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input."
                   " Or '-' to use stdin (e.g. piped input).")
@click.option('--null', '-n', 'prune_null', is_flag=True, type=click.BOOL,
              help='removes elements with null values.')
# @click.option('--empty', '-e', 'prune_empty', is_flag=True, type=click.BOOL, default=True,
#               help='removes elements with empty values.')
# @click.option('--trim', '-t', 'trim', type=click.BOOL,
#               help='trims leading and trailing whitespace from all string values.')
@click.option('--compact', '-c', 'style', flag_value='compact',
              help='output format style that minimizes the output.'
                   ' for more options, use the jsontool.format command.')
@click.option('--pretty', '-p', 'style', flag_value='pretty',
              help='output format style that generates human readable output.'
                   ' for more options, use the jsontool.format command.')
@click.option('--flat', '-f', 'style', flag_value='flat',
              help='output format style that generates multi-line, non-indented output.'
                   ' for more options, use the jsontool.format command.')
def strip(input, prune_null, style, **kwargs):
    """
    Removes specified portions of data from the input. Requires valid input.

    Examples:

        \b
        Example: Remove all elements with value=null:
        $ echo '{"a":{"b":null,"c":"null","d":"","e":{"f":null},"g":{},"h":[]}}' | python jsontool.py strip -n
        {"a": {"c": "null", "d": "", "e": {}, "g": {}, "h": []}}
    """
    if style == 'compact':
        dumps_separators = (',', ':')
        dumps_indent = None
    elif style == 'pretty':
        dumps_separators = None
        dumps_indent = 2
    elif style == 'flat':
        dumps_separators = (',', ': ')
        dumps_indent = 0
    else:
        dumps_separators = None
        dumps_indent = None

    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = json_utils.load_ordered(f)
        if prune_null:
            data = filter_none_values(data, recursive=True)
        s = json.dumps(data, indent=dumps_indent, separators=dumps_separators)
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
