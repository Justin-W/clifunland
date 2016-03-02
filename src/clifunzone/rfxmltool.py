import json
import logging
from collections import OrderedDict
from pprint import pformat

import click

from clifunzone import click_utils
from clifunzone import xml_utils
from clifunzone.reflection_utils import varsdict

try:
    from lxml import etree as ET
except ImportError:
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
# import xml.etree.ElementTree as ET


def debug_context(**kwargs):
    ctx = click.get_current_context()

    # debug_ = ctx.params.get('debug') or ctx.parent.params.get('debug') if ctx.parent else False
    # if debug_:
    #     echo_context(ctx)

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
    Provides CLI commands for interacting with Robot Framework test output data/files (XML format).
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
            click.echo('I was invoked with subcommand: %s.' % subcommand)

    try:
        debug_context(**{})
    except:
        logging.exception('debug_context error')


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
        # root = xml_utils.load(f)
        tree = ET.parse(f)
        root = tree.getroot()
        d = {}
        d.update({'xml': xml_utils.element_info(root)})

        rf_metrics = {
            'suites': xml_utils.count_elements(tree, xpath='//suite'),
            'tests': xml_utils.count_elements(tree, xpath='//test'),
            'messages': xml_utils.count_elements(tree, xpath='//msg')
        }
        d.update({'robot': rf_metrics})

        if verbose:
            d['_object'] = {
                'type': type(root),
                # 'repr': repr(root),
                # 'vars': sorted(vars(root)),
                # 'dir': sorted(dir(root)),
                'members': sorted(varsdict(root).keys())
            }
        # click.echo(d)
        # click.echo(sorted(d.items()))
        if verbose:
            s = pformat(d)
        else:
            s = json.dumps(d, indent=2, sort_keys=True)
        click.echo(s)


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
@click.option('--start', type=click.INT)
@click.option('--stop', type=click.INT)
@click.option('--step', type=click.INT)
@click.option('--status', type=click.Choice(['PASS', 'FAIL']))
@click.option('--showargs', '-a', is_flag=True, default=False,
              help="display each test's args.")
@click.option('--showmsgs', '-m', is_flag=True, default=False,
              help="display each test's inner messages.")
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
def keywords(input, start, stop, step, status, showargs, showmsgs, pretty, **kwargs):
    """
    Extracts RF keywords from the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        kws = [elem for elem in root.iter(tag='kw')]
        kws = [node_to_dict(kw, showargs=showargs, showmsgs=showmsgs) for kw in kws]
        if status:
            kws = [kw for kw in kws if kw['status']['status'] == status]
        kws = kws[start:stop:step]
        if pretty:
            output = json.dumps(kws, indent=4)
            click.echo(output)
        else:
            # click.echo(json.dumps(kws))
            for kw in kws:
                kw = json.dumps(kw)
                click.echo(kw)


@cli.command(name='tests')
@click.option('--input', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input. Or '-' to use stdin (e.g. piped input).")
@click.option('--start', type=click.INT)
@click.option('--stop', type=click.INT)
@click.option('--step', type=click.INT)
@click.option('--status', type=click.Choice(['PASS', 'FAIL']))
@click.option('--showargs', '-a', is_flag=True, default=False,
              help="display each test's args.")
@click.option('--showmsgs', '-m', is_flag=True, default=False,
              help="display each test's inner messages.")
@click.option('--pretty', '-p', is_flag=True, default=False, help='pretty format')
def testscommand(input, start, stop, step, status, showargs, showmsgs, pretty, **kwargs):
    """
    Extracts RF test data from the input.
    """
    if not input:
        input = '-'
    with click.open_file(input, mode='rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        test_elements = [elem for elem in root.iter(tag='test')]
        test_elements = [node_to_dict(test_element, showargs=showargs, showmsgs=showmsgs)
                         for test_element in test_elements]
        if status:
            test_elements = [test_element for test_element in test_elements if
                             test_element['status']['status'] == status]
        test_elements = test_elements[start:stop:step]
        if pretty:
            output = json.dumps(test_elements, indent=4)
            click.echo(output)
        else:
            # click.echo(json.dumps(kws))
            for test_element in test_elements:
                test_element = json.dumps(test_element)
                click.echo(test_element)


def node_to_dict(root, showargs=False, showmsgs=False, showtags=True):
    d = OrderedDict()

    # attribs = [k for k in ['id', 'name', 'type'] if k in root.attrib]
    attribs = root.attrib.keys()
    for attrib in attribs:
        d['@' + attrib] = root.attrib[attrib]

    status = root.find('status').attrib
    if status is not None:
        if type(status) is not dict:
            # Note: if lxml is being used, status will be a non-JSON-serializable object (<type 'lxml.etree._Attrib'>).
            # Therefore, we must manually convert it to a regular dict to enable JSON serialization compatibility.
            status = {k: v for k, v in status.items()}
        d['status'] = status

    doc = root.find('doc')
    if doc is not None:
        d['doc'] = doc.text

    if showtags:
        tags = root.find('tags')
        if tags is not None:
            tags = tags.iter(tag='tag')
            tags = [tag.text for tag in tags]
        d['tags'] = tags

    if showargs:
        args = root.find('arguments')
        if args is not None:
            args = args.iter(tag='arg')
            args = [arg.text for arg in args]
        d['args'] = args

    if showmsgs:
        msgs = root.iter(tag='msg')
        if msgs is not None:
            msgs = [msg.text for msg in msgs]
        d['messages'] = msgs

    return d


def main():
    cli()


if __name__ == '__main__':
    # main(default_map={
    #     'info': {
    #         'input': 'rfxml_parse.input.01.xml'
    #     }
    # })
    main()
