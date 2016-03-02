import json
import logging
import sys

import pytest
from click._compat import PY2
from click.testing import CliRunner

import clifunzone.xmltool as sut

# Use the most reasonable io that users would use for the python version.
if PY2:
    from cStringIO import StringIO as ReasonableBytesIO
    # from StringIO import StringIO as ReasonableStringIO
else:
    from io import BytesIO as ReasonableBytesIO
    # from io import StringIO as ReasonableStringIO


def assert_exit_code(actual, expected):
    __tracebackhide__ = True
    assert actual == expected


def assert_out_eq(actual, expected, encode=True, strict=False):
    """
    Utility assertion function. Helps keep the test code cleaner.

    :param actual:
    :param expected: a list of strings representing lines of output, or else a combined output string.
        A trailing newline gets appended automatically if expected is not False-y.
        If only a single newline is expected, pass [''].
    :param encode:
    :param strict:
    """
    __tracebackhide__ = True
    output_expected = bool(expected)
    if expected is None:
        expected = ''
    if isinstance(expected, list):
        # treat the list as a list of output lines
        expected = '\n'.join(expected)
    if output_expected:
        # automatically add a trailing newline only if some output is expected
        expected += '\n'
    if not strict:
        actual = py3_json_agnostic(actual)
        expected = py3_json_agnostic(expected)
    if encode:
        if actual is not None:
            actual = actual.encode()
        if expected is not None:
            expected = expected.encode()
    assert actual == expected


def assert_out_ok(actual, expected, encode=True):
    __tracebackhide__ = True
    assert_out_eq(actual, expected, encode=encode, strict=False)


def assert_json_eq(actual, expected):
    """
    Utility assertion function. Helps keep the test code cleaner.

    :param actual:
    :param expected: a list of strings representing lines of output, or else a combined output string.
        A trailing newline gets appended automatically if expected is not False-y.
        If only a single newline is expected, pass [''].
    """
    __tracebackhide__ = True
    output_expected = bool(expected)
    # if expected is None:
    #     expected = ''
    if isinstance(expected, list):
        # treat the list as a list of output lines
        expected = '\n'.join(expected)
    if output_expected:
        # automatically add a trailing newline only if some output is expected
        expected += '\n'

    # actual = ReasonableStringIO(actual).read()
    # expected = ReasonableStringIO(expected).read()
    #
    # actual = actual.strip()
    # expected = expected.strip()

    try:
        actual = json.loads(actual)
        expected = json.loads(expected)
    except ValueError:
        logging.exception('json.loads() error.\nactual=%s.\nexpected=%s.', actual, expected)
        raise

    # if not strict:
    try:
        actual = json.dumps(actual, sort_keys=True, separators=(',', ':'))
        expected = json.dumps(expected, sort_keys=True, separators=(',', ':'))
    except ValueError:
        logging.exception('json.dumps() error.\nactual=%s.\nexpected=%s.', actual, expected)
        raise
    # else:
    #     actual = json.dumps(actual, sort_keys=False, separators=(',', ':'))
    #     expected = json.dumps(expected, sort_keys=False, separators=(',', ':'))

    assert actual == expected


def py3_json_agnostic(actual):
    return actual.replace(', \n', ',\n')


def as_piped_input(input_text):
    # return PipedInput(input_text)
    # return ReasonableBytesIO(input_text)
    return ReasonableBytesIO(input_text.encode())
    # return ReasonableBytesIO(input_text.encode('utf-8'))


def clirunner_invoke_piped(cli, args, input_text, exit_code, expected=None, expected_json=None, expected_xml=None):
    runner = CliRunner()
    result = runner.invoke(cli, args, input=as_piped_input(input_text))
    if expected is not None:
        assert_out_ok(result.output, expected)
    if expected_json is not None:
        assert_json_eq(result.output, expected_json)
    if expected_xml is not None:
        # assert_xml_eq(result.output, expected_xml)
        assert_out_ok(result.output, expected_xml)
    assert_exit_code(result.exit_code, exit_code)


def test_none():
    runner = CliRunner()
    result = runner.invoke(sut.cli, [])

    assert result.output == 'I was invoked without a subcommand...\n'
    # assert 'I was invoked without a subcommand...' in result.output
    assert result.exit_code == 0


