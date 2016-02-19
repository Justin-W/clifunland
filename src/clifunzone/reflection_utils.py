from collections import MutableMapping

def is_file_like(obj):
    """
    Indicates whether a specified value is a 'file-like' object.

    :param obj: the object/value.
    :return:

    >>> is_file_like(None)
    False

    >>> is_file_like(1)
    False

    >>> is_file_like('')
    False

    >>> is_file_like('abc')
    False

    >>> is_file_like([1, 2])
    False

    >>> is_file_like((1, 2))
    False

    >>> is_file_like(set((1, 2)))
    False

    >>> is_file_like({1: 2})
    False

    >>> from collections import OrderedDict as od; is_file_like(od([(1, 2)]))
    False

    >>> import sys; is_file_like(sys.stdin) and is_file_like(sys.stderr) and is_file_like(sys.stdout)
    True
    """
    if obj is None:
        return False
    return hasattr(obj, 'read')


def is_dict_like(obj):
    """
    Indicates whether a specified value is a 'dict-like' object.

    :param obj: the object/value.
    :return:

    >>> is_dict_like(None)
    False

    >>> is_dict_like(1)
    False

    >>> is_dict_like('')
    False

    >>> is_dict_like('abc')
    False

    >>> is_dict_like([1, 2])
    False

    >>> is_dict_like((1, 2))
    False

    >>> is_dict_like(set((1, 2)))
    False

    >>> is_dict_like({1: 2})
    True

    >>> from collections import OrderedDict as od; is_dict_like(od([(1, 2)]))
    True

    >>> from json import loads; is_dict_like(loads('{"1": 2}'))
    True

    >>> from json import loads; is_dict_like(loads('{"1": {"2": 3"}}')[0])
    True
    """
    if obj is None:
        return False
    return isinstance(obj, MutableMapping)



def is_iterable(obj):
    """
    Indicates whether a specified value is an iterable object.

    :param obj: the object/value.
    :return:

    >>> is_iterable(None)
    False

    >>> is_iterable('')
    False

    >>> is_iterable('abc')
    False

    >>> is_iterable([])
    True

    >>> is_iterable({})
    True

    >>> import sys; is_iterable(sys.stdin) and is_iterable(sys.stderr) and is_iterable(sys.stdout)
    True
    """
    if obj is None:
        return False
    return hasattr(obj, '__iter__')


def varsdict(obj, hidden=False, callables=False):
    """
    Creates a dict of the attributes of a specified object.

    Works (unlike __builtin__.vars) even on objects without a __dict__ attribute.

    Adapted from: http://stackoverflow.com/a/31226800

    :param obj: the object/value.
    :param hidden: If True, even private and magic attributes will be included.
    :param callables: If True, even attributes that are callable will be included.
    :return: a dict.

    >>> varsdict(None) is None
    True

    >>> obj = True; sorted(varsdict(obj).items())  #doctest: +ELLIPSIS
    [('denominator', 1), ('imag', 0), ('numerator', 1), ('real', 1)]

    >>> obj = True; sorted(varsdict(obj, hidden=True).items())  #doctest: +ELLIPSIS
    [('__doc__', '...'), ('denominator', 1), ('imag', 0), ('numerator', 1), ('real', 1)]

    >>> obj = True; sorted(varsdict(obj, callables=True).items())  #doctest: +ELLIPSIS
    [('bit_length', <built-in method bit_length of bool object at 0x...>), ('conjugate', <built-in method conjugate ...

    >>> obj = True; sorted(varsdict(obj, hidden=True, callables=True).items())  #doctest: +ELLIPSIS
    [('__abs__', <method-wrapper '__abs__' of bool object at 0x...>), ('__add__', <method-wrapper '__add__' ...

    >>> obj = 1; sorted(varsdict(obj).items()); sorted(varsdict(obj, hidden=True).items())  #doctest: +ELLIPSIS
    [('denominator', 1), ('imag', 0), ('numerator', 1), ('real', 1)]
    [('__doc__', "..."), ('denominator', 1), ('imag', 0), ('numerator', 1), ('real', 1)]

    >>> obj = True; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())
    ['denominator', 'imag', 'numerator', 'real']
    ['__doc__', 'denominator', 'imag', 'numerator', 'real']

    >>> obj = ''; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())
    []
    ['__doc__']

    >>> obj = []; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())
    []
    ['__doc__', '__hash__']

    >>> obj = {}; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())  #doctest: +ELLIPSIS
    []
    ['__doc__', '__hash__']

    >>> import sys; is_file_like(sys.stdin) and is_file_like(sys.stderr) and is_file_like(sys.stdout)
    True
    """
    if obj is None:
        return None

    attribs = [n for n in dir(obj)]
    # exclude (if needed) hidden attributes by name
    attribs = [n for n in attribs if hidden or not n.startswith('_')]
    # get the actual attribute values as well (for the remaining attribute names)
    attribs = [(n, getattr(obj, n)) for n in attribs]
    # exclude (if needed) callable attributes
    attribs = [(n, v) for n, v in attribs if callables or not callable(v)]
    # convert the remaining (matching) attribute name/value pairs to a dict
    d = {n: v for n, v in attribs}

    return d


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
