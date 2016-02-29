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
