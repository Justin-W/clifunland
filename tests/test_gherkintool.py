import sys

import pytest

import clifunzone.gherkintool as sut
from click_testing_utils import clirunner_invoke_piped
from clifunzone import txt_utils


def test_none():
    expected = []
    clirunner_invoke_piped(sut.cli, [], '', exit_code=0, out_ok=expected)


def test_none_debug():
    expected = []
    clirunner_invoke_piped(sut.cli, ['-d'], '', exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text", [
    'Feature: abc\nScenario: def\n',
    '<abc/>',
    '{"abc": null}',
    'abc',
    'Hi. How are you? My name is John. What is your name?'
])
def test_echo(input_text):
    expected = input_text or ['']
    clirunner_invoke_piped(sut.echo, [], input_text, exit_code=0, out_ok=expected)


# @pytest.mark.parametrize("input_text,cli_args,expected", [
# ])
# def test_parse(input_text, cli_args, expected):
#     clirunner_invoke_piped(sut.parse, cli_args, input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_parse_invalid_input(input_text):
    clirunner_invoke_piped(sut.parse, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('Feature: abc\nScenario: def\nGiven a gift\nAnd I am polite\nWhen you can\nThen send a thank you note\n', [], [
        '  "text": "a gift", ',
        '  "text": "I am polite", ',
        '  "text": "you can", ',
        '  "text": "send a thank you note", ',
    ]),
    ('Feature: abc\nScenario: def\n', [], [
        '{',
        '  "type": "Feature"',
        '  "location": {',
        '    "column": 1,',
        '    "line": 1',
        '  },',
        '  "language": "en",',
        '  "scenarioDefinitions": [',
        '    {',
        '      "type": "Scenario"',
        '      "location": {',
        '        "column": 1,',
        '        "line": 2',
        '      },',
        '      "steps": [],',
        '      "name": "def",',
        '      "keyword": "Scenario",',
        '      "tags": []',
        '    }',
        '  ],',
        '  "comments": [],',
        '  "name": "abc",',
        '  "keyword": "Feature",',
        '  "tags": []',
        '}'
    ]),
    ('Feature: abc\nScenario: def\n', ['-s'], [
        '{',
        '  "comments": [],',
        '  "keyword": "Feature",',
        '  "language": "en",',
        '  "location": {',
        '    "column": 1,',
        '    "line": 1',
        '  },',
        '  "name": "abc",',
        '  "scenarioDefinitions": [',
        '    {',
        '      "keyword": "Scenario",',
        '      "location": {',
        '        "column": 1,',
        '        "line": 2',
        '      },',
        '      "name": "def",',
        '      "steps": [],',
        '      "tags": [],',
        '      "type": "Scenario"',
        '    }',
        '  ],',
        '  "tags": [],',
        '  "type": "Feature"',
        '}'
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_parse_fragments(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.parse, cli_args, input_text, exit_code=0, out_contains_seq=expected)


# @pytest.mark.parametrize("input_text,cli_args,expected", [
# ])
# def test_info(input_text, cli_args, expected):
#     clirunner_invoke_piped(sut.info, cli_args, input_text, exit_code=0, out_ok=expected)


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
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('Feature: abc\nScenario: def\nGiven a gift\nAnd I am polite\nWhen you can\nThen send a thank you note\n', [], [
        '  "content": {',
        '    "Scenarios": [',
        '      "def"',
        '  "count": {',
        '    "Types": {',
        '      "Feature": 1,',
        '      "Scenario": 1,',
        '      "Step": 4\n',
    ]),
    ('Feature: abc\nScenario: def\n', [], [
        '{',
        '  "content": {',
        '    "Scenarios": [',
        '      "def"',
        '  "count": {',
        '    "Types": {',
        '      "Feature": 1,',
        '      "Scenario": 1\n',
        '}'
    ]),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_info_fragments(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.info, cli_args, input_text, exit_code=0, out_contains_seq=expected)
