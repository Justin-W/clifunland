from collections import OrderedDict

from clifunzone import reflection_utils
from clifunzone import xml2json

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

    >>> load('')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    XMLSyntaxError: None
    # Note: the exception will be different without lxml: ParseError: no element found: line 1, column 0

    >>> load('<')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    XMLSyntaxError: StartTag: invalid element name, line 1, column 2
    # Note: the exception will be different without lxml: ParseError: unclosed token: line 1, column 0

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

    def get_distinct_tag_names(elements):
        # convert to tag names
        elements = [child.tag for child in elements]
        # filter out duplicates
        elements = set(elements)
        return elements

    def get_distinct_attribute_names(elements):
        names = set()
        for i in elements:
            names.update(i.attrib.keys())
        names = ('@' + k for k in names)
        return names

    d = OrderedDict()

    if tree:
        try:
            d.update({'path': tree.getpath(element)})
        except AttributeError:
            # tree.getpath() is only available in lxml, not in the builtin xml.etree
            # see: http://lxml.de/xpathxslt.html#xpath
            # see: http://stackoverflow.com/a/13352109
            pass

    d2 = {'tag': element.tag}
    if element.text:
        d2.update({'#text': element.text})
    if element.attrib:
        # get all attribs
        attribs = element.attrib.items()
        # prefix attrib names
        attribs = [('@' + k, v) for k, v in attribs]
        # attribs = {k, v for k, v in attribs}
        attribs = OrderedDict(attribs)
        # if attribs:
        #     # d['attribs'] = {'tags': attribs, 'count': attribs_count}
        #     d['attribs'] = attribs
        d2.update({'attributes': attribs})
    d['content'] = d2

    d['metrics'] = {}

    # get all direct children
    children = get_elements(element, xpath='./*')
    children_count = len(children)

    if children_count:
        d2 = {'count': children_count}
        d2.update({'tags': (sorted(get_distinct_tag_names(children)))})
        d2.update({'attributes': (sorted(get_distinct_attribute_names(children)))})
        d['metrics']['children'] = d2

    # get all descendants
    descendants = get_elements(element, xpath='.//*')
    descendants_count = len(descendants)

    if descendants_count:
        d2 = {'count': descendants_count}
        d2.update({'tags': (sorted(get_distinct_tag_names(descendants)))})
        d2.update({'attributes': (sorted(get_distinct_attribute_names(descendants)))})
        d['metrics']['descendants'] = d2
    return d


def is_empty_element(elem):
    """
    Indicates whether an XML Element object is 'empty'.

    :param elem: an Element object
    :return: True if elem is empty
    """
    # return not bool(len(elem) or len(elem.attrib) or len(elem.text))
    return not bool(len(elem) or elem.attrib or elem.text)


def is_parent_element(elem):
    """
    Indicates whether an XML Element object has any children.

    :param elem: an Element object
    :return: True if elem has any child elements
    """
    return len(elem)


def count_elements(obj, xpath=None):
    """
    Returns a count of the XML elements that match a specified XPath expression.

    This function encapsulates API differences between the lxml and ElementTree packages.

    :param obj: a tree or element object
    :param xpath: an XPath node set/selection expression
    :return: an int
    """
    if not xpath:
        xpath = '//'  # match all elements by default

    # try lxml syntax first (much faster!)
    try:
        return int(obj.xpath('count({xpath})'.format(xpath=xpath)))
    except AttributeError:
        # AttributeError: 'ElementTree' object has no attribute 'xpath'
        pass

    # else try ElementTree syntax
    if xpath.startswith('/'):
        # ElementTree's findall() doesn't like xpath expressions that start with a '/'.
        # e.g. "FutureWarning: This search is broken in 1.3 and earlier, and will be fixed in a future version. ..."
        xpath = '.' + xpath
    return len(obj.findall(xpath))


def get_elements(obj, xpath=None):
    """
    Returns all XML elements that match a specified XPath expression.

    This function encapsulates API differences between the lxml and ElementTree packages.

    :param obj: a tree or element object
    :param xpath: an XPath node set/selection expression
    :return: an iterable
    """
    if not xpath:
        xpath = '//'  # match all elements by default

    # try lxml syntax first (much faster!)
    try:
        return obj.xpath(xpath)
    except AttributeError:
        # AttributeError: 'ElementTree' object has no attribute 'xpath'
        pass

    # else try ElementTree syntax
    if xpath.startswith('/'):
        # ElementTree's findall() doesn't like xpath expressions that start with a '/'.
        # e.g. "FutureWarning: This search is broken in 1.3 and earlier, and will be fixed in a future version. ..."
        xpath = '.' + xpath
    return obj.findall(xpath)


def remove_elements(obj, xpath):
    """
    Removes all XML elements that match a specified XPath expression.

    This function encapsulates API differences between the lxml and ElementTree packages.

    :param obj: a tree or element object
    :param xpath: an XPath node set/selection expression
    :return: an int count of the number of removed elements
    """
    if not xpath:
        raise ValueError('invalid xpath')

    elements = get_elements(obj, xpath=xpath)
    # count = len(elements)
    count = 0
    for i in elements:
        # try lxml syntax first
        try:
            parent = i.getparent()
            parent.remove(i)
        except AttributeError:
            # else try ElementTree syntax
            obj.remove(i)
        count += 1
    return count


def remove_attributes_with_name(element, attrib_name):
    """
    Removes all occurrences of a specific attribute from all elements.

    :param element: an XML element object.
    :param attrib_name: the name of the attribute to remove.
    """
    if attrib_name.startswith('@'):
        # remove the optional leading '@'
        attrib_name = attrib_name[1:]
    # find all elements that have the attribute
    xpath = '//*[@{attrib}]'.format(attrib=attrib_name)
    elements = get_elements(element, xpath=xpath)
    for i in elements:
        del i.attrib[attrib_name]


def remove_attributes_with_value(element, attrib_value):
    """
    Removes all attributes with a specified value from all elements.

    :param element: an XML element object.
    :param attrib_value: the attribute value to match on.
    """
    # find all elements that have 1+ matching attributes
    xpath = '//*[@*="{value}"]'.format(value=(attrib_value.replace('"', '\\"')))
    elements = get_elements(element, xpath=xpath)
    for i in elements:
        # determine the matching keys/attributes
        keys = (k for k in i.attrib.keys() if i.attrib[k] == attrib_value)
        for attrib_name in keys:
            # remove each matching attribute from the current element
            del i.attrib[attrib_name]


def remove_attributes_with_empty_value(element):
    """
    Removes all attributes with an empty value from all elements.

    :param element: an XML element object.
    """
    remove_attributes_with_value(element, '')


# def remove_attributes_if(element, attrib_name, func):
#     """
#     Removes all occurrences of a specific attribute from all elements.
#
#     :param element: an XML element object.
#     :param attrib_name: the name of the attribute to remove.
#     :param func: a predicate function (i.e. returns a bool) with the signature:
#         f(attribute_name, attribute_value)
#     """
#     if attrib_name.startswith('@'):
#         # remove the optional leading '@'
#         attrib_name = attrib_name[1:]
#     # find all elements that have the attribute
#     xpath = '//*[@{attrib}]'.format(attrib=attrib_name)
#     elements = xml_utils.get_elements(element, xpath=xpath)
#     for i in elements:
#         del i.attrib[attrib_name]


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
