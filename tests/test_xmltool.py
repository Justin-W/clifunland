import sys

import pytest
from click_testing_utils import clirunner_invoke_piped

import clifunzone.xmltool as sut


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


@pytest.mark.parametrize("input_text,exit_code,expected", [
    ('<abc/>', 0, 'True'),
    ('<a>\n<b/>\n</a>', 0, 'True'),
    ('<a>\n<b><c/> </b></a>', 0, 'True'),
    ('<a>\t<b><c/> </b></a>', 0, 'True'),
    ('', 1, 'False'),
    (' ', 1, 'False'),
    ('<<<', 1, 'False'),
    ('>', 1, 'False'),
    ('<a>', 1, 'False'),
    ('abc', 1, 'False'),
    ('{"a": null}', 1, 'False')
])
def test_validate(input_text, exit_code, expected):
    clirunner_invoke_piped(sut.validate, [], input_text, exit_code=exit_code, out_ok=expected)


@pytest.mark.parametrize("input_text,expected", [
    ('<abc/>', [
        '{"abc":null}'
    ]),
    ('<a>\t<b><c/> </b></a>', [
        '{"a":{"#text":"\\t","b":{"c":{"#tail":" "}}}}'
    ])
])
def test_parse(input_text, expected):
    clirunner_invoke_piped(sut.parse, [], input_text, exit_code=0, out_json=expected)


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


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', [], '{"abc": null}'),
    ('<abc/>', ['-p'], [
        '{',
        '    "abc": null',
        '}'
    ]),
    ('<a>\n<b/>\n</a>', ['-p', '-sws'], [
        '{',
        '    "a": {',
        '        "b": null',
        '    }',
        '}'
    ]),
    ('<a>\n<b/>\n</a>', [], '{"a": {"b": {"#tail": "\\n"}, "#text": "\\n"}}'),
    ('<a>\n<b/>\n</a>', ['-sws'], '{"a": {"b": null}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', [],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#tail": " ", "#text": " hi\\t"}, '
     '"#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sws'],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#text": "hi"}}}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sa'],
     '{"a": {"b": {"c": {"#tail": " ", "#text": " hi\\t"}, "#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sns'],
     '{"a": {"@id": "1", "b": {"@id": "2", "c": {"@y": "a", "@x": "", "@z": "0", "#tail": " ", "#text": " hi\\t"}, '
     '"#text": "\\t"}, "#text": "\\t"}}'),
    ('<a id="1">\t<b id="2">\t<c x="" y="a" z="0"> hi\t</c> </b></a>', ['-sws', '-sa', '-sns'], [
        '{"a": {"b": {"c": "hi"}}}'
    ])
])
def test_tojson(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.tojson, cli_args, input_text, exit_code=0, out_json=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', ['--echo'], [
        '',
        'XML:',
        '<abc/>',
        '',
        'JSON:',
        '{"abc": null}'
    ])
])
def test_tojson_echo(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.tojson, cli_args, input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_tojson_invalid_input(input_text):
    clirunner_invoke_piped(sut.tojson, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<abc/>', [], ['{"path":"/abc","content":{"tag":"abc"}}']),
    ('<a/>', ['-p'],
     '[\n    {\n        "path": "/a",\n        "content": {\n            "tag": "a"\n        }\n    }\n]')
])
def test_elements(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.elements, cli_args, input_text, exit_code=0, out_json=expected)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<a>\t<b><c/> </b></a>', [], [
        '{"path":"/a","content":{"tag":"a","#text":"\\t"},' +
        '"metrics":{"children":{"count":1,"tags":["b"]},"descendants":{"count":2,"tags":["b","c"]}}}',
        '{"path":"/a/b","content":{"tag":"b"},' +
        '"metrics":{"children":{"count":1,"tags":["c"]},"descendants":{"count":1,"tags":["c"]}}}',
        '{"path":"/a/b/c","content":{"tag":"c"}}'
    ])
])
@pytest.mark.skipif(sys.version_info > (3, 3),
                    reason="fails on the py35 travis build")
