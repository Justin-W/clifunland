from collections import OrderedDict

import reflection_utils
import xml2json

try:
    from lxml import etree as ET
except ImportError:
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET


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


def xml_to_json(xmlstring, strip_attribute=False, strip_namespace=False, strip_whitespace=True, pretty=False):
    r"""
    Converts XML to JSON.

    :param xmlstring: the XML string.
    :param strip_attribute: If True, attributes will be ignored.
    :param strip_namespace: If True, namespaces will be ignored.
    :param strip_whitespace: If True, 'unimportant' whitespace will be ignored.
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

    >>> xml_to_json('<constants><constant id="pi" value="3.14" />\n<constant id="zero">0</constant></constants>')
    '{"constants": {"constant": [{"@id": "pi", "@value": "3.14"}, {"@id": "zero", "#text": "0"}]}}'

    >>> xml_to_json('<z> <q qz="z" qy="y" /> <a az="z" ab="b" ay="y" /> <x/></z>', strip_whitespace=True)
    '{"z": {"q": {"@qy": "y", "@qz": "z"}, "a": {"@ay": "y", "@az": "z", "@ab": "b"}, "x": null}}'

    >>> xml_to_json('<royg> <r/> <o/> <y/> <r e="d"/> <g/></royg>', strip_whitespace=True)
    '{"royg": {"r": [null, {"@e": "d"}], "o": null, "y": null, "g": null}}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=False)
    '{"a": {"b": {"@id": "b1", "#tail": "\\n"}, "c": {"#tail": " "}, "d": {"#tail": " ", "#text": " "}, "#text": " "}}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=True)
    '{"a": {"b": {"@id": "b1"}, "c": null, "d": null}}'

    >>> xml_to_json("<a> <b\nid=\"b1\"   />\n<c/> <d> </d> </a>", strip_namespace=False)
    '{"a": {"b": {"@id": "b1"}, "c": null, "d": null}}'

    >>> xml_to_json("<a> <b\nid=\"b1\"   />\n<c/> <d> </d> </a>", strip_namespace=True)
    '{"a": {"b": {"@id": "b1"}, "c": null, "d": null}}'

    >>> xml_to_json('<royg> <r/> <o/> <y/> <r e="d"/> <g/></royg>', strip_whitespace=True, strip_attribute=True)
    '{"royg": {"r": [null, null], "o": null, "y": null, "g": null}}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=False, strip_attribute=True)
    '{"a": {"b": {"#tail": "\\n"}, "c": {"#tail": " "}, "d": {"#tail": " ", "#text": " "}, "#text": " "}}'

    >>> xml_to_json('<a> <b\nid="b1"   />\n<c/> <d> </d> </a>', strip_whitespace=True, strip_attribute=True)
    '{"a": {"b": null, "c": null, "d": null}}'
    """
    if xmlstring is None:
        return None
    return xml2json.xml2json(xmlstring, strip_attribute=strip_attribute, strip_namespace=strip_namespace,
                             strip_whitespace=strip_whitespace, pretty=pretty)


# def etree_to_dict(t):
#     d = {t.tag: map(etree_to_dict, t.iterchildren())}
#     d.update(('@' + k, v) for k, v in t.attrib.iteritems())
#     d['text'] = t.text
#     return d


def element_info(element, tree=None):
    """
    Returns a dict with (incomplete) info about a specified element/node.

    :param element: an <ElementTree.Element> instance.
    :return: a <collections.OrderedDict> instance.
    """
    d = OrderedDict()

    d['tag'] = element.tag
    if tree:
        try:
            d['path'] = tree.getpath(element)
        except AttributeError:
            # tree.getpath() is only available in lxml, not in the builtin xml.etree
            # see: http://lxml.de/xpathxslt.html#xpath
            # see: http://stackoverflow.com/a/13352109
            pass

    if element.text:
        d['#text'] = element.text

    # get all attribs
    # children = element.iterfind('.')
    attribs = element.attrib.items()
    # attribs_count = len(attribs)
    # prefix attrib names
    attribs = [('@' + k, v) for k, v in attribs]
    # # filter out duplicates
    # attribs = set(attribs)
    # # sorted
    # attribs = sorted(attribs)
    # if attribs_count:
    if attribs:
        # d['attribs'] = {'tags': attribs, 'count': attribs_count}
        d['attribs'] = attribs

    # get all direct children
    # children = element.iterfind('.')
    children = element.findall('./*')
    children_count = len(children)
    # convert to tag names
    children = [child.tag for child in children]
    # filter out duplicates
    children = set(children)
    # sorted
    children = sorted(children)
    if children_count:
        d['children'] = {'tags': children, 'count': children_count}

    # get all descendants
    descendants = element.findall('.//')
    # convert to tag names
    descendants = [descendent.tag for descendent in descendants]
    descendants_count = len(descendants)
    # filter out duplicates
    descendants = set(descendants)
    # sorted
    descendants = sorted(descendants)
    if descendants_count:
        d['descendants'] = {'tags': descendants, 'count': descendants_count}

    return d


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
