import pytest

import clifunzone.rfxmltool as sut
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
    clirunner_invoke_piped(sut.echo, [], input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('<abc/>', '{"robot":{"messages":0,"suites":0,"tests":0},"xml":{"content":{"tag":"abc"},"metrics":{}}}'),
    ('<a>\t<b><c/> </b></a>',
     '{"robot":{"messages":0,"suites":0,"tests":0},' +
     '"xml":{"content":{"#text":"\\t","tag":"a"},"metrics":{"children":{"attributes":[],"count":1,"tags":["b"]},' +
     '"descendants":{"attributes":[],"count":2,"tags":["b","c"]}}}}')
])
def test_info(input_text, expected):
    clirunner_invoke_piped(sut.info, [], input_text, exit_code=0, out_json=expected)


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
