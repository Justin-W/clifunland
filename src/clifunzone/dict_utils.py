from collections import OrderedDict, MutableMapping


def flatten(d, separator='_', parent_key=None):
    """
    Converts a nested hierarchy of key/value object (e.g. a dict of dicts) into a flat (i.e. non-nested) dict.

    :param d: the dict (or any other instance of collections.MutableMapping) to be flattened.
    :param separator: the separator to use when concatenating nested key names into flattened key names.
    :param parent_key: used internally for recursion.
    :return: a flattened dict (i.e. containing no nested dicts as values).
    """
    if separator is None:
        separator = '_'
    if parent_key is None:
        parent_key = ''

    dict_type = dict if d is None else type(d)

    items = []
    for k, v in d.items():
        new_key = parent_key + separator + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, separator=separator, parent_key=new_key).items())
        else:
            items.append((new_key, v))
    return dict_type(items)


def format_keys(d, format_string):
    """
    Creates a new dict with all keys from an original dict reformatted/mapped.

    :param d: a dict.
    :param format_string: a normal python format string (i.e. str().format() style).
    :return: a new dict (of the same type as the original) containing the original dict's values,
        but with each key reformatted (as a string).

    >>> format_keys({'a': 1, 'b': 2}, '#{}:')
    {'#b:': 2, '#a:': 1}

    >>> format_keys(OrderedDict([('a',  1), ('z',  26)]), 'K={}.')
    OrderedDict([('K=a.', 1), ('K=z.', 26)])
    """
    dict_type = type(d)
    d = dict_type([(format_string.format(k), v) for k, v in d.items()])
    return d


def filter_none_values(d, recursive=True):
    """
    Returns a filtered copy of a dict, with all keys associated with 'None' values removed.

    adapted from: http://stackoverflow.com/q/20558699
    adapted from: http://stackoverflow.com/a/20558778

    :param d: a dict-like object.
    :param recursive: If True, performs the operation recursively on inner elements of the object.
    :return:

    >>> filter_none_values(None) is None
    True

    >>> filter_none_values(1)
    Traceback (most recent call last):
    TypeError: d is not a dict-like object.

    >>> filter_none_values({})
    {}

    >>> filter_none_values({'a': 1, 'b': None, 'c': '3'})
    {'a': 1, 'c': '3'}

    >>> filter_none_values({'a': 1, 'b': [1, None, 3], 'c': '3'})
    {'a': 1, 'c': '3', 'b': [1, 3]}

    >>> filter_none_values({'a': 1, 'b': [1, {'ba': 1, 'bb': None, 'bc': '3'}, 3], 'c': '3'})
    {'a': 1, 'c': '3', 'b': [1, {'ba': 1, 'bc': '3'}, 3]}

    >>> from collections import OrderedDict as od; filter_none_values(od((('a', 1), ('b', None), ('c', '3'))))
    OrderedDict([('a', 1), ('c', '3')])

    >>> from collections import OrderedDict as od; filter_none_values({'r': od((('a', 1), ('b', None), ('c', '3')))})
    {'r': OrderedDict([('a', 1), ('c', '3')])}

    >>> from json import loads; repr(filter_none_values(loads('{"a": 1, "b": null, "c": 3}')))
    "{u'a': 1, u'c': 3}"

    >>> from json import loads; repr(filter_none_values(loads('{"a": 1, "b": [], "c": 3}')))
    "{u'a': 1, u'c': 3, u'b': []}"

    >>> from json import loads; repr(filter_none_values(loads('{"a": 1, "b": {"ba": null}, "c": 3}')))
    "{u'a': 1, u'c': 3, u'b': {}}"

    >>> from json import loads; repr(filter_none_values(loads('{"a": 1, "b": {"ba": []}, "c": 3}')))
    "{u'a': 1, u'c': 3, u'b': {u'ba': []}}"

    >>> from json import loads; repr(filter_none_values(loads('{"a": 1, "b": {"ba": {"baa": null}}, "c": 3}')))
    "{u'a': 1, u'c': 3, u'b': {u'ba': {}}}"
    """

    def remove_none(obj):
        """Note: This one seems to be functionally equivalent to purify (at least for the cases I tested)."""
        if isinstance(obj, (list, tuple, set)):
            return type(obj)(remove_none(x) for x in obj if x is not None)
        elif isinstance(obj, dict):
            return type(obj)((remove_none(k), remove_none(v))
                             for k, v in obj.items() if k is not None and v is not None)
        else:
            return obj

    def purify(o):
        """Note: This one seems to be functionally equivalent to remove_none (at least for the cases I tested)."""
        if hasattr(o, 'items'):
            oo = type(o)()
            for k in o:
                if k is not None and o[k] is not None:
                    oo[k] = purify(o[k])
        elif hasattr(o, '__iter__'):
            oo = []
            for it in o:
                if it is not None:
                    oo.append(purify(it))
        else:
            return o
        return type(o)(oo)

    def strip_none(data):
        """Note: This one doesn't support OrderedDict, etc."""
        if isinstance(data, dict):
            return {k: strip_none(v) for k, v in data.items() if k is not None and v is not None}
        elif isinstance(data, list):
            return [strip_none(item) for item in data if item is not None]
        elif isinstance(data, tuple):
            return tuple(strip_none(item) for item in data if item is not None)
        elif isinstance(data, set):
            return {strip_none(item) for item in data if item is not None}
        else:
            return data

    if d is None:
        return None
    elif not hasattr(d, 'items'):
        raise TypeError('d is not a dict-like object.')

    if recursive:
        return remove_none(d)
        # return purify(d)
        # return strip_none(d)
    else:
        d = d.copy()
        # remove all keys
        bad_keys = [k for k, v in d.items() if v is None]
        for k in bad_keys:
            d.pop(k)
        return d


