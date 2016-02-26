import sys

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
@click.argument('infile', type=click.Path(exists=True, dir_okay=False))
def echoarg1(infile, **kwargs):
    """
    Echo the input.

    infile is the file containing the input to be echoed.
    """
    with open(infile, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.argument('infile', required=False, type=click.Path(exists=True, dir_okay=False, allow_dash=True))
def echoarg2(infile, **kwargs):
    """
    Echo the input.
    """
    if not infile:
        # infile = sys.stdin
        infile = '-'
    with click.open_file(infile, mode='rb') as f:
        s = f.read()
        click.echo(s)


# NOTE: Doesn't fully work
@cli.command()
@click.argument('infile', required=False, default='-', type=click.Path(exists=True, dir_okay=False, allow_dash=True))
def echoarg2b(infile, **kwargs):
    """
    Echo the input.
    """
    with click.open_file(infile, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.argument('infile', required=False, type=click.File())
def echoarg3(infile, **kwargs):
    """
    Echo the input.
    """
    with infile or sys.stdin as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.option('--infile', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input to be echoed. Or '-' to use stdin (e.g. piped input).")
def echoopt1(infile, **kwargs):
    """
    Echo the input.
    """
    if not infile:
        # infile = sys.stdin
        infile = '-'
    with click.open_file(infile, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.option('--infile', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the file containing the input to be echoed. Or '-'.")
@click.option('--intish', '-int', type=click.INT, help='a int value')
@click.option('--outfile', '-o', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the output file. Or '-'.")
@click.option('--logfile', '-l', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              help="the path to the log file. Or '-'.")
@click.option('--boolish', '-boo', type=click.BOOL, help='a bool value')
@click.option('--floatish', '-flt', type=click.FLOAT, help='a float value')
def echoopt2(infile, **kwargs):
    """
    Echo the input.
    """
    with click.open_file(infile, mode='rb') if infile else sys.stdin as f:
        s = f.read()
        click.echo(s)


# NOTE: Doesn't fully work
@cli.command()
@click.option('--infile', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True),
              default='-',
              help="the path to the file containing the input to be echoed. Or '-'.")
def echoopt2b(infile, **kwargs):
    """
    Echo the input.
    """
    with click.open_file(infile, mode='rb') as f:
        s = f.read()
        click.echo(s)


@cli.command()
@click.option('--infile', '-i', type=click.Path(exists=True, dir_okay=False, allow_dash=True))
def echoopt3(infile, **kwargs):
    """
    Echo the input.
    """
    if infile:
        with click.open_file(infile, mode='rb') as f:
            s = f.read()
            click.echo(s)
    else:
        with sys.stdin as f:
            s = f.read()
            click.echo(s)


@cli.command()
@click.option('--infile', '-i', required=False, type=click.File())
def echoopt4(infile, **kwargs):
    """
    Echo the input.
    """
    with infile or sys.stdin as f:
        s = f.read()
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
