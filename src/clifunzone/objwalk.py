from collections import Mapping
from collections import Sequence
from collections import Set

# See objwalk() function's docstring
# See: https://gist.github.com/sente/1480558
try:
    from six import string_types, iteritems
except ImportError:
    string_types = (str, unicode) if str is bytes else (str, bytes)  # noqa
    # iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()

    def iteritems(mapping):
        return getattr(mapping, 'iteritems', mapping.items)()

__all__ = ['objwalk']


def objwalk(obj, path=(), memo=None):
    """
    walks over pretty much any Python object and yields the objects contained within (if any)
    along with the path to reach them.

    See: https://gist.github.com/sente/1480558
    See: https://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    See: http://code.activestate.com/recipes/577982-recursively-walk-python-objects/

    :param obj:
    :param path:
    :param memo:

    >>> list(objwalk(1))
    [((), 1)]

    >>> d = {'a': 1, 'b': {'c': 6, 'd': 7, 'g': {'h': 3, 'i': 9}}, 'e': {'f': 3}}; list(objwalk(d))  # noqa
    [(('a',), 1), (('b', 'c'), 6), (('b', 'd'), 7), (('b', 'g', 'i'), 9), (('b', 'g', 'h'), 3), (('e', 'f'), 3)]
    """
    if memo is None:
        memo = set()
    if isinstance(obj, Mapping):
        if id(obj) not in memo:
            memo.add(id(obj))
            for key, value in iteritems(obj):
                for child in objwalk(value, path + (key,), memo):
                    yield child
    elif isinstance(obj, (Sequence, Set)) and not isinstance(obj, string_types):
        if id(obj) not in memo:
            memo.add(id(obj))
            for index, value in enumerate(obj):
                for child in objwalk(value, path + (index,), memo):
                    yield child
    else:
        yield path, obj


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
