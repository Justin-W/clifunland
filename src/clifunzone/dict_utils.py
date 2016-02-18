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
    print 'All (non-doctest) tests PASSED.'


if __name__ == "__main__":
    main()
