import sys

import pytest
from click_testing_utils import clirunner_invoke_piped

import clifunzone.txttool as sut
from clifunzone import txt_utils


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


@pytest.mark.parametrize("cli_args,expected", [
    ([], [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'Praesent quis erat vel ex egestas lobortis non nec augue.',
        'Etiam cursus nibh vel mattis cursus. Vivamus lectus erat, dictum et mauris eu, viverra tincidunt velit.',
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_lorem(cli_args, expected):
    clirunner_invoke_piped(sut.lorem, cli_args, exit_code=0, out_contains_seq=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ("Hi! How are you? My name is John-Paul. What's your name?", [], [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'Praesent quis erat vel ex egestas lobortis non nec augue.',
        'Etiam cursus nibh vel mattis cursus. Vivamus lectus erat, dictum et mauris eu, viverra tincidunt velit.',
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_split(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.split, cli_args, input_text, exit_code=0, out_contains_seq=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ("Hi! How are you? My name is John-Paul. What's your name?", [],
     "Hi!\nHow\nare\nyou?\nMy\nname\nis\nJohn-Paul.\nWhat's\nyour\nname?"),
    ("Hi! How are you? My name is John-Paul. What's your name?", ['-ss'],
     "Hi!\nHow\nare\nyou?\nMy\nname\nis\nJohn-Paul.\nWhat's\nyour\nname?"),
    ("Hi! How are you? My name is John-Paul. What's your name?", ['-sw'],
     "Hi\nHow\nare\nyou\nMy\nname\nis\nJohn-Paul\nWhat's\nyour\nname"),
    ("Hi! How are you? My name is John Paul. What is your name?", ['-sw'],
     "Hi\nHow\nare\nyou\nMy\nname\nis\nJohn\nPaul\nWhat\nis\nyour\nname"),
    ("Hi! How are you? My name is John-Paul. What's your name?", ['-sw', '-sep', ', '],
     "Hi, How, are, you, My, name, is, John-Paul, What's, your, name"),
    ("Hi! How are you? My name is John-Paul. What's your name?", ['-sw', '-sep', '|'],
     "Hi|How|are|you|My|name|is|John-Paul|What's|your|name"),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_split(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.split, cli_args, input_text, exit_code=0, out_eq=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('Lorem ipsum dolor sit amet', ['-v1', 'Lorem', '-v2', 'sit', '-v2', 'amet'],
     "{'max': 4, 'mean': 3.5, 'min': 3}"),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_distance(input_text, cli_args, expected):
    input_text = txt_utils.get_words(input_text)
    input_text = '\n'.join(input_text)
    clirunner_invoke_piped(sut.distance, cli_args, input_text, exit_code=0, out_eq=expected)


@pytest.mark.parametrize("cli_args,expected", [
    (['-v1', 'Lorem', '-v2', 'sit', '-v2', 'amet'],
     "{'max': 852, 'mean': 483.5, 'min': 3}"),
    (['-v1', 'lorem', '-v1', 'dolor', '-v2', 'consectetur', '-v2', 'adipiscing'],
     "{'max': 889, 'mean': 467.0740740740741, 'min': 3}"),
    (['-r', '-v1', '^Pellentesque$', '-v2', '^Vivamus'],
     "{'max': 528, 'mean': 222.66666666666666, 'min': 24}"),
    (['-r', '-ri', '-v1', '^Pellentesque$', '-v2', '^Vivamus'],
     "{'max': 910, 'mean': 287.1212121212121, 'min': 21}"),
    (['-v1', 'Lorem', '-v2', 'sit', '-v2', 'amet', '-v'],
     "{'max': 852, 'mean': 483.5, 'matches1': {'Lorem': set([0])}, " +
     "'matches2': {'amet': set([449, 386, 4, 722, 206, 50, 563, 852, 821, 787]), " +
     "'sit': set([448, 385, 3, 721, 205, 49, 562, 851, 820, 786])}, 'min': 3}"),
    (['-r', '-v1', '^Pellentesque$', '-v2', '^Vivamus', '-v'],
     "{'max': 528, 'mean': 222.66666666666666, 'matches1': {'Pellentesque': set([328, 99, 213, 478])}, " +
     "'matches2': {'Vivamus': set([45, 270, 143, 529, 627, 502])}, 'min': 24}"),
    (['-r', '-ri', '-v1', '^Pellentesque$', '-v2', '^Vivamus', '-v'],
     "{'max': 910, 'mean': 287.1212121212121, 'matches1': {'pellentesque': set([406, 839, 329, 207, 182, 24, 955]), " +
     "'Pellentesque': set([328, 99, 213, 478])}, " +
     "'matches2': {'Vivamus': set([45, 270, 143, 529, 627, 502])}, 'min': 21}"),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_distance_lorem(cli_args, expected):
    input_text = txt_utils.lorem_ipsum()
    input_text = txt_utils.get_words(input_text)
    input_text = '\n'.join(input_text)
    clirunner_invoke_piped(sut.distance, cli_args, input_text, exit_code=0, out_eq=expected)
