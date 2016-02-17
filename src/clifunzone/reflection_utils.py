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


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print 'Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total)


if __name__ == "__main__":
    main()
