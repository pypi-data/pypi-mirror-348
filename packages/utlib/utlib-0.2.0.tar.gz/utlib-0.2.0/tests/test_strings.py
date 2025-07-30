from utlib.strings_utils import word_count, is_polindrome, vowels


def test_strings():
    assert word_count('Hello, im trying to debug this code') == 7
    assert word_count('') == 0
    assert is_polindrome('heeh') == True
    assert is_polindrome('Hello') == False

    assert vowels('eng', True) == [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
        'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z',
    ]
    assert vowels('es', True) == [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
        'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z',
    ]
