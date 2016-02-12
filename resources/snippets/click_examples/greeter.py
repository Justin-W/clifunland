import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def greeter(**kwargs):
    name_ = kwargs['name']
    transformation = kwargs.get('transformation')
    if transformation == 'upper':
        name_ = name_.upper()
    elif transformation == 'lower':
        name_ = name_.lower()
    elif transformation == 'title':
        name_ = name_.title()
    elif transformation == 'reverse':
        name_ = name_[::-1]
    output = '{0}, {1}'.format(kwargs['greeting'], name_)
    if kwargs['caps']:
        output = output.upper()
    if kwargs.get('shout') or kwargs.get('emphasis'):
        output += '!!!!'
    else:
        output += '.'
    print(output)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def greet():
    pass


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
@click.option('--unchanged', 'transformation', flag_value='', default=True)
@click.option('--upper', 'transformation', flag_value='upper')
@click.option('--lower', 'transformation', flag_value='lower')
@click.option('--title', 'transformation', flag_value='title')
@click.option('--reverse', 'transformation', flag_value='reverse')
@click.option('--shout/--no-shout', default=False, help='enable/disable emphatic output')
def hello(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye', help='word to use for the greeting')
@click.option('--caps', is_flag=True, help='uppercase the output')
@click.option('--emphasis/--no-emphasis', default=False, help='enable/disable emphatic output')
def goodbye(**kwargs):
    greeter(**kwargs)


if __name__ == '__main__':
    greet()
