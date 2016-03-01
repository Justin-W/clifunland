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
    __tracebackhide__ = True
    if isinstance(expected, list):
        # treat the list as a list of output lines
        expected = '\n'.join(expected)
    if expected:
        # automatically add a trailing newline only if some output is expected
        expected += '\n'
    if not strict:
        actual = py3_json_agnostic(actual)
        expected = py3_json_agnostic(expected)
    if encode:
        actual = actual.encode()
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


def test_echo():
    runner = CliRunner()

    helper_test_echo(runner, '<abc/>')
    helper_test_echo(runner, '<a>\n<b/>\n</a>')
    helper_test_echo(runner, '<<<')


def helper_test_echo(runner, input_text):
    expected = input_text

    result = runner.invoke(sut.echo, [], input=as_piped_input(input_text))
    assert result.output == expected + '\n'
    assert result.exit_code == 0


@pytest.mark.parametrize("input_text,exit_code,expected", [
    ('<abc/>', 0, 'True'),
    ('<a>\n<b/>\n</a>', 0, 'True'),
    ('<a>\n<b><c/> </b></a>', 0, 'True'),
    ('<a>\t<b><c/> </b></a>', 0, 'True'),
    ('', 1, 'False'),
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
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_info_invalid_input(input_text):
    invoke_sut_piped_input(sut.info, [], input_text, exit_code=-1, expected='')
