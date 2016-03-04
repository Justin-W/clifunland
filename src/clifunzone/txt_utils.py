import re
from collections import Counter
from collections import OrderedDict


def get_info(s):
    """
    Returns a dict with (incomplete) info about a specified string.

    :param s: a string.
    :return: a <collections.OrderedDict> instance.
    """

    def get_distinct_tokens(tokens, ignore_case=False):
        if ignore_case:
            # convert to tag names
            tokens = [t.lower() for t in tokens]
        # filter out duplicates
        tokens = set(tokens)
        return tokens

    def get_tokens_info(tokens):
        d = {}
        d.update({'total': len(tokens)})
        ctr = Counter(tokens)
        d.update({'distinct': len(ctr.keys())})
        d.update({'each': OrderedDict(sorted(ctr.items()))})
        d = {'counts': d}
        return d

    d = OrderedDict()

    d.update({'length': len(s)})

    if not s:
        return d

    # d2 = {}
    # d2.update({'words': (get_distinct_tokens(s.split(' ,.'), ignore_case=True))})
    # d2.update({'sentences': (get_distinct_tokens(sentences, ignore_case=True))})
    # d['content'] = d2

    d['metrics'] = {}

    # get all chars
    tokens = list(s)
    tokens = [t.lower() for t in tokens]
    d['metrics']['chars'] = get_tokens_info(tokens)

    # get all words
    tokens = get_words(s)
    tokens = [t.lower() for t in tokens]
    d['metrics']['words'] = get_tokens_info(tokens)

    # # get all words
    # tokens = get_words(s)
    # if tokens:
    #     d2 = {'count': len(tokens)}
    #     tokens = get_distinct_tokens(tokens, ignore_case=True)
    #     d2.update({'count_distinct': (len(tokens))})
    #     d2.update({'distinct': (sorted(tokens))})
    #     d['metrics']['words'] = d2

    # # get all sentences
    # tokens = get_sentences(s)
    # if tokens:
    #     d2 = {'count': len(tokens)}
    #     tokens = get_distinct_tokens(tokens, ignore_case=True)
    #     d2.update({'count_distinct': (len(tokens))})
    #     d2.update({'distinct': (sorted(tokens))})
    #     d['metrics']['sentences'] = d2

    return d


def get_words(s):
    """

    :param s:
    :return:

    >>> get_words("Hi! My name is Anne-Marie. What is yours?")
    ['Hi', 'My', 'name', 'is', 'Anne-Marie', 'What', 'is', 'yours']

    >>> get_words("Hi! My name is Anne-Marie. What's yours?")
    ['Hi', 'My', 'name', 'is', 'Anne-Marie', "What's", 'yours']
    """
    # pattern = r"[\w']+"
    # return re.findall(pattern, s)
    # pattern = r'\W+'
    pattern = r"[^\w'\-]"
    words = re.split(pattern, s)
    # remove 'empty' words
    words = [w for w in words if w]
    return words


def get_sentences(s):
    raise NotImplementedError()
    # pattern = r"[^.!?]*[.!?]"
    # return re.findall(pattern, s)


def find_all(item, items, regex=False, regex_flags=None):
    """
    Finds the indexes and values for all values matching a given item.

    :param item: the value (or pattern) to match/find.
    :param items: an iterable of items to match against.
    :param regex: If True, item will be treated as a regex pattern.
    :param regex_flags: Optional flags for re.search().
    :return: an iterable of (index, value) tuples.

    >>> find_all('own',['Is', 'that', 'your', 'own', 'brown', 'cow'])
    [(3, 'own')]

    >>> find_all('own',['Is', 'that', 'your', 'own', 'brown', 'cow'], regex=True)
    [(3, 'own'), (4, 'brown')]

    >>> find_all('^own$',['Is', 'that', 'your', 'own', 'brown', 'cow'], regex=True)
    [(3, 'own')]

    >>> find_all('ow',['How', 'now', 'brown', 'cow'])
    []

    >>> find_all('ow$',['How', 'now', 'brown', 'cow'], regex=True)
    [(0, 'How'), (1, 'now'), (3, 'cow')]

    >>> find_all('[a-z]ow(?![\w])',['How', 'now', 'brown', 'cow'], regex=True)
    [(1, 'now'), (3, 'cow')]

    >>> find_all('(?<!\w)[a-z]ow',['How', 'now', 'brown', 'cow'], regex=True, regex_flags=re.IGNORECASE)
    [(0, 'How'), (1, 'now'), (3, 'cow')]

    >>> find_all('(?<=\w)[a-z]ow',['How', 'now', 'brown', 'cow'], regex=True, regex_flags=re.IGNORECASE)
    [(2, 'brown')]
    """
    if regex:
        flags = regex_flags or 0
        return [(index, value) for index, value in enumerate(items) if re.search(item, value, flags=flags)]
    else:
        return [(index, value) for index, value in enumerate(items) if value == item]


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
