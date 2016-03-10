from collections import Mapping
from collections import OrderedDict  # noqa
from collections import Sequence
from collections import Set
from collections import defaultdict  # noqa

# See objwalk() function's docstring
# See: https://gist.github.com/sente/1480558
try:
    from six import string_types, iteritems
except ImportError:
    string_types = (str, unicode) if str is bytes else (str, bytes)  # noqa
    # iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()

    def iteritems(mapping):
        return getattr(mapping, 'iteritems', mapping.items)()

__all__ = ['walk_items']


def nested_dict_iter(nested):
    """
    See: http://stackoverflow.com/a/10756615

    >>> list(nested_dict_iter(1))
    Traceback (most recent call last):
    AttributeError: 'int' object has no attribute 'iteritems'

    >>> d = {'a': 1, 'b': {'c': 6, 'd': 7, 'g': {'h': 3, 'i': 9}}, 'e': {'f': 3}}; list(nested_dict_iter(d))  # noqa
    [('h', 3), ('g', {'i': 9, 'h': 3}), ('f', 3), ('e', {'f': 3})]
    """
    for key, value in nested.iteritems():
        if isinstance(value, Mapping):
            for inner_key, inner_value in nested_dict_iter(value):
                yield inner_key, inner_value
    else:
        yield key, value


