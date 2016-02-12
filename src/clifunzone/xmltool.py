import click
from pprint import pformat

import xml2json

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def echo_kwargs(kwargs):
    click.echo('kwargs: %s' % kwargs)


def echo_context(ctx, depth=0):
    # if not depth:
    #     click.echo('dir(ctx): %s' % dir(ctx))
    obj = vars(ctx)
    obj = pformat(obj)
    click.echo('\nctx{d}:\n{obj}\n'.format(d=' (parent {})'.format(depth) if depth else '', obj=obj))
    if ctx.parent:
        echo_context(ctx.parent, depth=1 + depth)


def inherit_parent_params(ctx, params):
    """
    Copies specified params from the parent context into the params of the child context.

    :param ctx: a <click.core.Context> object
    :param params: an iterable of param names/keys
    """
    for k in params:
        ctx.params[k] = ctx.parent.params[k]


def process(**kwargs):
    ctx = click.get_current_context()

    # debug_ = ctx.params.get('debug') or ctx.parent.params.get('debug') if ctx.parent else False
    # if debug_:
    #     echo_context(ctx)

    inherit_parent_params(ctx, ('debug',))

    debug_ = ctx.params['debug']

    if debug_:
        click.echo('Debug mode: %s' % ('enabled' if debug_ else 'disabled'))
        echo_context(ctx)
        echo_kwargs(kwargs)

    subcommand = ctx.invoked_subcommand
    if subcommand == 'info':
        pass


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
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
@click.argument('input', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(exists=False), help='the path to the output file')
@click.option('--encoding', '-e', type=click.Choice(['json', 'xml']), default='json',
              help='the encoding format to use for the output')
@click.option('--verbose', '-v', is_flag=True, help='verbose mode')
@click.option('--ini', '-i', type=click.Path(exists=True), help='the path to the INI file')
def convert(**kwargs):
    """
    Reformat the input.
    """
    process(**kwargs)


@cli.command()
@click.argument('input', type=click.Path(exists=True, dir_okay=False))
# @click.argument('input', type=click.File('rb'))
def info(input, **kwargs):
    """
    Report various info about the input.
    """
    # process(**kwargs)
    # from xml.dom.minidom import parse, parseString
    # dom1 = parse('c:\\temp\\mydata.xml') # parse an XML file by name
    # datasource = open('c:\\temp\\mydata.xml')
    # dom2 = parse(datasource)   # parse an open file
    # dom3 = parseString('<myxml>Some data<empty/> some more data</myxml>')
    from xml.dom.minidom import parse
    dom = parse(input)
    click.echo('\nINFO about:\n{}\n'.format(input))
    echo_dom(dom)


@cli.command()
@click.argument('input', type=click.Path(exists=True, dir_okay=False))
# @click.argument('input', type=click.File('rb'))
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
@click.option('--echo', '-e', is_flag=True, default=False, help='echo input')
@click.option('--stripwhitespace', '-sws', is_flag=True, default=False)
@click.option('--stripnamespace', '-sns', is_flag=True, default=False)
def tojson(input, pretty, echo, stripwhitespace, stripnamespace, **kwargs):
    """
    Converts the XML input to JSON output.
    """
    # output = xml2json.json2xml(input)

    from collections import namedtuple
    Xml2JsonOptions = namedtuple('Xml2JsonOptions', ['pretty'], verbose=False)
    options = Xml2JsonOptions(pretty=pretty)

    with open(input, mode='rb') as f:
        xmlstring = f.read()
        if echo:
            click.echo('\nXML:')
            click.echo(xmlstring)
            click.echo('\nJSON:')
        output = xml2json.xml2json(xmlstring, options=options, strip_ns=stripnamespace, strip=stripwhitespace)
    # output = xml2json.elem2json(dom, options=options, strip_ns=None, strip=None)
    # click.echo('\nJSON:\n{}\n'.format(output))
    click.echo(output)


@cli.command()
@click.argument('input', type=click.Path(exists=True, dir_okay=False))
def echo(input, **kwargs):
    """
    Echo the input.
    """
    with open(input, mode='rb') as f:
        xmlstring = f.read()
        click.echo(xmlstring)


def echo_dom(dom):
    # if not depth:
    #     click.echo('dir(ctx): %s' % dir(ctx))
    obj = vars(dom)
    obj = pformat(obj)
    click.echo('\nvars(dom):\n{obj}\n'.format(obj=obj))

    obj = vars(dom)
    obj = pformat(obj)
    click.echo('\ndom content:\n{content}\n'.format(content=dom))


def main():
    cli()


if __name__ == '__main__':
    # main(default_map={
    #     'info': {
    #         'input': 'rfxml_parse.input.01.xml'
    #     }
    # })
    main()
