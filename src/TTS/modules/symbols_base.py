import string

RussianLower = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
                'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
                'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

RussianUpper = [x.upper() for x in RussianLower]

RussianConsonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л',
                     'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц',
                     'ч', 'ш', 'щ']

RussianVowels = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']

RussianUpperVowels = [x.upper() for x in RussianVowels]

RussianSoftVowels = ['е', 'ё', 'и', 'ю', 'я']  # на самом деле буквы, обозначающие мягкость согласных на письме

RussianUpperSoftVowels = [x.upper() for x in RussianSoftVowels]

RussianUpperConsonants = [x.upper() for x in RussianConsonants]

LatinLower = [x for x in string.ascii_lowercase]

LatinUpper = [x.upper() for x in LatinLower]

Digits = [x for x in string.digits]

MathematicalSigns = ['–', '+', '/', '*', '=', '<', '>', '%']

PunctuationMarks = ['.', ',', ':', ';', '(', ')', '!', '?', '-', ' ']

SpecialReadableSigns = ['№', '$', '&']

SpecialSigns = ['~', '`', '№', '#', '@', '$', '^', '&', '|', '\\', '{', '}', '[', ']', '"', '\'']


def is_consonant(sound) -> bool:
    return (any(x == sound for x in RussianConsonants)) or (any(x == sound for x in RussianUpperConsonants))


def contains_only_consonants(s: str) -> bool:
    res = True
    idx = 0
    while res is True and idx < len(s):
        res &= is_consonant(s[idx])
        idx += 1
    return res


def is_vowel(sound: str) -> bool:
    return (any(x == sound for x in RussianVowels)) or (any(x == sound for x in RussianUpperVowels))


def is_soft_vowel(vowel: str) -> bool:  # обозначает ли буква мягкость согласного
    return (any(x == vowel for x in RussianSoftVowels)) or (any(x == vowel for x in RussianUpperSoftVowels))


def contains_soft_vowel(string: str) -> bool:
    res = False
    idx = 0
    while res is False and idx < len(string):
        res |= is_soft_vowel(string[idx])
        idx += 1
    return res


def contains_only_soft_vowels(string: str) -> bool:
    res = True
    idx = 0
    while res is True and idx < len(string):
        if is_vowel(string[idx]):
            res &= is_soft_vowel(string[idx])
        idx += 1
    return res


def has_three_more_consonants_in_row(s: str) -> bool:
    res = False
    count = 0
    for i in s:
        if count >= 2:
            res = True
        if res is True:
            break
        if is_consonant(i):
            count += 1
        else:
            count = 0
    return res
