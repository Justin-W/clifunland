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


def as_piped_input(input_text):
    # return PipedInput(input_text)
    # return ReasonableBytesIO(input_text)
    return ReasonableBytesIO(input_text.encode())
    # return ReasonableBytesIO(input_text.encode('utf-8'))


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


def test_validate():
    runner = CliRunner()

    helper_test_validate(runner, '<abc/>', expected='True', exit_code=0)
    helper_test_validate(runner, '<a>\n<b/>\n</a>', expected='True', exit_code=0)
    helper_test_validate(runner, '<<<', expected='False', exit_code=1)


def helper_test_validate(runner, input_text, expected, exit_code):
    result = runner.invoke(sut.validate, [], input=as_piped_input(input_text))
    assert result.output == expected + '\n'
    assert result.exit_code == exit_code


def test_info():
    runner = CliRunner()

    # test valid input
    expected = '\n'.join([
        '{',
        '  "root": {',
        '    "content": {',
        '      "tag": "abc"',
        '    }, ',
        '    "metrics": {}',
        '  }',
        '}'
    ])
    helper_test_info(runner, '<abc/>', expected=expected + '\n', exit_code=0)

    expected = '\n'.join([
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
    helper_test_info(runner, '<a>\t<b><c/> </b></a>', expected=expected + '\n', exit_code=0)

    # test invalid input
    helper_test_info(runner, '', expected='', exit_code=-1)
    helper_test_info(runner, '<<<', expected='', exit_code=-1)
    helper_test_info(runner, '>', expected='', exit_code=-1)
    helper_test_info(runner, '<a>', expected='', exit_code=-1)


def helper_test_info(runner, input_text, expected, exit_code):
    result = runner.invoke(sut.info, [], input=as_piped_input(input_text))
    assert result.output.replace(', \n', ',\n').encode() == expected.replace(', \n', ',\n').encode()
    assert result.exit_code == exit_code
