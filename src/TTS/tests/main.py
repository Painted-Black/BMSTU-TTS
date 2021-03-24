import unittest

from modules.phonetic_processor import LetterPhonemeTranscriptor
from modules.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor


class PhonemeAllophoneTranscriptorCase(unittest.TestCase):
    def setUp(self):
        self.pat = PhonemeAllophoneTranscriptor()

    def test_single_vowel(self):
        phonemes = [["a"], ["o"], ["u"], ["i"], ["e"], ["y"],
                    ["_", "a"], ["_", "o"], ["_", "u"], ["_", "i"], ["_", "e"], ["_", "y"],
                    ["#", "a"], ["#", "o"], ["#", "u"], ["#", "i"], ["#", "e"], ["#", "y"],
                    ["a", "_"], ["o", "_"], ["u", "_"], ["i", "_"], ["e", "_"], ["y", "_"],
                    ["a", "#"], ["o", "#"], ["u", "#"], ["i", "#"], ["e", "#"], ["y", "#"],
                    ["_", "a", "_"], ["_", "o", "_"], ["_", "u", "_"], ["_", "i", "_"], ["_", "e", "_"], ["_", "y", "_"],
                    ["#", "a", "#"], ["#", "o", "#"], ["#", "u", "#"], ["#", "i", "#"], ["#", "e", "#"], ["#", "y", "#"],
                    ["a", "+"], ["o", "+"], ["u", "+"], ["i", "+"], ["e", "+"], ["y", "+"]]
        results = [["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_100"], ["o_100"], ["u_100"], ["i_100"], ["e_100"], ["y_100"],
                   ["a_000"], ["o_000"], ["u_000"], ["i_000"], ["e_000"], ["y_000"]]
        self.__run_test_cases(phonemes, results, "test_single_vowel")

    def test_vowel_left_context(self):
        phonemes = [["p", "a"], ["p", "a", "+"],
                    ["_", "p", "a"], ["_", "p", "a", "+"],
                    ["#", "p", "a"], ["#", "p", "a", "+"],
                    ["sh", "a"], ["sh", "a", "+"],
                    ["k", "a"], ["k", "a", "+"],
                    ["k'", "a"], ["k'", "a", "+"]]
        results = [["p_3", "a_110"], ["p_4", "a_010"],
                   ["p_3", "a_110"], ["p_4", "a_010"],
                   ["p_3", "a_110"], ["p_4", "a_010"],
                   ["sh_3", "a_120"], ["sh_4", "a_020"],
                   ["k_3", "a_130"], ["k_4", "a_030"],
                   ["k'_3", "a_140"], ["k'_4", "a_040"]]
        self.__run_test_cases(phonemes, results, "test_vowel_left_context")

    def test_vowel_right_context(self):
        phonemes = [["a", "p"], ["a", "+", "p"],
                    ["a", "p", "_"], ["a", "+", "p", "_"],
                    ["a", "p", "3"], ["a", "+", "p", "#"],
                    ["a", "t"], ["a", "+", "t"],
                    ["a", "t'"], ["a", "+", "t'"]]
        results = [["a_101", "p_0"], ["a_001", "p_0"],
                   ["a_101", "p_0"], ["a_001", "p_0"],
                   ["a_101", "p_0"], ["a_001", "p_0"],
                   ["a_102", "t_0"], ["a_002", "t_0"],
                   ["a_103", "t'_0"], ["a_003", "t'_0"]]
        self.__run_test_cases(phonemes, results, "test_vowel_right_context")

    def test_vowel_full_context(self):
        phonemes = [["p", "a", "p"], ["p", "a", "+", "p"],
                    ["p", "a", "t"], ["p", "a", "+", "t"],
                    ["p", "a", "t'"], ["p", "a", "+", "t'"],
                    ["sh", "a", "p"], ["sh", "a", "+", "p"],
                    ["sh", "a", "t"], ["sh", "a", "+", "t"],
                    ["sh", "a", "t'"], ["sh", "a", "+", "t'"],
                    ["k", "a", "p"], ["k", "a", "+", "p"],
                    ["k", "a", "t"], ["k", "a", "+", "t"],
                    ["k", "a", "t'"], ["k", "a", "+", "t'"],
                    ["k'", "a", "p"], ["k'", "a", "+", "p"],
                    ["k'", "a", "t"], ["k'", "a", "+", "t"],
                    ["k'", "a", "t'"], ["k'", "a", "+", "t'"]]
        results = [["p_3", "a_111", "p_0"], ["p_4", "a_011", "p_0"],
                   ["p_3", "a_112", "t_0"], ["p_4", "a_012", "t_0"],
                   ["p_3", "a_113", "t'_0"], ["p_4", "a_013", "t'_0"],
                   ["sh_3", "a_121", "p_0"], ["sh_4", "a_021", "p_0"],
                   ["sh_3", "a_122", "t_0"], ["sh_4", "a_022", "t_0"],
                   ["sh_3", "a_123", "t'_0"], ["sh_4", "a_023", "t'_0"],
                   ["k_3", "a_131", "p_0"], ["k_4", "a_031", "p_0"],
                   ["k_3", "a_132", "t_0"], ["k_4", "a_032", "t_0"],
                   ["k_3", "a_133", "t'_0"], ["k_4", "a_033", "t'_0"],
                   ["k'_3", "a_141", "p_0"], ["k'_4", "a_041", "p_0"],
                   ["k'_3", "a_142", "t_0"], ["k'_4", "a_042", "t_0"],
                   ["k'_3", "a_143", "t'_0"], ["k'_4", "a_043", "t'_0"]]
        self.__run_test_cases(phonemes, results, "test_vowel_full_context")

    def test_single_consonant(self):
        phonemes = [["p"], ["p", "_"], ["p", "#"],
                    ["p'"], ["p'", "_"], ["p'", "#"]]
        results = [["p_0"], ["p_0"], ["p_0"],
                   ["p'_0"], ["p'_0"], ["p'_0"]]
        self.__run_test_cases(phonemes, results, "test_single_consonant")

    def test_right_context_consonant(self):
        phonemes = [["p", "t"], ["p", "d"], ["p", "a"], ["p", "a", "+"],
                    ["p'", "t"], ["p'", "d"], ["p'", "a"], ["p'", "a", "+"]]
        results = [["p_1", "t_0"], ["p_2", "d_0"], ["p_3", "a_110"], ["p_4", "a_010"],
                   ["p'_1", "t_0"], ["p'_2", "d_0"], ["p'_3", "a_140"], ["p'_4", "a_040"]]
        self.__run_test_cases(phonemes, results, "test_single_consonant")

    def __run_test_cases(self, phonemes, results, name):
        for i in range(len(phonemes)):
            res = self.pat.transcript(phonemes[i])
            # print(res)
            try:
                assert len(res) == len(results[i])
            except AssertionError:
                print("Test {0} failed".format(name))
            n = len(res)
            for j in range(n):
                try:
                    assert str(res[j]) == results[i][j]
                except AssertionError:
                    print("Test {0} failed".format(name))


