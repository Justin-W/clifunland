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
    # pattern = r"[\w']+"
    # return re.findall(pattern, s)
    # pattern = r'\W+'
    pattern = r"[^\w'\-]"
    return re.split(pattern, s)



def get_sentences(s):
    raise NotImplementedError()
    # pattern = r"[^.!?]*[.!?]"
    # return re.findall(pattern, s)


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
