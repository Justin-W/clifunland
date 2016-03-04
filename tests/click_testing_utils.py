import json
import logging

from click._compat import PY2
from click.testing import CliRunner

from clifunzone.reflection_utils import is_string
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


def assert_out_contains(actual, expected, encode=True, sequential=False):
    """
    Utility assertion function. Helps keep the test code cleaner.

    :param actual:
    :param expected: a string or iterable of strings representing 1+ substrings that the output string should contain.
    :param encode:
    :param strict:
    :param sequential:
    """
    __tracebackhide__ = True
    if expected is None:
        expected = []
    elif is_string(expected):
        expected = [expected]
    if encode:
        if actual is not None:
            actual = actual.encode()
    if sequential:
        pos = 0
        for i, s in enumerate(expected):
            if encode:
                if s is not None:
                    s = s.encode()
            try:
                pos2 = actual.index(s, pos)
                # move pos to the beginning of the current match
                pos = pos2
            except ValueError:
                msg = "Expected #{index} not found in Actual[{start}:{end}]." + \
                      "\nExpected #{index}: ({value})." + \
                      "\nActual: ...{actual}..."
                # TODO: set max_actual dynamically based on the verbosity setting
                # max_actual = 80
                max_actual = 800
                assert False, msg.format(index=repr(i), value=repr(s), start=repr(pos), end=repr(len(actual)),
                                         actual=repr(actual[pos:pos + max_actual]))

            # Note: if we disallow nested substrings here, it would make sense to do so when sequential==False, too.
            # # move pos to the end of the current match (so that nested substrings are ignored)
            # pos += len(s)
    else:
        for s in expected:
            assert s in actual


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


def clirunner_invoke_piped(cli, args, input_text=None,
                           runner=None,
                           exit_code=None,
                           out_eq=None, out_ok=None, out_contains=None, out_contains_seq=None,
                           out_json=None, out_xml=None):
    """
    Invokes a CLI command (using <CliRunner>) in a way that simulates 'piped input',
    and (conditionally) performs various assertions on the exit code and output.

    E.g. Can simulate CLI commands such as:
    $ cat my.txt | python -m mypkg.mycli

    :param cli: the CLI function (i.e. click command) to invoke.
    :param args: the CLI args to pass to the cli command.
    :param input_text: a string or a list of strings.
        If passed, the strings will be passed to the invoked command in a way that simulates 'piped input'.
    :param runner: optional. a <CliRunner> instance. Allows the caller to reuse or configure the CliRunner instance.
    :param exit_code: the expected exit code.
    :param out_eq: the expected output.
        The actual output will be compared to this using assert_out_eq().
    :param out_ok: the expected output.
        The actual output will be compared to this using assert_out_ok().
    :param out_contains: the expected output.
        The actual output will be compared to this using out_contains(sequential=False).
    :param out_contains_seq: the expected output.
        The actual output will be compared to this using out_contains(sequential=True).
    :param out_json: the expected output.
        The actual output will be compared to this using assert_json_eq().
        E.g. Differences between actual and expected output 'irrelevant' to the JSON format may be ignored.
    :param out_xml: the expected output.
        The actual output will be compared to this using assert_out_ok().
        (Note: This param currently behaves identically to the out_ok param.
        However, in the future it may trigger the use of more XML-specific comparisons.
        E.g. Differences between actual and expected output 'irrelevant' to the XML format may be ignored.)
    :return: the value returned by invoking CliRunner().invoke(...).
    """
    if input_text is not None:
        log.debug('input_text=%s' % repr(input_text))
    if not runner:
        runner = CliRunner()
    input_stream = as_piped_input(input_text) if input_text is not None else None
    result = runner.invoke(cli, args, input=input_stream)
    actual = result.output
    log.debug('actual output=%s' % repr(actual))
    # if result.exc_info:
    #     log.info('actual exception info:%s.' % str(result.exc_info), exc_info=result.exc_info)
    if exit_code is not None:
        assert_exit_code(result.exit_code, exit_code)
    if out_eq is not None:
        assert_out_eq(actual, out_eq)
    if out_ok is not None:
        assert_out_ok(actual, out_ok)
    if out_contains is not None:
        assert_out_contains(actual, out_contains, sequential=False)
    if out_contains_seq is not None:
        assert_out_contains(actual, out_contains_seq, sequential=True)
    if out_json is not None:
        assert_json_eq(actual, out_json)
    if out_xml is not None:
        # assert_xml_eq(result.output, out_xml)
        assert_out_ok(actual, out_xml)
    return result