@pytest.mark.parametrize("input_text", [
    '<abc/>',
    '<a>\n<b/>\n</a>',
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_echo(input_text):
    expected = input_text or ['']
    clirunner_invoke_piped(sut.echo, [], input_text, exit_code=0, expected=expected)


@pytest.mark.parametrize("input_text,exit_code,expected", [
    ('<abc/>', 0, 'True'),
    ('<a>\n<b/>\n</a>', 0, 'True'),
    ('<a>\n<b><c/> </b></a>', 0, 'True'),
    ('<a>\t<b><c/> </b></a>', 0, 'True'),
    ('', 1, 'False'),
    (' ', 1, 'False'),
    ('<<<', 1, 'False'),
    ('>', 1, 'False'),
    ('<a>', 1, 'False'),
    ('abc', 1, 'False'),
    ('{"a": null}', 1, 'False')
])
def test_validate(input_text, exit_code, expected):
    clirunner_invoke_piped(sut.validate, [], input_text, exit_code=exit_code, expected=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('<abc/>', [
        '{',
        '  "root": {',
        '    "content": {',
        '      "tag": "abc"',
        '    }, ',
        '    "metrics": {}',
        '  }',
        '}'
    ]),
    ('<a>\t<b><c/> </b></a>', [
        '{',
        '  "root": {',
        '    "content": {',
        '      "#text": "\\t", ',
        '      "tag": "a"',
        '    }, ',
        '    "metrics": {',
        '      "children": {',
        '        "attributes": [], ',
        '        "count": 1, ',
        '        "tags": [',
        '          "b"',
        '        ]',
        '      }, ',
        '      "descendants": {',
        '        "attributes": [], ',
        '        "count": 2, ',
        '        "tags": [',
        '          "b", ',
        '          "c"',
        '        ]',
        '      }',
        '    }',
        '  }',
        '}'
    ])
])
def test_info(input_text, expected):
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=0, expected_json=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_info_invalid_input(input_text):
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', [], '{"abc": null}'),
    ('<abc/>', ['-p'], [
        '{',
        '    "abc": null',
        '}'
    ]),
    ('<a>\n<b/>\n</a>', ['-p', '-sws'], [
        '{',
        '    "a": {',
        '        "b": null',
        '    }',
        '}'
    ]),
    ('<a>\n<b/>\n</a>', [], '{"a": {"b": {"#tail": "\\n"}, "#text": "\\n"}}'),
    ('<a>\n<b/>\n</a>', ['-sws'], '{"a": {"b": null}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', [],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#tail": " ", "#text": " hi\\t"}, '
     '"#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sws'],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#text": "hi"}}}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sa'],
     '{"a": {"b": {"c": {"#tail": " ", "#text": " hi\\t"}, "#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sns'],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#tail": " ", "#text": " hi\\t"}, '
     '"#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sws', '-sa', '-sns'], [
        '{"a": {"b": {"c": "hi"}}}'
    ])
])
def test_tojson(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.tojson, cli_args, input_text, exit_code=0, expected_json=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', ['--echo'], [
        '',
        'XML:',
        '<abc/>',
        '',
        'JSON:',
        '{"abc": null}'
    ])
])
def test_tojson_echo(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.tojson, cli_args, input_text, exit_code=0, expected=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_tojson_invalid_input(input_text):
    clirunner_invoke_piped(sut.tojson, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,expected", [
    ('<abc/>', ['{"path":"/abc","content":{"tag":"abc"}}']),
    ('<a>\t<b><c/> </b></a>', [
        '{"path":"/a","content":{"tag":"a","#text":"\\t"},' +
        '"metrics":{"children":{"count":1,"tags":["b"]},"descendants":{"count":2,"tags":["b","c"]}}}',
        '{"path":"/a/b","content":{"tag":"b"},' +
        '"metrics":{"children":{"count":1,"tags":["c"]},"descendants":{"count":1,"tags":["c"]}}}',
        '{"path":"/a/b/c","content":{"tag":"c"}}'
    ])
])
@pytest.mark.skipif(sys.version_info > (3,3),
                    reason="fails on the py35 travis build")
