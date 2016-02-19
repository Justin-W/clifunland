import json
from collections import OrderedDict


def contains_valid_json(obj):
    """
    Indicates whether a specified value contains valid and well-formed JSON.

    :param obj: a file-like or string-like object.
    :return: True if valid, else False.

    >>> contains_valid_json(None)
    False

    >>> contains_valid_json('')
    False

    >>> contains_valid_json('{')
    False

    >>> contains_valid_json('{}')
    True

    >>> contains_valid_json('{"constants": {"pi": 3.14}}')
    True
    """
    if obj is None:
        return False
    try:
        try:
            # json_object = json.loads(obj.read())
            json.load(obj)
        except AttributeError:
            # obj is not a file
            json.loads(obj)
    except ValueError:
        return False
    return True


def load_ordered(fp, **kwargs):
    """
    Convenience wrapper for json.load() that loads the JSON while preserving the original element ordering/sequence.
    """
    return json.load(fp, object_pairs_hook=OrderedDict, **kwargs)


def loads_ordered(s, **kwargs):
    """
    Convenience wrapper for json.loads() that loads the JSON while preserving the original element ordering/sequence.

    >>> loads_ordered('{}')
    OrderedDict()

    >>> loads_ordered('{"constants": {"pi2": 3.14, "pi5": 3.14159}}')
    OrderedDict([(u'constants', OrderedDict([(u'pi2', 3.14), (u'pi5', 3.14159)]))])
    """
    return json.loads(s, object_pairs_hook=OrderedDict, **kwargs)


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
