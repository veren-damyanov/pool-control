import re


class regex:
    """Assert that a given string meets some expectations.
    Takes from https://kalnytskyi.com/howto/assert-str-matches-regex-in-pytest/
    """

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    # def __eq__(self, actual):
    #     return bool(self._regex.match(str(actual)))

    def __repr__(self):
        return f'pytest_regex({self._regex.pattern})'

    def __eq__(self, other):
        return self.matches(other)

    # def __imatmul__(self, other):
    #     return self.matches(other)

    def matches(self, other):
        return bool(self._regex.search(str(other)))


def test_regex():
    assert regex(r'\d{2}').matches('aaa42')
    assert regex(r'\d{2}').matches('42aaa')
    assert regex(r'\d{2}').matches('42')
    assert not regex(r'^\d{2}').matches('aaa42')
    assert not regex(r'\d\d\d').matches('aaa42')
