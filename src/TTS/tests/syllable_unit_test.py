import unittest

from modules.phonetic_processor.syllabic_complex1_unit import SyllabicComplex1Unit
from modules.phonetic_processor.syllabic_complex2_unit import SyllabicComplex2Unit
from modules.phonetic_processor.syllabic_complex3_unit import SyllabicComplex3Unit
from modules.phonetic_processor.open_syllable_unit import OpenSyllableUnit
from modules.allophone import Allophone
from modules.phonetic_processor.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor
from modules.phonetic_processor.letter_phoneme_transcriptor import LetterPhonemeTranscriptor


def run_test_cases(method, _allophones: [[Allophone]], _results: []):
    n = len(_allophones)
    for q in range(n):
        allophones = _allophones[q]
        results = _results[q]
        res = method(allophones)
        assert len(res) == len(results)
        n = len(res)
        for i in range(n):
            unit = res[i]
            real_unit = results[i]
            assert len(unit) == len(real_unit)
            m = len(unit)
            for j in range(m):
                syllable = res[i][j]
                real_syllable = results[i][j]
                assert len(syllable) == len(real_syllable)
                k = len(syllable)
                for g in range(k):
                    assert str(res[i][j][g].phoneme) == results[i][j][g]


class OpenSyllableUnitCase(unittest.TestCase):
    def setUp(self):
        self.__osu = OpenSyllableUnit()
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()

    def test_open_syllables(self):
        texts = ["КО+ЛОСА", "КО+Л", "", "О+", "К", "О+М", "МО+",
                 "МНО+ГО", "МАЙК", "А+ММО"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[["k", "o"], ["l", "a"], ["s", "a"]],
                   [["k", "o", "l"]],
                   [[]],
                   [["o"]],
                   [["k"]],
                   [["o", "m"]],
                   [["m", "o"]],
                   [["m", "n", "o"], ["g", "a"]],
                   [["m", "a", "j'", "k"]],
                   [["a"], ["m", "m", "a"]],
                   ]
        try:
            self.run_test_cases(allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_open_syllables"))
            raise AssertionError

    def run_test_cases(self, _allophones: [[Allophone]], _results: []):
        n = len(_allophones)
        for q in range(n):
            allophones = _allophones[q]
            results = _results[q]
            res = self.__osu.process(allophones)
            assert len(res) == len(results)
            n = len(res)
            for i in range(n):
                unit = res[i]
                real_unit = results[i]
                assert len(unit) == len(real_unit)
                k = len(unit)
                for g in range(k):
                    assert str(res[i][g].phoneme) == results[i][g]

    def tearDown(self):
        pass


class SyllableComplex3UnitCase(unittest.TestCase):
    def setUp(self):
        self.__sc3u = SyllabicComplex3Unit()
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()

    def test_sonant_vowel_by_word(self):
        texts = ["КО+ЛОСА", "КОЛО+СА", "КО+ЛОН", "КО+ЛА", "КОЛА+"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[[["k", "o", "l", "a"], ["s", "a"]]],
                   [[["k", "a"], ["l", "o"], ["s", "a"]]],
                   [[["k", "o"], ["l", "a", "n"]]],
                   [[["k", "o", "l", "a"]]],
                   [[["k", "a"], ["l", "a"]]]
                   ]
        try:
            run_test_cases(self.__sc3u.process_by_word, allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_sonant_vowel_by_word"))
            raise AssertionError

    def tearDown(self):
        pass


class SyllableComplex2UnitCase(unittest.TestCase):
    def setUp(self):
        self.__sc2u = SyllabicComplex2Unit()
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()

    def _test_two_sonants_by_word(self):
        texts = ["МА+ЙКА", "МА+ЙНА", "ЖА+РКО", "МА+ЙК", "РМА+ДА", "АРМА+ДА"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[[["m", "a", "j'"], ["k", "a"]]],
                   [[["m", "a"], ["j'", "n", "a"]]],
                   [[["zh", "a", "r"], ["k", "a"]]],
                   [[["m", "a", "j'", "k"]]],
                   [[["r", "m", "a"], ["d", "a"]]],
                   [[["a", "r", "m", "a"], ["d", "a"]]]
                   ]
        try:
            run_test_cases(self.__sc2u.process_by_word, allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_two_sonants_by_word"))
            raise AssertionError

    def tearDown(self):
        pass


class SyllableComplex1UnitCase(unittest.TestCase):
    def setUp(self):
        self.__sc1u = SyllabicComplex1Unit()
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()

    def _test_single_vowel_syllable(self):
        texts = ["АЛЛОФО+Н", "АЯ+КС"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[[["a", "l", "l", "a"], ["f", "o", "n"]]],
                   [[["a", "j'", "a", "k", "s"]]]
                   ]
        try:
            run_test_cases(self.__sc1u.process_by_word, allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_single_vowel_syllable"))
            raise AssertionError

    def _test_ja(self):
        texts = ["ТАКА+Я", "ЛИ+НИЯ", "Я+МА", "РА=ДИОА=ЭРОНАВИГА+ЦИЯ"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[[["t", "a"], ["k", "a", "j'", "a"]]],
                   [[["l'", "i"], ["n'", "i", "j'", "a"]]],
                   [[["j'", "a"], ["m", "a"]]],
                   [[["r", "a"], ["d'", "i", "a", "a", "e"], ["r", "a"], ["n", "a"], ["v'", "i"],
                     ["g", "a"], ["c", "y", "j'", "a"]]]
                   ]
        try:
            run_test_cases(self.__sc1u.process_by_word, allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_ja"))
            raise AssertionError

    def _test_vowels_sequence_by_word(self):
        texts = ["НАИ+ВНЫЙ", "ДИОРА+МА", "БО+А", "РА=ДИОА=ЭРОНАВИГА+ЦИЯ"]
        allophones = []
        for text in texts:
            phonemes = self.__lft.transcript(text)
            cur_allophones = self.__pat.transcript(phonemes)
            allophones.append(cur_allophones)
        results = [[[["n", "a", "i"], ["v", "n", "y", "j'"]]],
                   [[["d'", "i", "a"], ["r", "a"], ["m", "a"]]],
                   [[["b", "o", "a"]]],
                   [[["r", "a"], ["d'", "i", "a", "a", "e"], ["r", "a"], ["n", "a"], ["v'", "i"],
                     ["g", "a"], ["c", "y", "j'", "a"]]]
                   ]
        try:
            run_test_cases(self.__sc1u.process_by_word, allophones, results)
        except AssertionError:
            print("Test {0} failed".format("test_vowels_sequence_by_word"))
            raise AssertionError

    def tearDown(self):
        pass
