import json
import logging

from click._compat import PY2
from click.testing import CliRunner

from testing_utils import munge_object_mem_refs

# Use the most reasonable io that users would use for the python version.
if PY2:
    from cStringIO import StringIO as ReasonableBytesIO
    # from StringIO import StringIO as ReasonableStringIO
else:
    from io import BytesIO as ReasonableBytesIO
    # from io import StringIO as ReasonableStringIO


log = logging.getLogger(__name__)


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
    munge_json = not strict
    munge_mem_refs = not strict
    if expected is None:
        expected = ''
    if isinstance(expected, list):
        # treat the list as a list of output lines
        expected = '\n'.join(expected)
    if output_expected:
        # automatically add a trailing newline only if some output is expected
        expected += '\n'
    if munge_json:
        actual = py3_json_agnostic(actual)
        expected = py3_json_agnostic(expected)
    if munge_mem_refs:
        actual = munge_object_mem_refs(actual)
        expected = munge_object_mem_refs(expected)
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
        log.exception('json.loads() error.\nactual=%s.\nexpected=%s.', actual, expected)
        raise

    # if not strict:
    try:
        actual = json.dumps(actual, sort_keys=True, separators=(',', ':'))
        expected = json.dumps(expected, sort_keys=True, separators=(',', ':'))
    except ValueError:
        log.exception('json.dumps() error.\nactual=%s.\nexpected=%s.', actual, expected)
        raise
    # else:
    #     actual = json.dumps(actual, sort_keys=False, separators=(',', ':'))
    #     expected = json.dumps(expected, sort_keys=False, separators=(',', ':'))

    assert actual == expected


def py3_json_agnostic(s):
    return s.replace(', \n', ',\n')


def as_piped_input(input_text):
    # return PipedInput(input_text)
    # return ReasonableBytesIO(input_text)
    return ReasonableBytesIO(input_text.encode())
    # return ReasonableBytesIO(input_text.encode('utf-8'))


def clirunner_invoke_piped(cli, args, input_text, exit_code=None,
                           out_ok=None, out_json=None, out_xml=None):
    """
    Invokes a CLI command (using <CliRunner>) in a way that simulates 'piped input',
    and (conditionally) performs various assertions on the exit code and output.

    E.g. Can simulate CLI commands such as:
    $ cat my.txt | python -m mypkg.mycli

    :param cli: the CLI function (i.e. click command) to invoke.
    :param args: the CLI args to pass to the cli command.
    :param input_text: a string or a list of strings.
    :param exit_code: the expected exit code.
    :param out_ok: the expected output.
        The actual output will be compared to this using plain text comparisons.
    :param out_json: the expected output.
        The actual output will be compared to this using JSON comparisons.
        E.g. Differences between actual and expected output 'irrelevant' to the JSON format may be ignored.
    :param out_xml: the expected output.
        The actual output will be compared to this using XML comparisons.
        E.g. Differences between actual and expected output 'irrelevant' to the XML format may be ignored.
    :return: the value returned by invoking CliRunner().invoke(...).
    """
    runner = CliRunner()
    result = runner.invoke(cli, args, input=as_piped_input(input_text))
    if out_ok is not None:
        assert_out_ok(result.output, out_ok)
    if out_json is not None:
        assert_json_eq(result.output, out_json)
    if out_xml is not None:
        # assert_xml_eq(result.output, out_xml)
        assert_out_ok(result.output, out_xml)
    if exit_code is not None:
        assert_exit_code(result.exit_code, exit_code)
    return result
