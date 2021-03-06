import itertools
import re
from collections import Counter
from collections import OrderedDict

from clifunzone.reflection_utils import is_string


def lorem_ipsum():
    """
    Returns 'Lorem ipsum...' text.

    See: [lipsum.com](http://www.lipsum.com/)

    :return:

    >>> lorem_ipsum()  #doctest: +ELLIPSIS
    'Lorem ipsum dolor sit amet, consectetur ..., hendrerit nulla.'

    >>> len(lorem_ipsum())
    6877
    """
    return '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. In vestibulum ut odio vel fermentum. Donec tristique dignissim tortor, vel hendrerit justo suscipit iaculis. Maecenas pellentesque orci aliquam facilisis faucibus. Aenean tempor, augue non ornare volutpat, ex orci faucibus purus, ut viverra velit lacus id nulla. Vivamus egestas auctor eros, sit amet tristique urna ultrices dignissim. Proin urna elit, rhoncus et interdum id, sollicitudin nec nunc. Nunc ac nisl vitae erat porta lobortis. Sed maximus mattis ligula, ac imperdiet lacus dignissim non. Aenean et metus eros. Praesent augue felis, posuere nec ex quis, placerat consequat nisl. Donec quis neque nibh. Pellentesque sollicitudin, nunc sed faucibus placerat, felis urna cursus erat, a bibendum nisl ante eu ipsum. Quisque quis mollis nibh. Nam et condimentum justo. In hac habitasse platea dictumst.

Donec commodo elit enim, vel euismod sem rutrum ut. Vestibulum tempus rutrum elit nec dapibus. Vivamus luctus, quam nec pretium fermentum, nunc erat maximus orci, quis egestas massa mi iaculis tortor. Nulla facilisi. Mauris ultrices augue tempor congue ultricies. Morbi vel nulla eget erat facilisis molestie. Vestibulum finibus arcu eget elit mattis malesuada ac pellentesque eros. Cras et pretium quam, at porta sapien. Maecenas dignissim purus eu orci vehicula, gravida tempus neque imperdiet. Sed condimentum elementum urna, sit amet pellentesque neque. Aliquam eget libero leo. Pellentesque non placerat ex.

Phasellus mollis ligula elit, et interdum nunc lacinia sed. Curabitur feugiat ex justo, in bibendum enim fringilla quis. Morbi quis ultricies tellus. Nunc porttitor viverra nunc, ut venenatis mi facilisis a. Praesent quis erat vel ex egestas lobortis non nec augue. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus tincidunt sollicitudin leo nec lobortis. Praesent nec erat ut risus tempor luctus in in est. Nam elementum quam quis dolor molestie, sed porttitor sem condimentum. Morbi congue massa non sem tincidunt, in fringilla nisl vulputate. Nunc rhoncus erat id neque volutpat vulputate. Nunc sed tortor cursus, laoreet nisl sed, malesuada justo. Phasellus egestas ac neque nec cursus. Pellentesque pellentesque sapien at lobortis rhoncus. Ut non ipsum efficitur, auctor arcu in, consectetur neque.

Etiam eget purus quis mauris mollis bibendum. Etiam feugiat mollis odio, sed imperdiet velit dictum nec. Etiam volutpat orci id convallis bibendum. Phasellus nec risus condimentum, blandit elit in, facilisis felis. Praesent egestas tortor vitae tempor cursus. Sed nec egestas orci. Duis sit amet felis vitae sapien rutrum tincidunt. Aenean auctor magna sapien, non vulputate eros condimentum vel. Aenean tristique elit non turpis pellentesque vestibulum. Donec nunc sem, sodales id sapien eget, vestibulum eleifend eros. In id pharetra diam, at pulvinar ex. Nunc nec pharetra massa. Quisque porta, ligula non pulvinar dignissim, massa sem dignissim lorem, sed auctor risus est sed tellus. In rutrum tellus sit amet tristique varius. Sed a nunc neque. Nam nec tristique enim.

Aliquam erat volutpat. Duis id justo euismod, euismod risus ac, varius lectus. Suspendisse facilisis tempor felis sed ultrices. Pellentesque vel bibendum ante. Cras convallis lectus id erat semper, in gravida ex efficitur. Duis eleifend aliquam cursus. Etiam cursus nibh vel mattis cursus. Vivamus lectus erat, dictum et mauris eu, viverra tincidunt velit.

