import sys

import pytest

import clifunzone.jsontool as sut
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
    '{"a": null}',
    '{"a": 0}',
    '{"a": {"b": [{"c": 0}, {"d": 1}]}}',
    '',
    ' ',
    '{{{',
    '}',
    '{a}',
    'abc',
    '<abc/>'
])
def test_echo(input_text):
    expected = input_text or ['']
    clirunner_invoke_piped(sut.echo, [], input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text,exit_code,expected", [
    ('{"a": null}', 0, "OrderedDict([(u'a', None)])"),
    ('{"a": 0}', 0, "OrderedDict([(u'a', 0)])"),
    ('{"a": {"b": [{"c": 0}, {"d": 1}]}}', 0,
     "OrderedDict([(u'a', OrderedDict([(u'b', [OrderedDict([(u'c', 0)]), OrderedDict([(u'd', 1)])])]))])"),
    ('', -1, None),
    (' ', -1, None),
    ('{{{', -1, None),
    ('}', -1, None),
    ('{a}', -1, None),
    ('abc', -1, None),
    ('<abc/>', -1, None)
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_repr(input_text, exit_code, expected):
    clirunner_invoke_piped(sut.reprcommand, [], input_text, exit_code=exit_code, out_ok=expected)


@pytest.mark.parametrize("input_text,exit_code,expected", [
    ('{"a": null}', 0, 'True'),
    ('{"a": 0}', 0, 'True'),
    ('{"a": {"b": [{"c": 0}, {"d": 1}]}}', 0, 'True'),
    ('', 1, 'False'),
    (' ', 1, 'False'),
    ('{{{', 1, 'False'),
    ('}', 1, 'False'),
    ('{a}', 1, 'False'),
    ('abc', 1, 'False'),
    ('<abc/>', 1, 'False')
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_validate(input_text, exit_code, expected):
    clirunner_invoke_piped(sut.validate, [], input_text, exit_code=exit_code, out_ok=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('{"a": null}', '{"keys":["a"],"length":1}'),
    ('{"a": {"b": [{"c": 0}, {"d": 1}]}}', '{"keys":["a"],"length":1}')
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_info(input_text, expected):
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=0, out_json=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '{{{',
    '}',
    '{a}',
    'abc',
    '<abc/>'
])
def test_info_invalid_input(input_text):
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,template,expected", [
    ('{"p": "Jay", "g": "Hi"}', '{{g}} {{p}}!', 'Hi Jay!'),
    ('{"p": "J", "g": {"e": "Hi", "s": "Hola"}}', '{{g.e}} {{p}}!', 'Hi J!'),
    ('{"p": "J", "g": {"e": "Hi", "s": "Hola"}}', '{{g.s}} {{p}}!', 'Hola J!'),
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="currently broken for py35")
def test_mustache(input_text, template, expected):
    clirunner_invoke_piped(sut.mustache, ['-s', template], input_text, exit_code=0, out_eq=expected)