def _test_flatten(expected_value, d, separator=None):
    flattened = flatten(d, separator=separator)
    # print 'before:\t\t{}\nflattened:\t{}'.format(d, flattened)
    assert repr(flattened) == expected_value, 'repr(flatten(d)) != expected_value. expected_value={}; actual_value={}, d={}, separator={}.'.format(expected_value, flattened, d, separator)  # noqa


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))

    _test_flatten("{'a': 1, 'c_a': 2, 'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}",
                  {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y': 10}}, 'd': [1, 2, 3]})
    _test_flatten("{'a': 1, 'c_a': '2', 'c_b_x': 5, 'd': [1, 'two', 3], 'c_b_y': 10}",
                  {'a': 1, 'c': {'a': '2', 'b': {'x': 5, 'y': 10}}, 'd': [1, 'two', 3]})

    _test_flatten("OrderedDict([('a', 1), ('c_a', 2), ('c_b_x', 5), ('c_b_y', 10), ('d', [1, 2, 3])])",
                  OrderedDict([('a', 1), ('c', OrderedDict([('a', 2), ('b', OrderedDict([('x', 5), ('y', 10)]))])), ('d', [1, 2, 3])]))  # noqa
    _test_flatten("OrderedDict([('a', 1), ('c_a', '2'), ('c_b_x', 5), ('c_b_y', 10), ('d', [1, 'two', 3])])",
                  OrderedDict([('a', 1), ('c', OrderedDict([('a', '2'), ('b', OrderedDict([('x', 5), ('y', 10)]))])), ('d', [1, 'two', 3])]))  # noqa

    # _test_flatten("{'a': 1, 'c|a': '2', 'c|b|x': 5, 'd': [1, 'two', 3], 'c|b|y': 10}",
    #               {'a': 1, 'c': {'a': '2', 'b': {'x': 5, 'y': 10}}, 'd': [1, 'two', 3]}, separator='|')
    _test_flatten("{'a': 1, 'd': [1, 'two', 3], 'c|b|x': 5, 'c|a': '2', 'c|b|y': 10}",
                  {'a': 1, 'c': {'a': '2', 'b': {'x': 5, 'y': 10}}, 'd': [1, 'two', 3]}, separator='|')
    _test_flatten(
        "OrderedDict([('a', 1), ('c<~|~>a', '2'), ('c<~|~>b<~|~>x', 5), ('c<~|~>b<~|~>y', 10), ('d', [1, 'two', 3])])",
        OrderedDict([('a', 1), ('c', OrderedDict([('a', '2'), ('b', OrderedDict([('x', 5), ('y', 10)]))])), ('d', [1, 'two', 3])]), separator='<~|~>')  # noqa
    print('All (non-doctest) tests PASSED.')


if __name__ == "__main__":
    main()