Aliquam vestibulum neque non nisi porttitor sagittis. Donec quam mi, placerat placerat ultricies sed, lacinia at urna. Vivamus et viverra turpis. Phasellus justo turpis, finibus nec mauris at, tristique tempor urna. Nulla maximus efficitur convallis. Donec non mauris pharetra elit hendrerit fringilla. Quisque auctor volutpat risus, et vehicula nulla feugiat sit amet. Integer efficitur est dui, et varius tellus porttitor quis. Etiam tempor nunc a erat efficitur convallis. Quisque turpis neque, convallis eu viverra nec, ultricies non turpis. Nam eget erat mauris. Fusce quis arcu nunc. Mauris pulvinar, lorem nec mattis feugiat, tellus sapien sodales neque, sed condimentum sapien lorem quis arcu.

Donec pulvinar orci eros, ut feugiat sem pharetra a. Praesent iaculis commodo ullamcorper. Vivamus sed sapien elit. Vestibulum at dui quis neque fermentum elementum. Nulla facilisis accumsan molestie. Ut blandit at enim nec commodo. Donec a ex quis turpis iaculis condimentum ut a sem. Mauris feugiat aliquam metus, ornare condimentum eros scelerisque ac.

Nullam rhoncus ut eros at cursus. Sed massa purus, interdum iaculis elit in, viverra molestie purus. Nunc fringilla lorem magna, vitae scelerisque massa facilisis vitae. Nullam a nisl id purus dignissim aliquet vitae vel diam. Donec faucibus neque et libero pharetra iaculis. Maecenas eu molestie orci. Nunc pharetra arcu dolor, a gravida felis tincidunt sit amet. Cras purus nisi, venenatis quis auctor quis, tempor vitae tellus. Nulla vel tortor suscipit, ullamcorper sapien in, lobortis enim.

Nullam mollis odio lacinia ante fringilla, a gravida purus aliquam. Nam tempor, mauris non efficitur rutrum, velit dolor malesuada lectus, eu elementum augue risus in eros. Phasellus eget mauris ac erat mollis maximus non sed leo. Suspendisse tincidunt tempus aliquet. Etiam nulla felis, gravida sit amet rhoncus in, ullamcorper sagittis elit. Duis scelerisque neque at eros facilisis, quis rhoncus quam venenatis. Sed pretium risus ipsum, a sodales ante ullamcorper non.

Mauris id tristique enim. Praesent commodo feugiat metus, sit amet elementum risus lobortis eget. Quisque auctor efficitur sapien ultrices auctor. Donec eget ante lobortis, suscipit turpis et, pellentesque neque. Praesent aliquam tincidunt dictum. Suspendisse auctor erat et mi tincidunt, sit amet ornare elit congue. Ut varius diam id metus sodales, eget fermentum enim luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas non odio vestibulum felis tristique pretium. Suspendisse hendrerit et elit vel dictum.

Vestibulum at nibh lorem. Nullam euismod lacus lacus, ut bibendum quam ullamcorper non. Curabitur ac orci et dui dignissim semper ut id turpis. Morbi ultricies, elit vel fringilla ullamcorper, turpis nunc vehicula tortor, vitae porta lectus ante non sapien. Aenean nec est a tortor rhoncus bibendum. In hac habitasse platea dictumst. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec pellentesque lacus et tincidunt sagittis. Aliquam non nunc elit. Suspendisse eleifend eros vitae ligula dapibus pulvinar. Interdum et malesuada fames ac ante ipsum primis in faucibus.

