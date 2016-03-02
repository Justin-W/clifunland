import re


def munge_object_mem_refs(s, replacement=None):
    """
    Replaces all occurrences of 'raw object instance' references in a specified string.

    Since such raw instance references contain runtime-variable content that complicate automated testing,
    this function can be used to convert the runtime-variable portions of the text into static, predictable content.

    E.g. Can convert text fragments such as '<abcd.efg.HiClass object at 0x109abcdef>' into
    '<abcd.efg.HiClass object at 0x...>'.

    :param s: the string content to munge.
    :param replacement: the replacement content. Defaults to '...'.
    :return: a string containing the munged input text.

    >>> munge_object_mem_refs(None) is None
    True

    >>> munge_object_mem_refs('')
    ''

    >>> munge_object_mem_refs('abc')
    'abc'

    >>> munge_object_mem_refs('<abcd.efg.HiClass object at 0x102345678>')
    '<abcd.efg.HiClass object at 0x...>'

    >>> munge_object_mem_refs('<abcd.efg.HiClass object at 0x109abcdef>')
    '<abcd.efg.HiClass object at 0x...>'

    >>> munge_object_mem_refs('<abcd.efg.HiClass object at 0x109ABCDEF>')
    '<abcd.efg.HiClass object at 0x...>'

    >>> munge_object_mem_refs('<abcd.efg.HiClass object at 0x109abcdef>', '0'*9)
    '<abcd.efg.HiClass object at 0x000000000>'

    >>> munge_object_mem_refs('<abcd.efg.HiClass object at 0x102345678>, <my.pkg.MyClass object at 0x109abcdef>')
    '<abcd.efg.HiClass object at 0x...>, <my.pkg.MyClass object at 0x...>'

    >>> munge_object_mem_refs('AAA object at 0x109abcdef>ZZZ')
    'AAA object at 0x...>ZZZ'

    >>> munge_object_mem_refs('AAAobject at 0x109abcdef>ZZZ')
    'AAAobject at 0x109abcdef>ZZZ'

    >>> munge_object_mem_refs('AAA object at 0x109abcdefZZZ')
    'AAA object at 0x109abcdefZZZ'

    >>> munge_object_mem_refs('AAA Object at 0x109abcdef>ZZZ')
    'AAA Object at 0x109abcdef>ZZZ'

    >>> munge_object_mem_refs('AAA object at 0x109abcdeg>ZZZ')
    'AAA object at 0x109abcdeg>ZZZ'

    >>> munge_object_mem_refs('AAA object at 0x109abcde>ZZZ')
    'AAA object at 0x109abcde>ZZZ'

    >>> munge_object_mem_refs('AAA object at 0x109abcdef0>ZZZ')
    'AAA object at 0x109abcdef0>ZZZ'

    """
    if s is None:
        return None
    if not replacement:
        replacement = '...'
        # replacement = '0'*9
        # replacement = ''
    # pattern = r' object at 0x[0-9a-fA-F]+'
    # pattern = r' object at 0x[0-9a-fA-F]+>'
    pattern = r' object at 0x[0-9a-fA-F]{9}>'
    repl = ' object at 0x{}>'.format(replacement)
    return re.sub(pattern, repl, s)
