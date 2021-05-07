import unittest
from modules.phonetic_processor.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor


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
                   ["pause_0", "a_100"], ["pause_0", "o_100"], ["pause_0", "u_100"], ["pause_0", "i_100"], ["pause_0", "e_100"], ["pause_0", "y_100"],
                   ["pause_1", "a_100"], ["pause_1", "o_100"], ["pause_1", "u_100"], ["pause_1", "i_100"], ["pause_1", "e_100"], ["pause_1", "y_100"],
                   ["a_100", "pause_0"], ["o_100", "pause_0"], ["u_100", "pause_0"], ["i_100", "pause_0"], ["e_100", "pause_0"], ["y_100", "pause_0"],
                   ["a_100", "pause_1"], ["o_100", "pause_1"], ["u_100", "pause_1"], ["i_100", "pause_1"], ["e_100", "pause_1"], ["y_100", "pause_1"],
                   ["pause_0", "a_100", "pause_0"], ["pause_0", "o_100", "pause_0"], ["pause_0", "u_100", "pause_0"], ["pause_0", "i_100", "pause_0"], ["pause_0", "e_100", "pause_0"], ["pause_0", "y_100", "pause_0"],
                   ["pause_1", "a_100", "pause_1"], ["pause_1", "o_100", "pause_1"], ["pause_1", "u_100", "pause_1"], ["pause_1", "i_100", "pause_1"], ["pause_1", "e_100", "pause_1"], ["pause_1", "y_100", "pause_1"],
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
                   ["pause_0", "p_3", "a_110"], ["pause_0", "p_4", "a_010"],
                   ["pause_1", "p_3", "a_110"], ["pause_1", "p_4", "a_010"],
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
                   ["a_101", "p_0", "pause_0"], ["a_001", "p_0", "pause_0"],
                   ["a_101", "p_0"], ["a_001", "p_0", "pause_1"],
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
        results = [["p_0"], ["p_0", "pause_0"], ["p_0", "pause_1"],
                   ["p'_0"], ["p'_0", "pause_0"], ["p'_0", "pause_1"]]
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
                raise AssertionError
            n = len(res)
            for j in range(n):
                try:
                    assert str(res[j]) == results[i][j]
                except AssertionError:
                    print("Test {0} failed".format(name))
                    raise AssertionError
