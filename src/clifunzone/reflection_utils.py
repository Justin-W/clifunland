def is_file_like(obj):
    """
    Indicates whether a specified value is a 'file-like' object.

    :param obj: the object/value.
    :return:

    >>> is_file_like(None)
    False

    >>> is_file_like('')
    False

    >>> is_file_like('abc')
    False

    >>> is_file_like([])
    False

    >>> is_file_like({})
    False

    >>> import sys; is_file_like(sys.stdin) and is_file_like(sys.stderr) and is_file_like(sys.stdout)
    True
    """
    if obj is None:
        return False
    return hasattr(obj, 'read')


def varsdict(obj, hidden=False):
    """
    Creates a dict of the attributes of a specified object.

    Works (unlike __builtin__.vars) even on objects without a __dict__ attribute.

    :param obj: the object/value.
    :param hidden: If True, even private and magic attributes will be included.
    :return: a dict.

    >>> varsdict(None) is None
    True

    >>> obj = True; sorted(varsdict(obj).items()); sorted(varsdict(obj, hidden=True).items())  #doctest: +ELLIPSIS
    [('bit_length', <built-in method bit_length of bool object at 0x...>), ('conjugate', <built-in method conjugate ...
    [('__abs__', <method-wrapper '__abs__' of bool object at 0x...>), ('__add__', <method-wrapper '__add__' of ...

    >>> obj = 1; sorted(varsdict(obj).items()); sorted(varsdict(obj, hidden=True).items())  #doctest: +ELLIPSIS
    [('bit_length', <built-in method bit_length of int object at 0x...>), ('conjugate', <built-in method conjugate ...
    [('__abs__', <method-wrapper '__abs__' of int object at 0x...>), ('__add__', <method-wrapper '__add__' of int ...

    >>> obj = True; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())  #doctest: +ELLIPSIS
    ['bit_length', 'conjugate', 'denominator', 'imag', 'numerator', 'real']
    ['__abs__', '__add__', '__and__', '__class__', '__cmp__', '__coerce__', '__delattr__', '__div__', '__divmod__', ...

    >>> obj = ''; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())  #doctest: +ELLIPSIS
    ['capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', ...
    ['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', ...

    >>> obj = []; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())  #doctest: +ELLIPSIS
    ['append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
    ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', ...

    >>> obj = {}; sorted(varsdict(obj).keys()); sorted(varsdict(obj, hidden=True).keys())  #doctest: +ELLIPSIS
    ['clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', ...
    ['__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', ...

    >>> import sys; is_file_like(sys.stdin) and is_file_like(sys.stderr) and is_file_like(sys.stdout)
    True
    """
    if obj is None:
        return None
    # d = dict([attr, getattr(obj, attr)] for attr in dir(obj) if hidden or not attr.startswith('_'))
    d = {attr: getattr(obj, attr) for attr in dir(obj) if hidden or not attr.startswith('_')}
    return d


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