Phasellus semper sem vulputate turpis laoreet accumsan. Nullam sollicitudin nisi vel nibh aliquet, sed feugiat felis volutpat. Suspendisse potenti. Cras ac urna rutrum, rhoncus diam eleifend, hendrerit nulla.'''  # noqa


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
    Splits a string into an iterable of words.

    :param s: the string to split.
    :return: an iterable.

    >>> get_words("Hi! My name is Anne Marie. What is yours?")
    ['Hi', 'My', 'name', 'is', 'Anne', 'Marie', 'What', 'is', 'yours']

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


def get_index_distance_stats(indexes1, indexes2):
    """
    Calculates statistics about the distances between

    Adapted from: http://stackoverflow.com/a/33389155

    :param indexes1: an iterable of numeric values.
    :param indexes2: an iterable of numeric values.
    :return: a dict of statistical values.

    >>> get_index_distance_stats([], [])
    Traceback (most recent call last):
    ValueError: indexes1 is invalid

    >>> get_index_distance_stats([1, 3, 5, 7, 9], [])
    Traceback (most recent call last):
    ValueError: indexes2 is invalid

    >>> get_index_distance_stats([1, 3, 5, 7, 9], [1, 4, 9, 16, 25, 36, 49])
    {'max': 48, 'mean': 16.65714285714286, 'min': 0}

    >>> get_index_distance_stats([4, 16, 36, 64], [9, 25, 49, 81])
    {'max': 77, 'mean': 30.25, 'min': 5}
    """
    if not indexes1:
        raise ValueError('indexes1 is invalid')
    if not indexes2:
        raise ValueError('indexes2 is invalid')
    distances = [abs(x[0] - x[1]) for x in itertools.product(indexes1, indexes2)]
    try:
        min_dist = min(distances)
        max_dist = max(distances)
        mean_dist = sum(distances) / float(len(distances))
    except ValueError:
        min_dist = None
        max_dist = None
    try:
        mean_dist = sum(distances) / float(len(distances))
    except ZeroDivisionError:
        mean_dist = None
    return {'min': min_dist, 'max': max_dist, 'mean': mean_dist}


def find_distances(item1, item2, items, regex=False, regex_flags=None, verbose=False):
    """
    Uses find_all() and get_index_distance_stats() to calculate distance stats for 2 items (or 2 sets of items)
    within a given list of items. E.g. The distances of 2 words (or 2 word sets) within a given list of words.

    Adapted from: http://stackoverflow.com/a/33389155

    :param item1: the value (or pattern) to match/find.
        If it is not a string, it will be treated as an iterable of values/patterns to match.
    :param item2: the value (or pattern) to match/find.
        If it is not a string, it will be treated as an iterable of values/patterns to match.
    :param items: an iterable of items to match against.
    :param regex: If True, item will be treated as a regex pattern.
    :param regex_flags: Optional flags for re.search().
    :return:

    >>> words = get_words(lorem_ipsum())
    >>> find_distances(['lorem'], ['ipsum'], words)
    {'max': 893, 'mean': 402.56, 'min': 83}

    >>> words = get_words(lorem_ipsum())
    >>> find_distances(['lorem', 'dolor'], ['consectetur', 'adipiscing'], words)
    {'max': 889, 'mean': 467.0740740740741, 'min': 3}

    >>> words = get_words(lorem_ipsum())
    >>> w1 = ['^Pellentesque$']
    >>> w2 = ['^Vivamus']
    >>> find_distances(w1, w2, words, regex=True, regex_flags=re.IGNORECASE)
    {'max': 910, 'mean': 287.1212121212121, 'min': 21}
    """

    def find_distinct_indexes(find_items, all_items, regex, regex_flags):
        all_indexes = set()
        for item in find_items:
            indexes = find_all(item, all_items, regex=regex, regex_flags=regex_flags)
            indexes = (index for (index, value) in indexes)
            all_indexes.update(indexes)
        return all_indexes

    def get_matches_detail(indexes, items):
        # details = ((i, items[i]) for i in indexes)
        # details = [(i, items[i]) for i in indexes]
        # details = {i: items[i] for i in indexes}
        # details = dict((items[i], i) for i in indexes)
        details = {}
        for i in indexes:
            value = items[i]
            if value not in details:
                details[value] = set()
                # details[value] = []
            details[value].add(i)
            # details[value].append(i)
        return details

    if is_string(item1):
        item1 = [item1]
    if is_string(item2):
        item2 = [item2]

    indexes1 = find_distinct_indexes(item1, items, regex, regex_flags)
    indexes2 = find_distinct_indexes(item2, items, regex, regex_flags)
    d = get_index_distance_stats(indexes1, indexes2)
    if verbose:
        d.update({'matches1': get_matches_detail(indexes1, items)})
        d.update({'matches2': get_matches_detail(indexes2, items)})
    return d


def main():
    import doctest
    fail, total = doctest.testmod(optionflags=(doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE))
    print('Doctest: {f} FAILED ({p} of {t} PASSED).'.format(f=fail, p=(total - fail), t=total))


if __name__ == "__main__":
    main()
