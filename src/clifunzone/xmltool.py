import json
import sys
from pprint import pformat

import click

import click_utils
import xml_utils
from reflection_utils import varsdict

try:
    from lxml import etree as ET
except ImportError:
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET


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
    Provides CLI commands for interacting with XML data/files.
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


@cli.command()
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
        b = xml_utils.contains_valid_xml(f)
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
    Provides info about the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        data = xml_utils.load(f)
        d = {
            'length': len(data),
            'tag': data.tag
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


# @cli.command()
# @click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
#               help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
# def dominfo(input, **kwargs):
#     """
#     Provides info about the input.
#     """
#     if not input:
#         input = '-'
#     with click.open_file(input, mode='rb') as f:
#         # process(**kwargs)
#         # from xml.dom.minidom import parse, parseString
#         # dom1 = parse('c:\\temp\\mydata.xml') # parse an XML file by name
#         # datasource = open('c:\\temp\\mydata.xml')
#         # dom2 = parse(datasource)   # parse an open file
#         # dom3 = parseString('<myxml>Some data<empty/> some more data</myxml>')
#         from xml.dom.minidom import parse
#         dom = parse(f)
#         click.echo('\nINFO about:\n{}\n'.format(input))
#         obj = vars(dom)
#         obj = pformat(obj)
#         click.echo('\nvars(dom):\n{obj}\n'.format(obj=obj))
#         click.echo('\ndom content:\n{content}\n'.format(content=dom))


# @cli.command()
# @click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
#               help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
# @click.option('--output', '-o', type=click.Path(exists=False), help='the path to the output file')
# @click.option('--encoding', '-e', type=click.Choice(['json', 'xml']), default='json',
#               help='the encoding format to use for the output')
# @click.option('--verbose', '-v', is_flag=True, help='verbose mode')
# @click.option('--ini', '-i', type=click.Path(exists=True), help='the path to the INI file')
# def convert(**kwargs):
#     """
#     Reformat the input.
#     """
#     process(**kwargs)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
# @click.argument('input', type=click.File('rb'))
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
@click.option('--echo', '-e', is_flag=True, default=False, help='echo input')
@click.option('--stripwhitespace', '-sws', 'strip_whitespace', is_flag=True, default=False,
              help='causes unimportant whitespaces to be ignored.')
@click.option('--stripnamespace', '-sns', 'strip_namespace', is_flag=True, default=False,
              help='causes XML namespaces to be ignored.')
@click.option('--stripattribute', '-sa', 'strip_attribute', is_flag=True, default=False,
              help='causes XML attributes to be ignored.')
def tojson(input, pretty, echo, strip_whitespace, strip_namespace, strip_attribute, **kwargs):
    """
    Converts the XML input to JSON output.
    """
    # output = xml2json.json2xml(input)

    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        xmlstring = f.read()
        if echo:
            click.echo('\nXML:')
            click.echo(xmlstring)
            click.echo('\nJSON:')
    output = xml_utils.xml_to_json(xmlstring, strip_whitespace=strip_whitespace, strip_namespace=strip_namespace,
                                   strip_attribute=strip_attribute, pretty=pretty)
    # output = xml2json.elem2json(dom, options=options, strip_ns=None, strip=None)
    # click.echo('\nJSON:\n{}\n'.format(output))
    click.echo(output)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
def elements(input, pretty, **kwargs):
    """
    Extracts information about the elements (i.e. tags) from the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        tag = None  # 'div' or whatever
        items = root.iter(tag=tag) if tag else root.iter()
        # items = [i for i in items]
        items = [xml_utils.element_info(i, tree=tree) for i in items]
        if pretty:
            output = json.dumps(items, indent=4)
            click.echo(output)
        else:
            lines = [json.dumps(i, indent=None, separators=(',', ':')) for i in items]
            for line in lines:
                click.echo(line)


def main():
    cli()


if __name__ == '__main__':
    # main(default_map={
    #     'info': {
    #         'input': 'rfxml_parse.input.01.xml'
    #     }
    # })
    main()
