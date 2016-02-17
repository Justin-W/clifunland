from xml.etree import ElementTree as ET

import reflection_utils


def contains_valid_xml(obj):
    """
    Indicates whether a specified value contains valid and well-formed XML.

    :param obj: a file-like or string-like object.
    :return: True if valid, else False.

    >>> contains_valid_xml(None)
    False

    >>> contains_valid_xml('')
    False

    >>> contains_valid_xml('<')
    False

    >>> contains_valid_xml('<xml />')
    True

    >>> contains_valid_xml('<constants><constant id="pi" value="3.14" /><constant id="zero">0</constant></constants>')
    True
    """
    if obj is None:
        return False
    try:
        if reflection_utils.is_file_like(obj):
            # read the contents of obj
            obj = obj.read()
        ET.fromstring(obj)
    except ET.ParseError:
        return False
    return True


def load(obj):
    """
    Parses a specified object using ElementTree.

    :param obj: a file-like or string-like object.
    :return: True if valid, else False.

    >>> load(None)
    Traceback (most recent call last):
    ValueError

    >>> load('')
    Traceback (most recent call last):
    ParseError: no element found: line 1, column 0

    >>> load('<')
    Traceback (most recent call last):
    ParseError: unclosed token: line 1, column 0

    >>> load('<abc />').tag
    'abc'

    >>> load('<constants><constant id="pi" value="3.14" /><constant id="zero">0</constant></constants>').tag
    'constants'
    """
    if obj is None:
        raise ValueError
    if reflection_utils.is_file_like(obj):
        # read the contents of obj
        obj = obj.read()
    return ET.fromstring(obj)


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print 'Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total)


if __name__ == "__main__":
    main()
