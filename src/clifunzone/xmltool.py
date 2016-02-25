import click
import json
import sys
from pprint import pformat

import click_utils
import dict_utils
import xml_utils
from reflection_utils import varsdict

try:
    from lxml import etree as ET
except ImportError:
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
# import xml.etree.ElementTree as ET


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
        # root = xml_utils.load(f)
        tree = ET.parse(f)
        root = tree.getroot()
        d = {}
        d.update({'root': xml_utils.element_info(root)})
        if verbose:
            d['_object'] = {
                'type': type(root),
                # 'repr': repr(data),
                # 'vars': sorted(vars(data)),
                # 'dir': sorted(dir(data)),
                'members': sorted(varsdict(root).keys())
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
@click.option('--verbose', '-v', is_flag=True, type=click.BOOL,
              help='enables more detailed output.')
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
def elements(input, verbose, pretty, **kwargs):
    """
    Prints information about each element (i.e. tag) in the input.

    Examples:

        \b
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py elements | tail -n 1
        {"path":"/a/b[2]/d","content":{"tag":"d"}}

        \b
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py elements | head -n 1
        {"path":"/a","content":{"tag":"a"},"metrics":{"children":{"count":2,"tags":["b"]},\\
        "descendants":{"count":6,"tags":["b","c","d","e"]}}}
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
        if not verbose:
            # remove 'noise' from the data output to make it more understandable/readable/concise
            # items = [dict_utils.map_values(i, lambda v: '' if v == '\n' else v) for i in items]
            items = [dict_utils.remove_if(i, lambda k, v: v == '\n', output=True) for i in items]
            items = [dict_utils.remove_if(i, lambda k, v: v == '', output=True) for i in items]
            items = [dict_utils.remove_if(i, lambda k, v: v is None, output=True) for i in items]
            items = [dict_utils.remove_if(i, lambda k, v: v == [], output=True) for i in items]
            items = [dict_utils.remove_if(i, lambda k, v: v == {}, output=True) for i in items]
            # items = [dict_utils.filter_none_values(i) for i in items]
            # items = [dict_utils.filter_empty_values(i) for i in items]
        if pretty:
            output = json.dumps(items, indent=4)
            click.echo(output)
        else:
            lines = [json.dumps(i, indent=None, separators=(',', ':')) for i in items]
            for line in lines:
                click.echo(line)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--whitespace', '-w', is_flag=True, type=click.BOOL,
              help='removes any leading/trailing whitespace.')
@click.option('--empty', '-e', is_flag=True, type=click.BOOL,
              help='removes all empty elements.')
@click.option('--xpath', '-x', 'xpaths', type=click.STRING, multiple=True,
              help='removes all elements matching a given XPath expression.'
                   ' Repeatable. (Can be specified multiple times.)')
@click.option('--tag', '-t', 'tags', type=click.STRING, multiple=True,
              help='removes all elements with the specified tag.'
                   ' Repeatable. (Can be specified multiple times.)')
@click.option('--attribute', '--attrib', '-a', 'attributes', type=click.STRING, multiple=True,
              help='removes all attributes with the specified name from all elements.'
                   ' Repeatable. (Can be specified multiple times.)')
@click.option('--attribute-value', '-av', 'attribute_values', type=click.STRING, multiple=True,
              help='removes all attributes with the specified name from all elements.'
                   ' Repeatable. (Can be specified multiple times.)')
@click.option('--empty-attributes', '-ea', 'empty_attributes', is_flag=True, type=click.BOOL,
              help='removes all attributes with empty values from all elements.')
@click.option('--all-attributes', 'all_attributes', is_flag=True, type=click.BOOL,
              help='removes all attributes from all elements.')
@click.option('--all-text', 'all_text', is_flag=True, type=click.BOOL,
              help='removes all text content from all elements.')
def strip(input, whitespace, empty, xpaths, tags, attributes, attribute_values, empty_attributes, all_attributes,
          all_text, **kwargs):
    """
    Removes specified portions of XML data from the input.

    This command can be used to simplify complex data (by discarding specific portions of it).
    Such simplification might be used (for example) as part of an interactive data analysis process.

    Examples:

        \b
        Example: Remove all d tags that are direct children of b tags:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py strip -x "//b/d"
        <a><b><c/></b><b/></a>
    """

    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        parser = None
        if whitespace:
            try:
                parser = ET.XMLParser(remove_blank_text=True)
            except TypeError:
                # TypeError: __init__() got an unexpected keyword argument 'remove_blank_text'
                # lxml not imported?
                pass
        if parser:
            tree = ET.parse(f, parser=parser)
        else:
            tree = ET.parse(f)
        root = tree.getroot()
        # import reflection_utils
        # click.echo('tree: %s' % reflection_utils.varsdict(tree))
        # click.echo('tree: %s' % dir(tree))
        # click.echo('root: %s' % reflection_utils.varsdict(root))
        # click.echo('root: %s' % dir(root))

        if tags:
            # convert each tag to an xpath
            if not xpaths:
                xpaths = []
            xpaths += ['//{tag}'.format(tag=s) for s in tags]
        for xpath in xpaths:
            xml_utils.remove_elements(root, xpath=xpath)
        if all_attributes:
            for i in [i for i in root.iter() if i.attrib]:
                i.attrib.clear()
        else:
            if empty_attributes:
                xml_utils.remove_attributes_with_empty_value(root)
            if attributes:
                for attrib_name in attributes:
                    xml_utils.remove_attributes_with_name(root, attrib_name)
            if attribute_values:
                for attrib_value in attribute_values:
                    xml_utils.remove_attributes_with_value(root, attrib_value)
        if all_text:
            for i in [i for i in root.iter() if i.text]:
                i.text = ''
        if whitespace:
            for i in [i for i in root.iter() if i.text]:
                i.text = i.text.strip()
        if empty:
            # Note: the repeat flag will cause elements that become empty (as a result of removal of empty children)
            # to be subsequently detected as empty and removed.
            repeat = True
            while repeat:
                repeat = False  # stop unless a removal occurs
                for parent in [i for i in root.iter() if xml_utils.is_parent_element(i)]:
                    for child in [i for i in xml_utils.get_elements(parent, xpath='./*')
                                  if xml_utils.is_empty_element(i)]:
                        repeat = True
                        parent.remove(child)
        # output = ET.tostring(root, method='text')
        output = ET.tostring(root)
        click.echo(output)


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--xpath', '-x', type=click.STRING,
              help='removes all elements matching a given XPath expression.')
@click.option('--root', '-r', 'root_tag', default='results',
              help='a tag to use as the root element of the output.'
                   ' if not specified and multiple matches are found, the output may not be valid XML.')
@click.option('--no-root', '-nr', 'no_root', is_flag=True, type=click.BOOL,
              help='prevents the root tag from being added to the output.')
def find(input, xpath, root_tag, no_root, **kwargs):
    """
    Extracts specified portions of XML data from the input.

    This command can be used to extract a data subset from within more complex data.

    Note: The ElementTree package (Python builtin) has limited XPath support.
    Therefore, some of the examples below will only work if the lxml package is used (instead of ElementTree).

    Examples:

        \b
        Example: Find all b elements:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//b' -nr
        <b><c/></b>
        <b><d><e/></d><d/></b>

        \b
        Example: Find the 1st b element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//b[1]' -nr
        <b><c/></b>

        \b
        Example: Find the 2nd b element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//b[2]' -nr
        <b><d><e/></d><d/></b>

        \b
        Example: Find the last b element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//b[last()]' -nr
        <b><d><e/></d><d/></b>

        \b
        Example: Find all e elements that are a child of a d element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//d/e' -nr
        <e/>

        \b
        Example: Find all d elements with a child e element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//d/e/parent::*' -nr
        <d><e/></d>

        \b
        Example: Find all d elements with a child e element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//d/e/parent::*' -nr
        <d><e/></d>

        \b
        Example: Find all elements with exactly 1 inner element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//*[count(*)=1]' -nr
        <b><c/></b>
        <d><e/></d>

        \b
        Example: Find all elements with exactly 2+ inner elements:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//*[count(*)>=2]' -nr
        <a><b><c/></b><b><d><e/></d><d/></b></a>
        <b><d><e/></d><d/></b>

        \b
        Example: Find all elements with 1 child element:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//*[count(/*)=1]' -nr
        <b><c/></b>
        <d><e/></d>

        \b
        Example: Find all elements with 1 inner element with tag c:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//*[count(./c)=1]' -nr
        <b><c/></b>

        \b
        Example: Find all elements with 1 inner element with either the c OR e tag:
        $ echo '<a><b><c/></b><b><d><e/></d><d/></b></a>' | python xmltool.py find -x '//*[count(./c|./e)=1]' -nr
        <b><c/></b>
        <d><e/></d>

        \b
        Example: Find all b elements with attribute @z=1:
        $ echo '<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>' | \\
        python xmltool.py find -x '//b[@z="1"]' -nr
        <b z="1"><c/></b>

        \b
        Example: Find all elements with attribute @z=1:
        $ echo '<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>' | \\
        python xmltool.py find -x '//*[@z="1"]' -nr
        <b z="1"><c/></b>
        <e z="1"/>

        \b
        Example: Find all elements with attribute @z except those with @z=2:
        $ echo '<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>' | \\
          python xmltool.py find -x '//*[@z and @z!="2"]' -nr
        <b z="1"><c/></b>
        <d z="1"><e z="2"/></d>

        \b
        Example: Find all elements with attribute @z=1 and a node position greater than 2:
        $ echo '<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>' | \\
          python xmltool.py find -x '//*[@z="1" and position()>2]' -nr
        <d z="1"><e z="2"/></d>

        \b
        Example: Find all elements with text that contains "3":
        $ echo '<z><a>1a1</a><b>2b1</b><c>3c1</c><a>4a2</a><b>5b2</b><c>6c2</c><a>7a3</a></z>' | \\
          python xmltool.py find -x '//*[contains(text(),"3")]' -nr
        <c>3c1</c>
        <a>7a3</a>
    """

    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        if xpath:
            elements = xml_utils.get_elements(root, xpath=xpath)
        else:
            elements = []
        # output = ET.tostring(root, method='text')
        if no_root:
            root_tag = None
        if root_tag:
            header = '<%s>' % root_tag
            footer = '</%s>' % root_tag
        else:
            header, footer = None, None

        if header:
            click.echo(header)
        for i in elements:
            output = ET.tostring(i)
            click.echo(output)
        if footer:
            click.echo(footer)


def main():
    cli()


if __name__ == '__main__':
    # main(default_map={
    #     'info': {
    #         'input': 'rfxml_parse.input.01.xml'
    #     }
    # })
    main()