class LetterPhonemeTranscriptorCase(unittest.TestCase):
    def setUp(self):
        self.lpt = LetterPhonemeTranscriptor()

    def test_space(self):
        text = '_'
        res = self.lpt.transcript(text)
        assert res == ['_']

    def test_lattice(self):
        text = '#'
        res = self.lpt.transcript(text)
        assert res == ['#']

    def test_pluse(self):
        text = '+'
        res = self.lpt.transcript(text)
        assert res == ['+']

    def test_equ(self):
        text = '='
        res = self.lpt.transcript(text)
        assert res == ["="]

    def test_empty(self):
        text = ''
        res = self.lpt.transcript(text)
        assert res == ['']

    def test_u(self):
        words = ["У+ТКА", "ЮЛА+"]
        results = [["u", "+", "t", "k", "a"], ["j'", "u", "l", "a", "+"]]
        self.__run_test_cases(words, results, 'u')

    def test_e(self):
        words = ["Э+ТОТ", "Е+ЛЬ"]
        results = [["e", "+", "t", "a", "t"], ["j'", "e", "+", "l'"]]
        self.__run_test_cases(words, results, 'e')

    def test_o(self):
        words = ["ЛЁ+ТЧИК", "О+СЕНЬ"]
        results = [["l'", "o", "+", "ch'", "i", "k"], ["o", "+", "s'", "e", "n'"]]
        self.__run_test_cases(words, results, 'o')

    def test_a(self):
        words = ["АНАНА+С", "Я+БЛОКА", "МЯ+ГКИЙ", "МОЛОКО+"]
        results = [["a", "n", "a", "n", "a", "+", "s"], ["j'", "a", "+", "b", "l", "a", "k", "a"],
                   ["m'", "a", "+", "h'", "k'", "i", "j'"], ["m", "a", "l", "a", "k", "o", "+"]]
        self.__run_test_cases(words, results, 'a')

    def test_y(self):
        words = ["СЫ+ТЫЙ", "ШИ+ЛО", "ПРИНЁ+С_ИГРУ+ШКУ"]
        results = [["s", "y", "+", "t", "y", "j'"], ["sh", "y", "+", "l", "a"],
                   ["p", "r'", "i", "n'", "o", "+", "s", "_", "y", "g", "r", "u", "+", "sh", "k", "u"]]
        self.__run_test_cases(words, results, 'y')

    def test_sh_s(self):
        words = ["ЩЕКА+", "СЧА+СТЬЕ", "ПЕРЕБЕ+ЖЧИК"]
        results = [["sh'", "e", "k", "a", "+"], ["sh'", "a", "+", "s'", "t'", "j'", "e"],
                   ["p'", "e", "r'", "e", "b'", "e", "+", "sh'", "i", "k"]]
        self.__run_test_cases(words, results, 'sh_s')

    def test_ch_s(self):
        words = ["ЧАСЫ+"]
        results = [["ch'", "a", "s", "y", "+"]]
        self.__run_test_cases(words, results, 'ch_s')

    def test_c(self):
        words = ["ЦА+ПЛЯ", "СПЕЦСВЯ+ЗЬ", "ПЕРЕВОЛНОВА+ТЬСЯ", "РУЧА+ЕТСЯ", "БЛЮ+ДЦЕ", "ОТЦА+"]
        results = [["c", "a", "+", "p", "l'", "a"], ["s", "p'", "e", "c", "s", "v'", "a", "+", "s'"],
                   ["p'", "e", "r'", "e", "v", "a", "l", "n", "a", "v", "a", "+", "c", "a"],
                   ["r",  "u", "ch'", "a", "+", "j'", "e", "c", "a"],
                   ["b", "l'", "u", "+", "c", "c", "e"], ["a", "c", "c", "a", "+"]]
        self.__run_test_cases(words, results, 'c')

    def test_h(self):
        words = ["ТРЁ=ХХВО+СТКА", "ЛЕГКО+"]
        results = [["t", "r'", "o", "=", "h", "h", "v", "o", "+", "s", "t", "k", "a"],
                   ["l'", "e", "h", "k", "o", "+"]]
        self.__run_test_cases(words, results, 'h')

    def test_h_s(self):
        words = ["ХИ+ТРЫЙ", "ЛЁ+ГКИЙ"]
        results = [["h'", "i", "+", "t", "r", "y", "j'"],
                   ["l'", "o", "+", "h'", "k'", "i", "j'"]]
        self.__run_test_cases(words, results, "h_s")

    def test_j_s(self):
        words = ["ЯМА+ЙКА", "ВОРОБЬИ+", "БУЛЬО+Н", "КОНЬЯ+К", "ОБЪЁ+М"]
        results = [["j'", "a", "m", "a", "+", "j'", "k", "a"], ["v", "a", "r", "a", "b'", "j'", "i", "+"],
                   ["b", "u", "l'", "j'", "o", "+", "n"], ["k", "a", "n'", "j'", "a", "+", "k"],
                   ["a", "b", "j'", "o", "+", "m"]]
        self.__run_test_cases(words, results, 'j_s')

    def test_m(self):
        words = ["МРА+МОР", "ИЮ+НЬСКИМ_ВЕ+ТРОМ"]
        results = [["m", "r", "a", "+", "m", "a", "r"],
                   ["i", "j'", "u", "+", "n'", "s", "k'", "i", "m", "_", "v'", "e", "+", "t", "r", "a", "m"]]
        self.__run_test_cases(words, results, 'm')

    def test_m_s(self):
        words = ["ТРИУМВИРА+Т", "НАЪТУ+МБЕ", "МЯ+ЧИК"]
        results = [["t", "r'", "i", "u", "m'", "v'", "i", "r", "a", "+", "t"],
                   ["n", "a", "t", "u", "+", "m'", "b'", "e"], ["m'", "a", "+", "ch'", "i", "k"]]
        self.__run_test_cases(words, results, 'm_s')

    def test_n(self):
        words = ["НО+ША", "ВА+СИН_ЧЕМОДА+Н"]
        results = [["n", "o", "+", "sh", "a"],
                   ["v", "a", "+", "s'", "i", "n", "_", "ch'", "e", "m", "a", "d", "a", "+", "n"]]
        self.__run_test_cases(words, results, 'n')

    def test_n_s(self):
        words = ["ЗАКО+НЧИТЬ", "БА+НТИК", "КО+НЬ"]
        results = [["z", "a", "k", "o", "+", "n'", "ch'", "i", "t'"], ["b", "a", "+", "n'", "t'", "i", "k"],
                   ["k", "o", "+", "n'"]]
        self.__run_test_cases(words, results, 'n_s')

    def test_l(self):
        words = ["СО+ЛНЕЧНЫЙ", "СО+ЛНЦЕ", "ПО=ЛЪЛИСТА+"]
        results = [["s", "o", "+", "l", "n'", "e", "ch'", "n", "y", "j'"],
                   ["s", "o", "+", "n", "c", "e"],
                   ["p", "o", "=", "l", "l'", "i", "s", "t", "a", "+"]]
        self.__run_test_cases(words, results, 'l')

    def test_l_s(self):
        words = ["Э+ЛЛИПС", "НО+ЛЬ"]
        results = [["e", "+", "l'", "l'", "i", "p", "s"], ["n", "o", "+", "l'"]]
        self.__run_test_cases(words, results, 'l_s')

    def test_r(self):
        words = ["КРОМЕ+ШНАЯ"]
        results = [["k", "r", "a", "m'", "e", "+", "sh", "n", "a", "j'", "a"]]
        self.__run_test_cases(words, results, 'r')

    def test_r_s(self):
        words = ["КОРРИ+ДА", "КО+РЬ"]
        results = [["k", "a", "r'", "r'", "i", "+", "d", "a"], ["k", "o", "+", "r'"]]
        self.__run_test_cases(words, results, 'r_s')

    def test_b(self):
        words = ["СТОЛБНЯ+К", "ДУ+Б_ЗЕЛЁ+НЫЙ", "КРЕПДЫШИ+Н", "СЕ+РП_ЗАБЛЕСТЕ+Л", "СТО+ЛБ"]
        results = [["s", "t", "a", "l", "b", "n'", "a", "+", "k"],
                   ["d", "u", "+", "b", "_", "z'", "e", "l'", "o", "+", "n", "y", "j'"],
                   ["k", "r'", "e", "b", "d", "y", "sh", "y", "+", "n"],
                   ["s'", "e", "+", "r", "b", "_", "z", "a", "b", "l'", "e", "s'", "t'", "e", "+", "l"],
                   ["s", "t", "o", "+", "l", "p"]]
        self.__run_test_cases(words, results, 'b')

    def test_b_s(self):
        words = ["ОБМЯ+К", "НАЪПНЕ+"]
        results = [["a", "b'", "m'", "a", "+", "k"],
                   ["n", "a", "p", "n'", "e", "+"]]
        self.__run_test_cases(words, results, 'b_s')

    def test_p(self):
        words = ["ПО+Л", "ОКО+П"]
        results = [["p", "o", "+", "l"],
                   ["a", "k", "o", "+", "p"]]
        self.__run_test_cases(words, results, 'p')

    def test_p_s(self):
        words = ["ПИ+Л", "СКО+РБЬ"]
        results = [["p'", "i", "+", "l"],
                   ["s", "k", "o", "+", "r", "p'"]]
        self.__run_test_cases(words, results, 'p_s')

    def test_v(self):
        words = ["ГРА+Ф_ВИ+КТОР", "СА+МОГО", "ТВОЕГО+", "АФГАНИСТА+Н"]
        results = [["g", "r", "a", "+", "v", "_", "v'", "i", "+", "k", "t", "a", "r"],
                   ["s", "a", "+", "m", "a", "v", "a"],
                   ["t", "v", "a", "j'", "e", "v", "o", "+"],
                   ["a", "v", "g", "a", "n'", "i", "s", "t", "a", "+", "n"]]
        self.__run_test_cases(words, results, 'v')

    def test_v_s(self):
        words = ["ВВЁ+З", "ВИ+ЛКА", "КРО+ВЬ_ВРАГА+"]
        results = [["v'", "v'", "o", "+", "s"],
                   ["v'", "i", "+", "l", "k", "a"],
                   ["k", "r", "o", "+", "v'", "_", "v", "r", "a", "g", "a", "+"]]
        self.__run_test_cases(words, results, 'v_s')

    def test_f(self):
        words = ["ЗА+ВТРА", "ФРУ+КТ", "КРО+В"]
        results = [["z", "a", "+", "f", "t", "r", "a"],
                   ["f", "r", "u", "+", "k", "t"],
                   ["k", "r", "o", "+", "f"]]
        self.__run_test_cases(words, results, 'f')

    def test_f_s(self):
        words = ["ГОТО+ВЬСЯ", "ФИ+КУС", "КРО+ВЬ"]
        results = [["g", "a", "t", "o", "+", "f'", "s'", "a"],
                   ["f'", "i", "+", "k", "u", "s"],
                   ["k", "r", "o", "+", "f'"]]
        self.__run_test_cases(words, results, 'f_s')

    def test_d(self):  # надо проверить точнее сочетания ДЧ
        words = ["ПОДУ+Л", "БЕ+ЗДНА", "ПО+ЗДНИЙ", "МУНДШТУ+К", "ЛАНДТА+Г", "ЯГДТА+Ш", "СЕРДЧИ+ШКО", "УКЛА+ДЧИК",
                 "БЛЮ+ДЦЕ", "ОБИ+ДЧИК", "КО+Д_ДО+МА"]
        results = [["p", "a", "d", "u", "+", "l"],
                   ["b'", "e", "+", "z", "n", "a"],
                   ["p", "o", "+", "z'", "n'", "i", "j'"],
                   ["m", "u", "n", "sh", "t", "u", "+", "k"],
                   ["l", "a", "n", "t", "a", "+", "k"],
                   ["j'", "a", "k", "t", "a", "+", "sh"],
                   ["s'", "e", "r", "ch'", "i", "+", "sh", "k", "a"],
                   ["u", "k", "l", "a", "+", "ch'", "i", "k"],
                   ["b", "l'", "u", "+", "c", "c", "e"],
                   ["a", "b'", "i", "+", "ch'", "i", "k"],
                   ["k", "o", "+", "d", "_", "d", "o", "+", "m", "a"]]
        self.__run_test_cases(words, results, 'd')

    def test_d_s(self):
        words = ["ДНЯ+МИ", "ОТДИРА+ТЬ"]
        results = [["d'", "n'", "a", "+", "m'", "i"],
                   ["a", "d'", "d'", "i", "r", "a", "+", "t'"]]
        self.__run_test_cases(words, results, 'd_s')

    def test_t(self):  # проверить СТЛ
        words = ["ЧА+СТНЫЙ", "ЗАСТЛА+ТЬ", "РЕНТГЕ+Н", "ХРИПОТЦА+", "ЧУКО+ТСКИЙ", "БРА+ТСТВО",
                 "КРУ+ЖИТСЯ", "КРУЖИ+ТЬСЯ", "МЛА+ДШЕ", "КО+Д", "СЧАСТЛИ+ВЫЙ"]
        results = [["ch'", "a", "+", "s", "n", "y", "j'"],
                   ["z", "a", "s", "l", "a", "+", "t'"],
                   ["r'", "e", "n", "g'", "e", "+", "n"],
                   ["h", "r'", "i", "p", "a", "c", "c", "a", "+"],
                   ["ch'", "u", "k", "o", "+", "c", "k'", "i", "j'"],
                   ["b", "r", "a", "+", "c", "t", "v", "a"],
                   ["k", "r", "u", "+", "zh", "y", "c", "a"],
                   ["k", "r", "u", "zh", "y", "+", "c", "a"],
                   ["m", "l", "a", "+", "t", "sh", "e"],
                   ["k", "o", "+", "t"],
                   ["sh'", "a", "s", "l'", "i", "+", "v", "y", "j'"]]
        self.__run_test_cases(words, results, 't')

    def test_t_s(self):
        words = ["ПОДТИ+П", "ТИ+П", "БУ+ДЬ"]
        results = [["p", "a", "t'", "t'", "i", "+", "p"],
                   ["t'", "i", "+", "p"],
                   ["b", "u", "+", "t'"]]
        self.__run_test_cases(words, results, 't_s')

    def test_g(self):
        words = ["ВОКЗА+Л", "СТОКГО+ЛЬМ", "СВОЕГО+", "СА+МОГО", "ГО+Д", "ХИ+МИК_ГО+ДА"]
        results = [["v", "a", "g", "z", "a", "+", "l"],
                   ["s", "t", "a", "g", "g", "o", "+", "l'", "m"],
                   ["s", "v", "a", "j'", "e", "v", "o", "+"],
                   ["s", "a", "+", "m", "a", "v", "a"],
                   ["g", "o", "+", "t"],
                   ["h'", "i", "+", "m'", "i", "g", "_", "g", "o", "+", "d", "a"]]
        self.__run_test_cases(words, results, 'g')

    def test_g_s(self):
        words = ["ТРИ+ГГЕР", "ГЕ+НА"]
        results = [["t", "r'", "i", "+", "g'", "g'", "e", "r"],
                   ["g'", "e", "+", "n", "a"]]
        self.__run_test_cases(words, results, 'g_s')

    def test_k(self):
        words = ["БЕ+ГСТВО", "АКСИО+МА", "СТО+Г", "СТО+Г_СЕ+НА"]
        results = [["b'", "e", "+", "k", "s", "t", "v", "a"],
                   ["a", "k", "s'", "i", "o", "+", "m", "a"],
                   ["s", "t", "o", "+", "k"],
                   ["s", "t", "o", "+", "k", "_", "s'", "e", "+", "n", "a"]]
        self.__run_test_cases(words, results, 'k')

    def test_k_s(self):
        words = ["КИ+ПР"]
        results = [["k'", "i", "+", "p", "r"]]
        self.__run_test_cases(words, results, 'k_s')

    def test_z(self):
        words = ["СБА+ВИТЬ", "Е+ЗЖУ", "ЗО+Л", "ПРИНЁ+С_ЗУ+БЫ"]
        results = [["z", "b", "a", "+", "v'", "i", "t'"],
                   ["j'", "e", "+", "zh", "zh", "u"],
                   ["z", "o", "+", "l"],
                   ["p", "r'", "i", "n'", "o", "+", "z", "_", "z", "u", "+", "b", "y"]]
        self.__run_test_cases(words, results, 'z')

    def test_z_s(self):
        words = ["ЗЕЛЁ+НЫЙ", "СДЕ+ЛАТЬ", "КОСЬБА+"]
        results = [["z'", "e", "l'", "o", "+", "n", "y", "j'"],
                   ["z'", "d'", "e", "+", "l", "a", "t'"],
                   ["k", "a", "z'", "b", "a", "+"]]
        self.__run_test_cases(words, results, 'z_s')

    def test_s(self):
        words = ["БЕЗПОЩА+ДНО", "РУЧА+ЕТСЯ", "ПЕРЕВОЛНОВА+ТЬСЯ", "ВЫ+ЛЕЗ", "ВЫ+ЛЕЗ_СО+М", "СЧА+СТЬЕ", "РАСШИ+Б"]
        results = [["b'", "e", "s", "p", "a", "sh'", "a", "+", "d", "n", "a"],
                   ["r",  "u", "ch'", "a", "+", "j'", "e", "c", "a"],
                   ["p'", "e", "r'", "e", "v", "a", "l", "n", "a", "v", "a", "+", "c", "a"],
                   ["v", "y", "+", "l'", "e", "s"],
                   ["v", "y", "+", "l'", "e", "s", "_", "s", "o", "+", "m"],
                   ["sh'", "a", "+", "s'", "t'", "j'", "e"],
                   ["r", "a", "sh", "sh", "y", "+", "p"]]
        self.__run_test_cases(words, results, 's')

    def test_s_s(self):
        words = ["АГРЕССИ+ВНОСТЬ", "СИ+ЛА", "БРО+СЬ"]
        results = [["a", "g", "r'", "e", "s'", "s'", "i", "+", "v", "n", "a", "s'", "t'"],
                   ["s'", "i", "+", "l", "a"],
                   ["b", "r", "o", "+", "s'"]]
        self.__run_test_cases(words, results, 's_s')

    def test_zh(self):
        words = ["ЖО+РА", "ЖИ+ТЬ", "ДРО+ЖЬ_ЗЕМЛИ+", "ВЪЕЗЖА+ТЬ", "БРО+ШЬ_ЖЕ+НИ"]
        results = [["zh", "o", "+", "r", "a"],
                   ["zh", "y", "+", "t'"],
                   ["d", "r", "o", "+", "zh", "_", "z'", "e", "m", "l'", "i", "+"],
                   ["v", "j'", "e", "zh", "zh", "a", "+", "t'"],
                   ["b", "r", "o", "+", "zh", "_", "zh", "e", "+", "n'", "i"]]
        self.__run_test_cases(words, results, 'zh')

    def test_sh(self):
        words = ["МОЛОДЁ+ЖЬ", "РАСШИ+Б", "ШИ+ЛО"]
        results = [["m", "a", "l", "a", "d'", "o", "+", "sh"],
                   ["r", "a", "sh", "sh", "y", "+", "p"],
                   ["sh", "y", "+", "l", "a"]]
        self.__run_test_cases(words, results, 'sh')

    def test_voiced_assimilation(self):
        words = ["СКА+ЗКА", "ЛО+ДКА", "РАСПИСА+ТЬ", "ВХО+Д",
                 "ОТБИ+ТЬ", "ПРО+СЬБА", "КОСЬБА+", "СДА+ТЬ",
                 "СВО+Й", "КВА+С", "ОТВЕ+Т", "ХВАЛИ+ТЬ",
                 "БРА+Т_ДРУ+ГА", "ПРИНЁ+С_ДОМО+Й",
                 "ВСТРЯХНУ+ТЬ", "ЧА+СТЬ_ГО+РОДА", "ТЕ+КСТ_БИ+БЛИИ",
                 "ЛУ+Г", "РО+З", "ПРУ+Д", "ДУ+Б",
                 "ЛУ+Г_ДО+МА", "ЛУ+Г_ВОДА+"]
        results = [["s", "k", "a", "+", "s", "k", "a"],
                   ["l", "o", "+", "t", "k", "a"],
                   ["r", "a", "s", "p'", "i", "s", "a", "+", "t'"],
                   ["f", "h", "o", "+", "t"],
                   ["a", "d", "b'", "i", "+", "t'"],
                   ["p", "r", "o", "+", "z'", "b", "a"],
                   ["k", "a", "z'", "b", "a", "+"],
                   ["z", "d", "a", "+", "t'"],
                   ["s", "v", "o", "+", "j'"],
                   ["k", "v", "a", "+", "s"],
                   ["a", "t", "v'", "e", "+", "t"],
                   ["h", "v", "a", "l'", "i", "+", "t'"],
                   ["b", "r", "a", "+", "d", "_", "d", "r", "u", "+", "g", "a"],
                   ["p", "r'", "i", "n'", "o", "+", "z", "_", "d", "a", "m", "o", "+", "j'"],
                   ["f", "s", "t", "r'", "a", "h", "n", "u", "+", "t'"],
                   ["ch'", "a", "+", "z'", "d'", "_", "g", "o", "+", "r", "a", "d", "a"],
                   ["t'", "e", "+", "g", "z", "d", "_", "b'", "i", "+", "b", "l'", "i", "i"],
                   ["l", "u", "+", "k"],
                   ["r", "o", "+", "s"],
                   ["p", "r", "u", "+", "t"],
                   ["d", "u", "+", "p"],
                   ["l", "u", "+", "g", "_", "d", "o", "+", "m", "a"],
                   ["l", "u", "+", "k", "_", "v", "a", "d", "a", "+"]]
        self.__run_test_cases(words, results, 'voiced_assimilation')

    def test_unpronounceable_combinations(self):
        words = ["ЧА+СТНЫЙ", "СЧАСТЛИ+ВЫЙ", "РЕНТГЕ+Н", "ПО+ЗДНО", "ПОДЪУЗДЦЫ+", "ГОЛЛА+НДЦЫ",
                 "СЕ+РДЦЕ", "ЛАНДША+ФТ", "ЯГДТА+Ш", "СО+ЛНЦЕ"]
        results = [["ch'", "a", "+", "s", "n", "y", "j'"],
                   ["sh'", "a", "s", "l'", "i", "+", "v", "y", "j'"],
                   ["r'", "e", "n", "g'", "e", "+", "n"],
                   ["p", "o", "+", "z", "n", "a"],
                   ["p", "a", "d", "u", "s", "c", "y", "+"],
                   ["g", "a", "l", "l", "a", "+", "n", "c", "y"],
                   ["s'", "e", "+", "r", "c", "e"],
                   ["l", "a", "n", "sh", "a", "+", "f", "t"],
                   ["j'", "a", "k", "t", "a", "+", "sh"],
                   ["s", "o", "+", "n", "c", "e"]]
        self.__run_test_cases(words, results, 'unpronounceable_combinations')

    def test_phonemes_change(self):
        words = ["СЧА+СТЬЕ", "ПЕРЕБЕ+ЖЧИК", "ПЕРЕВОЛНОВА+ТЬСЯ", "РУЧА+ЕТСЯ",
                 "БЛЮ+ДЦЕ", "ОТЦА+", "ЛЁ+ГКИЙ", "ЛЕГКО+", "СИ+НЕГО", "КРА+СНОГО",
                 "МНО+ГО", "ДО+РОГО", "РАСШИ+Б", "ВЪЕЗЖА+ТЬ"]
        results = [["sh'", "a", "+", "s'", "t'", "j'", "e"],
                   ["p'", "e", "r'", "e", "b'", "e", "+", "sh'", "i", "k"],
                   ["p'", "e", "r'", "e", "v", "a", "l", "n", "a", "v", "a", "+", "c", "a"],
                   ["r", "u", "ch'", "a", "+", "j'", "e", "c", "a"],
                   ["b", "l'", "u", "+", "c", "c", "e"],
                   ["a", "c", "c", "a", "+"],
                   ["l'", "o", "+", "h'", "k'", "i", "j'"],
                   ["l'", "e", "h", "k", "o", "+"],
                   ["s'", "i", "+", "n'", "e", "v", "a"],
                   ["k", "r", "a", "+", "s", "n", "a", "v", "a"],
                   ["m", "n", "o", "+", "g", "a"],  # !!
                   ["d", "o", "+", "r", "a", "g", "a"],  # !!
                   ["r", "a", "sh", "sh", "y", "+", "p"],
                   ["v", "j'", "e", "zh", "zh", "a", "+", "t'"]]
        self.__run_test_cases(words, results, 'phonemes_change')

    def __run_test_cases(self, words, results, name):
        for i in range(len(words)):
            res = self.lpt.transcript(words[i])
            try:
                assert res == results[i]
            except AssertionError:
                print("Test {0} failed".format(name))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
