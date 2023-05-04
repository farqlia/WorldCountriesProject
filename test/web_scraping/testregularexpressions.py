import re


def test_learn_regular_expression():
    string = ''''<h2><a>Afganistan</a></h2><p><strong>unpaved: </strong>17,000 km (2017)</p>'''
    pattern = re.compile("<(?P<tag>.*?)>(?P<content>.+)</(?P=tag)>")
    matches = pattern.findall(string)
    assert len(matches) == 2
    assert matches[0][1] == '<a>Afganistan</a>'
    assert matches[1][1] == '<strong>unpaved: </strong>17,000 km (2017)'


def test_learn_regular_expression2():
    string = "<strong><bold>key: </bold></strong> description of quantity"
    pattern = re.compile("<.*>(?P<key>.+?)</.*>(?P<content>.*?)")
    matches_iter = pattern.finditer(string)
    match = next(matches_iter)
    assert match.group('key') == 'key: '
    assert match.group('content') == ' description of quantity'


def test_learn_regular_expression3():
    string = ''''<p><strong>unpaved: </strong>17,000 km (2017)</p>'''
    pattern = re.compile("<.*>(?P<key>.+?)</.*>(?P<content>.*?)")
    matches_iter = pattern.finditer(string)
    match = next(matches_iter)
    assert match.group('content') == ''


def test_learn_regular_expression4():
    string = "<strong>unpaved: </strong>17,000 km (2017)"
    pattern = re.compile("<strong>(?P<key>.+?)</strong>(?P<value>.+)")
    match = pattern.search(string)
    print(match.group('key'))
    print(match.group('value'))