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


def py3_json_agnostic(actual):
    return actual.replace(', \n', ',\n')


def as_piped_input(input_text):
    # return PipedInput(input_text)
    # return ReasonableBytesIO(input_text)
    return ReasonableBytesIO(input_text.encode())
    # return ReasonableBytesIO(input_text.encode('utf-8'))


def invoke_sut_piped_input(cli, args, input_text, exit_code, expected):
    runner = CliRunner()
    result = runner.invoke(cli, args, input=as_piped_input(input_text))
    assert_out_ok(result.output, expected)
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
    invoke_sut_piped_input(sut.echo, [], input_text, exit_code=0, expected=expected)


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
    invoke_sut_piped_input(sut.validate, [], input_text, exit_code=exit_code, expected=expected)


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
    invoke_sut_piped_input(sut.info, [], input_text, exit_code=0, expected=expected)


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
    invoke_sut_piped_input(sut.info, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', [], '{"abc": null}'),
    ('<abc/>', ['--echo'], [
        '',
        'XML:',
        '<abc/>',
        '',
        'JSON:',
        '{"abc": null}'
    ]),
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
    invoke_sut_piped_input(sut.tojson, cli_args, input_text, exit_code=0, expected=expected)


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
    invoke_sut_piped_input(sut.tojson, [], input_text, exit_code=-1, expected=None)


@pytest.mark.parametrize("input_text,expected", [
    ('<abc/>', '{"path":"/abc","content":{"tag":"abc"}}'),
    ('<a>\t<b><c/> </b></a>', [
        '{"path":"/a","content":{"#text":"\\t","tag":"a"},' +
        '"metrics":{"children":{"count":1,"tags":["b"]},"descendants":{"count":2,"tags":["b","c"]}}}',
        '{"path":"/a/b","content":{"tag":"b"},' +
        '"metrics":{"children":{"count":1,"tags":["c"]},"descendants":{"count":1,"tags":["c"]}}}',
        '{"path":"/a/b/c","content":{"tag":"c"}}'
    ])
])
def test_elements(input_text, expected):
    invoke_sut_piped_input(sut.elements, [], input_text, exit_code=0, expected=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('<a/>', '[\n    {\n        "path": "/a",\n        "content": {\n            "tag": "a"\n        }\n    }\n]')
])
def test_elements_pretty(input_text, expected):
    invoke_sut_piped_input(sut.elements, ['-p'], input_text, exit_code=0, expected=expected)


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
    invoke_sut_piped_input(sut.elements, [], input_text, exit_code=-1, expected=None)
