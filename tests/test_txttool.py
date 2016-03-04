import sys

import pytest

import clifunzone.txttool as sut
from click_testing_utils import clirunner_invoke_piped


def test_none():
    expected = 'I was invoked without a subcommand...'
    clirunner_invoke_piped(sut.cli, [], '', exit_code=0, out_ok=expected)


def test_none_debug():
    expected = [
        '',
        "ctx:",
        "{'_close_callbacks': [],",
        " '_depth': 2,",
        " '_meta': {},",
        " 'allow_extra_args': True,",
        " 'allow_interspersed_args': False,",
        " 'args': [],",
        " 'auto_envvar_prefix': None,",
        " 'color': None,",
        " 'command': <click.core.Group object at 0x10c6d5ed0>,",
        " 'default_map': None,",
        " 'help_option_names': ['-h', '--help'],",
        " 'ignore_unknown_options': False,",
        " 'info_name': 'cli',",
        " 'invoked_subcommand': None,",
        " 'max_content_width': None,",
        " 'obj': None,",
        " 'params': {'debug': True},",
        " 'parent': None,",
        " 'protected_args': [],",
        " 'resilient_parsing': False,",
        " 'terminal_width': None,",
        " 'token_normalize_func': None}",
        '',
        'I was invoked without a subcommand...',
        'Debug mode: enabled',
        '',
        "ctx:",
        "{'_close_callbacks': [],",
        " '_depth': 2,",
        " '_meta': {},",
        " 'allow_extra_args': True,",
        " 'allow_interspersed_args': False,",
        " 'args': [],",
        " 'auto_envvar_prefix': None,",
        " 'color': None,",
        " 'command': <click.core.Group object at 0x10c6d5ed0>,",
        " 'default_map': None,",
        " 'help_option_names': ['-h', '--help'],",
        " 'ignore_unknown_options': False,",
        " 'info_name': 'cli',",
        " 'invoked_subcommand': None,",
        " 'max_content_width': None,",
        " 'obj': None,",
        " 'params': {'debug': True},",
        " 'parent': None,",
        " 'protected_args': [],",
        " 'resilient_parsing': False,",
        " 'terminal_width': None,",
        " 'token_normalize_func': None}",
        '',
        'kwargs: {}',
        'subcommand: None'
    ]
    clirunner_invoke_piped(sut.cli, ['-d'], '', exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text", [
    '<abc/>',
    '{"abc": null}',
    'abc',
    'Hi. How are you? My name is John. What is your name?'
])
def test_echo(input_text):
    expected = input_text or ['']
    clirunner_invoke_piped(sut.echo, [], input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('abc', ['-oj'], [
        '{',
        '  "content": {',
        '    "length": 3,',
        '    "metrics": {',
        '      "chars": {',
        '        "counts": {',
        '          "distinct": 3,',
        '          "each": {',
        '            "a": 1,',
        '            "b": 1,',
        '            "c": 1',
        '          },',
        '          "total": 3',
        '        }',
        '      },',
        '      "words": {',
        '        "counts": {',
        '          "distinct": 1,',
        '          "each": {',
        '            "abc": 1',
        '          },',
        '          "total": 1',
        '        }',
        '      }',
        '    }',
        '  }',
        '}'
    ]),
    ('<abc/>', ['-od'], [
        "{'content': OrderedDict([('length', 6), ('metrics', {" +
        "'chars': {'counts': {'distinct': 6, 'total': 6, " +
        "'each': OrderedDict([('/', 1), ('<', 1), ('>', 1), ('a', 1), ('b', 1), ('c', 1)])}}, " +
        "'words': {'counts': {'distinct': 1, 'total': 1, 'each': OrderedDict([('abc', 1)])}}})])}"
    ]),
    ('{"abc": null}', ['-od'], [
        "{\'content\': OrderedDict([(\'length\', 13), (\'metrics\', {\'chars\': {" +
        "\'counts\': {\'distinct\': 11, \'total\': 13, " +
        "\'each\': OrderedDict([(\' \', 1), (\'\"\', 2), (\':\', 1), (\'a\', 1), (\'b\', 1), (\'c\', 1), (\'l\', 2), " +
        "(\'n\', 1), (\'u\', 1), (\'{\', 1), (\'}\', 1)])}}, " +
        "\'words\': {\'counts\': {\'distinct\': 2, \'total\': 2, " +
        "\'each\': OrderedDict([(\'abc\', 1), (\'null\', 1)])}}})])}"
    ]),
    ('{"abc": null}', ['-f'], [
        '{',
        '  "content_length": 13,',
        '  "content_metrics_chars_counts_distinct": 11,',
        '  "content_metrics_chars_counts_each_ ": 1,',
        '  "content_metrics_chars_counts_each_\\"": 2,',
        '  "content_metrics_chars_counts_each_:": 1,',
        '  "content_metrics_chars_counts_each_a": 1,',
        '  "content_metrics_chars_counts_each_b": 1,',
        '  "content_metrics_chars_counts_each_c": 1,',
        '  "content_metrics_chars_counts_each_l": 2,',
        '  "content_metrics_chars_counts_each_n": 1,',
        '  "content_metrics_chars_counts_each_u": 1,',
        '  "content_metrics_chars_counts_each_{": 1,',
        '  "content_metrics_chars_counts_each_}": 1,',
        '  "content_metrics_chars_counts_total": 13,',
        '  "content_metrics_words_counts_distinct": 2,',
        '  "content_metrics_words_counts_each_abc": 1,',
        '  "content_metrics_words_counts_each_null": 1,',
        '  "content_metrics_words_counts_total": 2',
        '}'
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_info(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.info, cli_args, input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('Hi! How are you? My name is John Paul. What is your name?', ['-f'], [
        '"content_length": 57,',
        '"content_metrics_chars_counts_distinct": 20,',
        '"content_metrics_chars_counts_each_ ": 12,',
        '"content_metrics_chars_counts_each_y": 3,',
        '"content_metrics_chars_counts_total": 57,',
        '"content_metrics_words_counts_distinct": 11,',
        '"content_metrics_words_counts_each_is": 2,',
        '"content_metrics_words_counts_each_john": 1,',
        '"content_metrics_words_counts_each_name": 2,',
        '"content_metrics_words_counts_each_paul": 1,',
        '"content_metrics_words_counts_each_what": 1,',
        '"content_metrics_words_counts_total": 13'
    ]),
    ("Hi! How are you? My name is John-Paul. What's your name?", ['-f'], [
        '"content_length": 56,',
        '"content_metrics_chars_counts_distinct": 22,',
        '"content_metrics_chars_counts_each_ ": 10,',
        '"content_metrics_chars_counts_each_!": 1,',
        '"content_metrics_chars_counts_each_\'": 1,',
        '"content_metrics_chars_counts_total": 56,',
        '"content_metrics_words_counts_distinct": 10,',
        '"content_metrics_words_counts_each_is": 1,',
        '"content_metrics_words_counts_each_john-paul": 1,',
        '"content_metrics_words_counts_each_name": 2,',
        '"content_metrics_words_counts_each_what\'s": 1,',
        '"content_metrics_words_counts_total": 11'
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_info_fragments(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.info, cli_args, input_text, exit_code=0, out_contains_seq=expected)