def walk_items(obj, values_only=False, ancestors=True, keys_as_ancestors=False, obj_ancestors=(), key=None):
    """
    Recursively walks a nested object hierarchy, yielding (depth, key, value, ancestors) tuples as it walks.

    The walk is performed depth-first.

    Adapted from: https://gist.github.com/sente/1480558
    Adapted from: http://stackoverflow.com/a/32935278
    Also see: https://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    Also see: http://code.activestate.com/recipes/577982-recursively-walk-python-objects/

    :param obj: a python object.
    :param values_only: if True, then only non-collection values will be yielded.
    :param ancestors: if False, then the ancestor value will be excluded from the returned tuples.
    :param keys_as_ancestors: if True, then keys and indexes will be treated as an ancestor.
    :param obj_ancestors: the hierarchical ancestors (with the root first and direct parent last) of obj.
    :param key: the key (for Mappings) or index (for Sequences) of obj within obj's direct ancestor/parent.
    :return: (depth, key, value, ancestors) tuples.
        if obj is a Mapping, key will be a key.
        elif obj is a Sequence, key will be an index.
        the ancestors portion contains the hierarchical ancestors (e.g. root, ..., direct parent, obj) of the value.
        the depth portion indicates the number of hierarchical ancestors of the value.

    >>> d = 1; list(walk_items(d))
    [(0, None, 1, ())]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> list(walk_items(d, ancestors=False))[1:7]
    [(1, 'a', ['aa', 1]), (2, 0, 'aa'), (2, 1, 1), (1, 'c', ('ca', [3, 4])), (2, 0, 'ca'), (2, 1, [3, 4])]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> list(walk_items(d, ancestors=False, values_only=True))[1:]
    [(2, 1, 1), (2, 0, 'ca'), (3, 0, 3), (3, 1, 4), (2, 'ba', 2)]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> list(walk_items(d, keys_as_ancestors=True, values_only=True))[0:1]
    [(4, 0, 'aa', ({'a': ['aa', 1], 'c': ('ca', [3, 4]), 'b': {'ba': 2}}, 'a', ['aa', 1], 0))]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> list(walk_items(d, keys_as_ancestors=True, values_only=True))[-1:]
    [(4, 'ba', 2, ({'a': ['aa', 1], 'c': ('ca', [3, 4]), 'b': {'ba': 2}}, 'b', {'ba': 2}, 'ba'))]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> d = walk_items(d, ancestors=False, keys_as_ancestors=True, values_only=True);
    >>> list(enumerate(d))
    [(0, (4, 0, 'aa')), (1, (4, 1, 1)), (2, (4, 0, 'ca')), (3, (6, 0, 3)), (4, (6, 1, 4)), (5, (4, 'ba', 2))]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> d = walk_items(d, ancestors=False, keys_as_ancestors=False, values_only=True);
    >>> list(enumerate(d))
    [(0, (2, 0, 'aa')), (1, (2, 1, 1)), (2, (2, 0, 'ca')), (3, (3, 0, 3)), (4, (3, 1, 4)), (5, (2, 'ba', 2))]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> d = walk_items(d, ancestors=False, keys_as_ancestors=False, values_only=False);
    >>> list(enumerate(d))[1::3]
    [(1, (1, 'a', ['aa', 1])), (4, (1, 'c', ('ca', [3, 4]))), (7, (3, 0, 3)), (10, (2, 'ba', 2))]

    >>> d = {'a': ['aa', 1], 'b': {'ba': 2}, 'c': ('ca', [3, 4])};
    >>> d = walk_items(d, keys_as_ancestors=False, values_only=True);
    >>> [(i, d, k, v) for i, (d, k, v, a) in enumerate(d)]
    [(0, 2, 0, 'aa'), (1, 2, 1, 1), (2, 2, 0, 'ca'), (3, 3, 0, 3), (4, 3, 1, 4), (5, 2, 'ba', 2)]

    >>> d = ['a', 1]; list(walk_items(d))
    [(0, None, ['a', 1], ()), (1, 0, 'a', (['a', 1],)), (1, 1, 1, (['a', 1],))]

    >>> d = {'a': 1}; list(walk_items(d))
    [(0, None, {'a': 1}, ()), (1, 'a', 1, ({'a': 1},))]

    >>> d = ('a', 1); list(walk_items(d))
    [(0, None, ('a', 1), ()), (1, 0, 'a', (('a', 1),)), (1, 1, 1, (('a', 1),))]

    >>> d = set(('a', 1)); list(walk_items(d))
    [(0, None, set(['a', 1]), ()), (1, 0, 'a', (set(['a', 1]),)), (1, 1, 1, (set(['a', 1]),))]

    >>> d = [1]; list(walk_items(d))
    [(0, None, [1], ()), (1, 0, 1, ([1],))]

    >>> d = [['a', 1]]; list(walk_items(d))[1:]
    [(1, 0, ['a', 1], ([['a', 1]],)), (2, 0, 'a', ([['a', 1]], ['a', 1])), (2, 1, 1, ([['a', 1]], ['a', 1]))]

    >>> d = [{'a': 1}]; list(walk_items(d))
    [(0, None, [{'a': 1}], ()), (1, 0, {'a': 1}, ([{'a': 1}],)), (2, 'a', 1, ([{'a': 1}], {'a': 1}))]

    >>> d = [('a', 1)]; list(walk_items(d))[1:]
    [(1, 0, ('a', 1), ([('a', 1)],)), (2, 0, 'a', ([('a', 1)], ('a', 1))), (2, 1, 1, ([('a', 1)], ('a', 1)))]

    >>> d = [set(('a', 1))]; list(walk_items(d))[1:3]
    [(1, 0, set(['a', 1]), ([set(['a', 1])],)), (2, 0, 'a', ([set(['a', 1])], set(['a', 1])))]

    >>> d = [set(('a', 1))]; list(walk_items(d, ancestors=False))
    [(0, None, [set(['a', 1])]), (1, 0, set(['a', 1])), (2, 0, 'a'), (2, 1, 1)]

    >>> d = [OrderedDict((('a', 1),('b', 2)))];
    >>> d = list(walk_items(d, values_only=True, ancestors=False)); list(enumerate(d))
    [(0, (2, 'a', 1)), (1, (2, 'b', 2))]

    >>> d = [OrderedDict((('a', 1),('b', 2)))];
    >>> d = list(walk_items(d, values_only=True)); [(i, d, k, v) for i, (d, k, v, a) in enumerate(d)]
    [(0, 2, 'a', 1), (1, 2, 'b', 2)]

    >>> d = {'a': 1, 'b': {'c': 6, 'd': 7, 'g': {'h': 3, 'i': 9}}, 'e': {'f': 3}};
    >>> d = list(walk_items(d, ancestors=False, values_only=True)); list(enumerate(d))[-3:]
    [(3, (3, 'i', 9)), (4, (3, 'h', 3)), (5, (2, 'f', 3))]

    >>> d = OrderedDict({'a': 1, 'b': {'c': 6, 'd': 7, 'g': OrderedDict((('h', 3), ('i', 9)))}, 'e': {'f': 3}});
    >>> d = list(walk_items(d, ancestors=False, values_only=False)); list(enumerate(d))[-3:]
    [(7, (3, 'i', 9)), (8, (1, 'e', {'f': 3})), (9, (2, 'f', 3))]

    >>> d = OrderedDict({'a': 1, 'b': {'c': 6, 'd': 7, 'g': defaultdict(int, (('h', 3), ('i', 9)))}, 'e': {'f': 3}});
    >>> d = list(walk_items(d, ancestors=False)); list(enumerate(d))[-3:]
    [(7, (3, 'h', 3)), (8, (1, 'e', {'f': 3})), (9, (2, 'f', 3))]

    >>> d = OrderedDict({'a': 1, 'b': {'g': OrderedDict((('h', 3), ('i', 9)))}, 'e': defaultdict(int, {'f': 10})});
    >>> d = list(walk_items(d, ancestors=False, values_only=False)); list(enumerate(d))[-2:]
    [(6, (1, 'e', defaultdict(<type 'int'>, {'f': 10}))), (7, (2, 'f', 10))]

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True));
    >>> d = [(i, d, k, v) for i, (d, k, v, a) in enumerate(d) if v % 2];
    >>> list(d)
    [(0, 4, 'e', 5), (3, 2, 'i', 9)]

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=False));
    >>> d = [(i, d, k, v) for i, (d, k, v, a) in enumerate(d) if isinstance(v, int) and v % 2];
    >>> list(d)
    [(4, 4, 'e', 5), (8, 2, 'i', 9)]

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True));
    >>> d = [(i, d, k, v) for i, (d, k, v, a) in enumerate(d) if not v % 2];
    >>> list(d)
    [(1, 4, 'f', 6), (2, 2, 'b', 2), (4, 2, 'h', 8)]

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True, keys_as_ancestors=True));
    >>> d = [(i, d, k, v) for i, (d, k, v, a) in enumerate(d) if not v % 2];
    >>> list(d)
    [(1, 8, 'f', 6), (2, 4, 'b', 2), (4, 4, 'h', 8)]

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True, keys_as_ancestors=True));
    >>> d = ['#{}: {}={}'.format(i, '.'.join(a[1::2]), v) for i, (d, k, v, a) in enumerate(d) if not v % 2];
    >>> list(d)
    ['#1: a.c.d.f=6', '#2: a.b=2', '#4: g.h=8']

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True, keys_as_ancestors=True));
    >>> d = ['#{}. {}={}'.format(i, ':'.join(a[-3::2]), v) for i, (d, k, v, a) in enumerate(d) if not v % 2];
    >>> list(d)
    ['#1. d:f=6', '#2. a:b=2', '#4. g:h=8']

    >>> d = {'a': {'b': 2, 'c': {'d': {'e': 5, 'f': 6}}}, 'g': {'h': 8, 'i': 9}};
    >>> d = list(walk_items(d, values_only=True, keys_as_ancestors=True));
    >>> d = ["#{}. {}['{}']={}".format(i, a[-3], a[-1], v) for i, (d, k, v, a) in enumerate(d) if not v % 2];
    >>> list(d)
    ["#1. d['f']=6", "#2. a['b']=2", "#4. g['h']=8"]
    """
    is_map = isinstance(obj, Mapping)
    is_seq = isinstance(obj, (Sequence, Set)) and not isinstance(obj, string_types)
    is_collection = bool(is_map or is_seq)
    if not values_only or not is_collection:
        if ancestors:
            yield len(obj_ancestors), key, obj, obj_ancestors
        else:
            yield len(obj_ancestors), key, obj
    if is_collection:
        if is_map:
            items = iteritems(obj)
        elif is_seq:
            items = enumerate(obj)
        for key, value in items:
            obj_ancestors2 = obj_ancestors + (obj,)
            if keys_as_ancestors:
                obj_ancestors2 += (key,)
            for child in walk_items(value, obj_ancestors=obj_ancestors2, key=key,
                                    values_only=values_only, ancestors=ancestors, keys_as_ancestors=keys_as_ancestors):
                yield child


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