def test_elements(input_text, expected):
    # expected = '{"output":{[%s]}}' % ','.join(expected)
    expected = '[%s]' % ','.join(expected)
    clirunner_invoke_piped(sut.elements, ['-p'], input_text, exit_code=0, expected_json=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('<a/>', '[\n    {\n        "path": "/a",\n        "content": {\n            "tag": "a"\n        }\n    }\n]')
])
def test_elements_pretty(input_text, expected):
    clirunner_invoke_piped(sut.elements, ['-p'], input_text, exit_code=0, expected_json=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_elements_invalid_input(input_text):
    clirunner_invoke_piped(sut.elements, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<a>\t<b> <c/> hi \t</b></a>', ['-w'], '<a><b><c/> hi \t</b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b/d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e'], '<a><b><c/></b><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b/c'], '<a><b/><b><d><e/></d><d/></b></a>'),
    ('<a><b>1</b><b><c/></b><b><d><e/></d><d/></b></a>', ['-e'], '<a><b>1</b></a>'),
    ('<a><b>1</b><b><c/>2</b><b><d><e>2</e></d></b></a>', ['-x //b/c', '-e'], '<a><b>1</b><b><d><e>2</e></d></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e', '-x //b/c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-t d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-t e', '-t c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e', '-t c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', [], '<a>t<b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-e'], '<a>t<b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ea'], '<a>t<b b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes'], '<a>t<b/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-text'], '<a><b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab'], '<a>t<b e="" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-av', 'False'], '<a>t<b e="" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-av', '0'], '<a>t<b e="" b="False"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai'], '<a>t<b e=""/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai', '-e'], '<a>t<b e=""/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai', '-ea', '-e'], '<a>t</a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes', '-e'], '<a>t</a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes', '--all-text', '-e'], '<a></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b'], '<a/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[1]'], '<a><b><c/></b><b><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[2]'], '<a><b><c/></b><b><d><e/></d></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[5]'], '<a><b><c/></b><b><d><e/></d><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)<=1]'], '<a><b id="b2"/></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(*)=0]'],
     '<a><b id="b1"/><b id="b2"><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)<1]'],
     '<a><b id="b1"/><b id="b2"><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)=3]'],
     '<a><b id="b1"><c/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x /*//*[count(./*)=2]'],
     '<a><b id="b1"><c/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[count(*)>=1]'], '<a><b><c/></b><b><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[count(*)!=1]'], '<a><b><c/></b><b><d><e/></d></b></a>')
])
def test_strip(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.strip, cli_args, input_text, exit_code=0, expected_xml=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_strip_invalid_input(input_text):
    clirunner_invoke_piped(sut.strip, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<a><b><c/></b></a>', ['-x //b'], '<results>\n<b><c/></b>\n</results>'),
    ('<a><b><c/></b></a>', ['-x //b', '-nr'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b'],
     '<R>\n<b><c/></b>\n<b><d><e/></d><d/></b>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[position()=1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[2]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[last()]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[position()=2]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d/e'], '<e/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b/c/parent::*'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d/e/parent::*'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //*[count(./c)=1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(./c|./e)=1]'],
     '<R>\n<b><c/></b>\n<d><e/></d>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>', ['-nr', '-x //b[@z="1"]'],
     '<b z="1"><c/></b>'),
    ('<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>', ['-rR', '-x //*[@z="1"]'],
     '<R>\n<b z="1"><c/></b>\n<e z="1"/>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-rR', '-x //*[@z="1"]'],
     '<R>\n<b z="1"><c/></b>\n<d z="1"><e z="2"/></d>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-rR', '-x //*[@z and @z!="2"]'],
     '<R>\n<b z="1"><c/></b>\n<d z="1"><e z="2"/></d>\n</R>'),
    # ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-nr', '-x //*[@z="1" and position()>2]'],
    #  '<d z="1"><e z="2"/></d>'),
    ('<z><a>1a1</a><b>2b1</b><c>3c1</c><a>4a2</a><b>5b2</b><c>6c2</c><a>7a3</a></z>',
     ['-rR', '-x //*[contains(text(),"3")]'],
     '<R>\n<c>3c1</c>\n<a>7a3</a>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b/d'], '<R>\n<d><e/></d>\n<d/>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b'], '<R>\n<b><c/></b>\n<b><d><e/></d><d/></b>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //d'], '<R>\n<d><e/></d>\n<d/>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[1]'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[2]'], '<d/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //d[5]'], '<R>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[5]'], ''),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(.//*)<=1]'],
     '<R>\n<b id="b1"><c/></b>\n<c/>\n<d><e/></d>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(*)=0]'],
     '<R>\n<c/>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(.//*)<1]'],
     '<R>\n<c/>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[count(.//*)=3]'],
     '<b id="b2"><d><e/></d><d/></b>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x /*//*[count(./*)=2]'],
     '<b id="b2"><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[count(*)>=1]'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[count(*)!=1]'], '<d/>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]'],
     '<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]'],
     '<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //b[@id="b1"]'],
     '<b id="b1"><c/></b>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //b[@id="b1"]', '-x //*[./e]'],
     '<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]', '-x //b[@id="b1"]'],
     '<b id="b1"><c/></b>'),
])
def test_find(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.find, cli_args, input_text, exit_code=0, expected_xml=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_find_invalid_input(input_text):
    clirunner_invoke_piped(sut.find, [], input_text, exit_code=-1, expected=None)
