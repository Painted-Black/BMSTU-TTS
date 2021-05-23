from abc import ABC
from modules.allophone import Allophone
from modules.phonetic_processor.open_syllable_unit import OpenSyllableUnit


class SyllabicUnit(ABC):
    Sonants = {"j'", "v", "v'", "r", "r'", "l", "l'", "n", "n'", "m", "m'"}

    def _correct_sonants(self, syllables: [[[Allophone]]]):
        n = len(syllables)
        for i in range(n):
            j = 0
            while j < len(syllables[i]):
                cur_syllable, next_syllable = self._get_cur_next(syllables[i], j)
                if next_syllable is not None:
                    p = len(next_syllable)
                    cur_last = self._get_last(cur_syllable)
                    if cur_last is not None and cur_last.is_vowel() and p != 0:
                        to_add, new_next = self._remove_first_sonant(next_syllable)
                        syllables[i][j] += to_add
                        syllables[i][j + 1] = new_next
                        if len(new_next) == 0:
                            syllables[i] = syllables[i][:j + 1] + syllables[i][j + 2:]
                            j -= 1
                j += 1

    def _remove_first_sonant(self, syllable: [Allophone]):
        to_remove = []
        idx = None
        n = len(syllable)
        for i in range(n):
            allophone = syllable[i]
            if i < n - 1:
                next_allophone = syllable[i+1]
                if allophone.is_consonant() and \
                    allophone.phoneme in self.Sonants and \
                    next_allophone.is_consonant() is True and \
                     next_allophone.phoneme not in self.Sonants:
                    to_remove.append(allophone)
                    idx = i
                break
            else:
                break
        if idx is not None:
            new_syllable = syllable[idx + 1:]
        else:
            new_syllable = syllable
        return to_remove, new_syllable

    def _correct_single_vowel(self, syllables: [[[Allophone]]]) -> [[[Allophone]]]:
        n = len(syllables)
        for i in range(n):
            m = len(syllables[i])
            j = 0
            while j < m:
                if len(syllables[i][j]) == 1 and j != m - 1:
                    syllables[i][j+1] = syllables[i][j] + syllables[i][j+1]
                    syllables[i] = syllables[i][:j] + syllables[i][j+1:]
                    m -= 1
                j += 1

    def _correct_j_vowel(self, syllables: [[[Allophone]]]) -> [[[Allophone]]]:
        n = len(syllables)
        for i in range(n):
            unit = syllables[i]
            m = len(unit)
            for j in range(m):
                cur_syllable, next_syllable = self._get_cur_next(unit, j)
                if next_syllable is not None:
                    p = len(next_syllable)
                    cur_last = self._get_last(cur_syllable)
                    if cur_last is not None and cur_last.is_vowel() and p != 0:
                        to_add, new_next = self._remove_j(next_syllable)
                        unit[j] += to_add
                        unit[j+1] = new_next
                        if len(new_next) == 0:
                            syllables[i] = unit[:j+1] + unit[j+2:]

    def _remove_j(self, syllable: [Allophone]):
        to_remove = []
        idx = None
        found_j = False
        for i in range(len(syllable)):
            allophone = syllable[i]
            if allophone.is_consonant() and allophone.phoneme == "j'":
                found_j = True
                to_remove.append(allophone)
            elif found_j and allophone.is_vowel() and allophone.is_stressed() is False:
                to_remove.append(allophone)
                idx = i
            elif found_j and allophone.is_vowel() and allophone.is_stressed() is True:
                idx = None
                break
            else:
                break
        if idx is not None:
            tmp_new_syllable = syllable[idx + 1:]
            if len(tmp_new_syllable) == 0 or \
                    (len(tmp_new_syllable) != 0 and OpenSyllableUnit().count_vowels(tmp_new_syllable) > 0):
                new_syllable = tmp_new_syllable
            else:
                new_syllable = syllable
                to_remove = []
        else:
            new_syllable = syllable
            to_remove = []
        return to_remove, new_syllable

    def _correct_double_vowels(self, syllables: [[[Allophone]]]) -> [[[Allophone]]]:
        n = len(syllables)
        for i in range(n):
            j = 0
            while j < len(syllables[i]):
                cur_syllable, next_syllable = self._get_cur_next(syllables[i], j)
                if next_syllable is not None:
                    p = len(next_syllable)
                    cur_last = self._get_last(cur_syllable)
                    if cur_last is not None and cur_last.is_vowel() and p != 0:
                        to_add, new_next = self._remove_first_vowels(next_syllable)
                        syllables[i][j] += to_add
                        syllables[i][j+1] = new_next
                        if len(new_next) == 0:
                            syllables[i] = syllables[i][:j+1] + syllables[i][j+2:]
                            j -= 1
                j += 1

    def _remove_first_vowels(self, syllable: [Allophone]):
        to_remove = []
        idx = None
        for i in range(len(syllable)):
            allophone = syllable[i]
            if allophone.is_vowel():
                to_remove.append(allophone)
                idx = i
            else:
                break
        if idx is not None:
            new_syllable = syllable[idx+1:]
        else:
            new_syllable = syllable
        if self._contains_only_consonants(new_syllable):
            to_remove += new_syllable
            new_syllable = []
        return to_remove, new_syllable

    def _split_syllables(self, units: [[Allophone]]):
        syllables = [[]]
        for i in range(len(units)):
            unit = units[i]
            m = len(unit)
            for j in range(m):
                allophone = unit[j]
                n = len(syllables) - 1
                next_alloohine = None
                if j + 1 <= m - 1:
                    next_alloohine = unit[j + 1]
                syllables[n].append(allophone)
                if next_alloohine is not None:
                    if allophone.is_vowel() is True and next_alloohine.is_vowel() is False:
                        syllables.append([])
                else:
                    syllables.append([])
                a = 1
        syllables = self._delete_empty_elements(syllables)
        return syllables

    def _split_syntagmas(self, allophones: [Allophone]) -> [[Allophone]]:
        words = [[]]
        n = len(allophones)
        for i in range(n):
            allophone = allophones[i]
            if allophone.is_pause() is True and allophone.is_word_pause() is False:
                words.append([])
            elif allophone.is_pause() is False:
                m = len(words) - 1
                words[m].append(allophone)
        words_corrected = self._delete_empty_elements(words)
        return words_corrected

    def _split_words(self, allophones: [Allophone]) -> [[Allophone]]:
        words = [[]]
        n = len(allophones)
        for i in range(n):
            allophone = allophones[i]
            if allophone.is_pause() is True:
                words.append([])
            else:
                m = len(words) - 1
                words[m].append(allophone)
        words_corrected = self._delete_empty_elements(words)
        return words_corrected

    def _delete_empty_elements(self, arr: [[]]):
        corrected = []  # без пустых слов
        for elem in arr:
            if len(elem) != 0:
                corrected.append(elem)
        return corrected

    def _get_cur_next(self, unit, cur_idx):
        cur = None
        _next = None
        if len(unit) > cur_idx >= 0:
            cur = unit[cur_idx]
        if len(unit) > cur_idx + 1 >= 0:
            _next = unit[cur_idx + 1]
        return cur, _next

    def _get_last(self, arr):
        n = len(arr) - 1
        last = None
        if n >= 0:
            last = arr[n]
        return last

    def _contains_only_consonants(self, arr: [Allophone]) -> bool:
        res = True
        for a in arr:
            if a.is_vowel() is True:
                res = False
                break
        return res