def test_elements_as_lines(input_text, cli_args, expected):
    # expected = '{"output":{[%s]}}' % ','.join(expected)
    # expected = '[%s]' % ','.join(expected)
    clirunner_invoke_piped(sut.elements, cli_args, input_text, exit_code=0, out_ok=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_elements_invalid_input(input_text):
    clirunner_invoke_piped(sut.elements, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<a>\t<b> <c/> hi \t</b></a>', ['-w'], '<a><b><c/> hi \t</b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b/d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e'], '<a><b><c/></b><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b/c'], '<a><b/><b><d><e/></d><d/></b></a>'),
    ('<a><b>1</b><b><c/></b><b><d><e/></d><d/></b></a>', ['-e'], '<a><b>1</b></a>'),
    ('<a><b>1</b><b><c/>2</b><b><d><e>2</e></d></b></a>', ['-x //b/c', '-e'], '<a><b>1</b><b><d><e>2</e></d></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e', '-x //b/c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-t d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-t e', '-t c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d/e', '-t c'], '<a><b/><b><d/><d/></b></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', [], '<a>t<b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-e'], '<a>t<b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ea'], '<a>t<b b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes'], '<a>t<b/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-text'], '<a><b e="" b="False" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab'], '<a>t<b e="" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-av', 'False'], '<a>t<b e="" i="0"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-av', '0'], '<a>t<b e="" b="False"/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai'], '<a>t<b e=""/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai', '-e'], '<a>t<b e=""/></a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['-ab', '-ai', '-ea', '-e'], '<a>t</a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes', '-e'], '<a>t</a>'),
    ('<a>t<b e="" b="False" i="0"/></a>', ['--all-attributes', '--all-text', '-e'], '<a></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //b'], '<a/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d'], '<a><b><c/></b><b/></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[1]'], '<a><b><c/></b><b><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[2]'], '<a><b><c/></b><b><d><e/></d></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[5]'], '<a><b><c/></b><b><d><e/></d><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)<=1]'], '<a><b id="b2"/></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(*)=0]'],
     '<a><b id="b1"/><b id="b2"><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)<1]'],
     '<a><b id="b1"/><b id="b2"><d/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x //*[count(.//*)=3]'],
     '<a><b id="b1"><c/></b></a>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-x /*//*[count(./*)=2]'],
     '<a><b id="b1"><c/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[count(*)>=1]'], '<a><b><c/></b><b><d/></b></a>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-x //d[count(*)!=1]'], '<a><b><c/></b><b><d><e/></d></b></a>')
])
def test_strip(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.strip, cli_args, input_text, exit_code=0, out_xml=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_strip_invalid_input(input_text):
    clirunner_invoke_piped(sut.strip, [], input_text, exit_code=-1, out_ok=None)


@pytest.mark.parametrize("input_text,cli_args,expected", [
    ('<a><b><c/></b></a>', [], '<results>\n</results>'),
    ('<a><b><c/></b></a>', ['-nr'], ''),
    ('<a><b><c/></b></a>', ['-x //b'], '<results>\n<b><c/></b>\n</results>'),
    ('<a><b><c/></b></a>', ['-x //b', '-nr'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b'],
     '<R>\n<b><c/></b>\n<b><d><e/></d><d/></b>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[position()=1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[2]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[last()]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b[position()=2]'], '<b><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d/e'], '<e/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //b/c/parent::*'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d/e/parent::*'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //*[count(./c)=1]'], '<b><c/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(./c|./e)=1]'],
     '<R>\n<b><c/></b>\n<d><e/></d>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>', ['-nr', '-x //b[@z="1"]'],
     '<b z="1"><c/></b>'),
    ('<a><b z="1"><c/></b><b z="2"><d><e z="1"/></d><d/></b></a>', ['-rR', '-x //*[@z="1"]'],
     '<R>\n<b z="1"><c/></b>\n<e z="1"/>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-rR', '-x //*[@z="1"]'],
     '<R>\n<b z="1"><c/></b>\n<d z="1"><e z="2"/></d>\n</R>'),
    ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-rR', '-x //*[@z and @z!="2"]'],
     '<R>\n<b z="1"><c/></b>\n<d z="1"><e z="2"/></d>\n</R>'),
    # ('<a><b z="1"><c/></b><b z="2"><d z="1"><e z="2"/></d></b></a>', ['-nr', '-x //*[@z="1" and position()>2]'],
    #  '<d z="1"><e z="2"/></d>'),
    ('<z><a>1a1</a><b>2b1</b><c>3c1</c><a>4a2</a><b>5b2</b><c>6c2</c><a>7a3</a></z>',
     ['-rR', '-x //*[contains(text(),"3")]'],
     '<R>\n<c>3c1</c>\n<a>7a3</a>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b/d'], '<R>\n<d><e/></d>\n<d/>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //b'], '<R>\n<b><c/></b>\n<b><d><e/></d><d/></b>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //d'], '<R>\n<d><e/></d>\n<d/>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[1]'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[2]'], '<d/>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-rR', '-x //d[5]'], '<R>\n</R>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[5]'], ''),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(.//*)<=1]'],
     '<R>\n<b id="b1"><c/></b>\n<c/>\n<d><e/></d>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(*)=0]'],
     '<R>\n<c/>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-rR', '-x //*[count(.//*)<1]'],
     '<R>\n<c/>\n<e/>\n<d/>\n</R>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[count(.//*)=3]'],
     '<b id="b2"><d><e/></d><d/></b>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x /*//*[count(./*)=2]'],
     '<b id="b2"><d><e/></d><d/></b>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[count(*)>=1]'], '<d><e/></d>'),
    ('<a><b><c/></b><b><d><e/></d><d/></b></a>', ['-nr', '-x //d[count(*)!=1]'], '<d/>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]'],
     '<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]'],
     '<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //b[@id="b1"]'],
     '<b id="b1"><c/></b>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //b[@id="b1"]', '-x //*[./e]'],
     '<b id="b1"><c/></b>\n<d><e/></d>'),
    ('<a><b id="b1"><c/></b><b id="b2"><d><e/></d><d/></b></a>', ['-nr', '-x //*[./e]', '-x //b[@id="b1"]'],
     '<d><e/></d>\n<b id="b1"><c/></b>'),
])
def test_find(input_text, cli_args, expected):
    clirunner_invoke_piped(sut.find, cli_args, input_text, exit_code=0, out_xml=expected)


@pytest.mark.parametrize("input_text", [
    '',
    ' ',
    '<<<',
    '>',
    '<a>',
    'abc',
    '{"a": null}'
])
def test_find_invalid_input(input_text):
    clirunner_invoke_piped(sut.find, [], input_text, exit_code=-1, out_ok=None)
