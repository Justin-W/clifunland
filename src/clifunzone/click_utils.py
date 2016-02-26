from pprint import pformat

import click

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

# def main():
#     cli()
#
#
# if __name__ == '__main__':
#     main()
