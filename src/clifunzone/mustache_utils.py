import pystache


def render(template, *context, **kwargs):
    """
    Renders a mustache template.

    Uses (and depends on) the pystache package.

    :param template: the mustache template
    :param context: positional params
    :param kwargs: kwarg params
    :return: a string

    >>> render('{{greeting}} {{person}}!', **{'person': 'Mom', 'greeting': 'Hi'})
    u'Hi Mom!'

    >>> render('{{g}} {{p}}!', p='Mom', g='Hey')
    u'Hey Mom!'

    >>> render('{{g.informal}} {{p}}!', **{'p': 'Mom', 'g': {'informal': 'Hi', 'formal': 'Hello'}})
    u'Hi Mom!'

    >>> render('{{g.formal}} {{p}}!', **{'p': 'Mom', 'g': {'informal': 'Hi', 'formal': 'Hello'}})
    u'Hello Mom!'

    >>> render('{{g.f}} {{p}}!', p='Mom', g={'i': 'Hi', 'f': 'Hello'}, **{'g': {'i': 'hi', 'f': 'hello'}})
    Traceback (most recent call last):
    TypeError: render() got multiple values for keyword argument 'g'

    >>> render('{{g.f}} {{p}}!', p='Mom', g={'i': 'Hi', 'f': 'Hello'})
    u'Hello Mom!'

    >>> render('{{g.f}} {{p}}!', p='Mom', **{'g': {'i': 'hi', 'f': 'hello'}})
    u'hello Mom!'
    """
    return pystache.render(template, *context, **kwargs)


# def render_file(template_filepath, *context, **kwargs):
#     if not file:
#         raise ValueError("Missing or invalid parameter: filepath.")
#     with open(template_filepath, mode='rU') as template_file:
#         template = template_file.read()  # .replace('\\n', '\n')
#
#     return render(template, context, kwargs)


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
