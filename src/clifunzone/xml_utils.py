from xml.etree import ElementTree as ET

import reflection_utils
import xml2json


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


def xml_to_json(xmlstring, strip_whitespace=True, strip_namespace=False, pretty=False):
    r"""
    Converts XML to JSON.

    :param xmlstring: the XML string.
    :param strip_whitespace: If True, 'unimportant' whitespace will be ignored.
    :param strip_namespace: If True, namespaces will be ignored.
    :param pretty: If True, the output will be pretty-formatted.
    :return: a JSON string.

    >>> xml_to_json(None) is None
    True

    >>> xml_to_json('')
    Traceback (most recent call last):
    ParseError: no element found: line 1, column 0

    >>> xml_to_json('<')
    Traceback (most recent call last):
    ParseError: unclosed token: line 1, column 0

    >>> xml_to_json('<a/>')
    '{"a": null}'

    >>> xml_to_json('<a/>', pretty=True)
    '{\n    "a": null\n}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=False)
    '{"a": {"#text": " ", "c": {"#tail": " "}, "b": {"#tail": "\\n", "@id": "b1"}, "d": {"#tail": " ", "#text": " "}}}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=True)
    '{"a": {"c": null, "b": {"@id": "b1"}, "d": null}}'

    >>> xml_to_json("<a> <b\nid=\"b1\"   />\n<c/> <d> </d> </a>", strip_namespace=False)
    '{"a": {"c": null, "b": {"@id": "b1"}, "d": null}}'

    >>> xml_to_json("<a> <b\nid=\"b1\"   />\n<c/> <d> </d> </a>", strip_namespace=True)
    '{"a": {"c": null, "b": null, "d": null}}'

    >>> xml_to_json('<constants><constant id="pi" value="3.14" />\n<constant id="zero">0</constant></constants>')
    '{"constants": {"constant": [{"@id": "pi", "@value": "3.14"}, {"#text": "0", "@id": "zero"}]}}'
    """

    def construct_options_param(pretty):
        from collections import namedtuple
        Xml2JsonOptions = namedtuple('Xml2JsonOptions', ['pretty'], verbose=False)
        options = Xml2JsonOptions(pretty=pretty)
        return options
    if xmlstring is None:
        return None
    options = construct_options_param(pretty)
    return xml2json.xml2json(xmlstring, options=options, strip_ns=strip_namespace, strip=strip_whitespace)


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
