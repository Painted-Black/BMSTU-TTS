import pickle
from .symbols_base import is_vowel, count_vowels
from pymorphy2 import MorphAnalyzer


class StressMarker:
    def __init__(self, stress_db_connection, main_stress_mark, secondary_stress_mark):
        self.stress_db_connection = stress_db_connection
        self.main_stress_mark = main_stress_mark
        self.secondary_stress_mark = secondary_stress_mark

    def mark(self, words: [], morphs: []) -> []:
        stresses = []
        n = len(words)
        for i in range(n):
            word = words[i]
            tag = morphs[i]
            if tag.is_stressed is True:
                stress = self.__get_stress(tag)
                stresses.append(stress)
            else:
                stresses.append(word)
        return stresses

    def __get_stress(self, tag):
        res = None
        if 'ё' in tag.item:
            res = self.__mark_jo_stress(tag.item)
        else:
            stress_forms = self.stress_db_connection.read(pickle.dumps(tag.normal_form))
            if stress_forms is not None:
                stress_forms = pickle.loads(stress_forms)
                res = self.__chose_stress(stress_forms, tag)
                if res is None:
                    res = self.__stress_unknown_word(tag.item)
            else:
                res = self.__stress_unknown_word(tag.item)
        return res

    def __mark_jo_stress(self, word: str) -> str:
        jo_idx = word.find('ё')
        stress = word[:jo_idx+1] + "+" + word[jo_idx+1:]
        return stress

    def __chose_stress(self, stress_forms, morph) -> str:
        analyzer = MorphAnalyzer()
        chosen_form = None
        stress = None
        for stress_form in stress_forms:
            s_form = stress_form[0].replace(self.main_stress_mark, '')
            s_form = s_form.replace(self.secondary_stress_mark, '')
            stress_tag = analyzer.parse(s_form)[0].tag
            if stress_tag.POS == morph.tag.POS or len(stress_forms) == 1 or\
               (morph.tag.POS == "VERB" and stress_tag.POS == "INFN"):
                chosen_form = stress_form
        if chosen_form is None:
            return None
        homonyms = []
        for s in chosen_form:
            s_form = s.replace(self.main_stress_mark, '')
            s_form = s_form.replace(self.secondary_stress_mark, '')
            if s_form == morph.item:
                homonyms.append(s)
        index = 0
        max_idx = len(analyzer.parse(morph.item))
        for homonym in homonyms:
            if index == max_idx or stress is not None:
                break
            s_form = homonym.replace(self.main_stress_mark, '')
            s_form = s_form.replace(self.secondary_stress_mark, '')
            cur_tag = analyzer.parse(s_form)[index]
            if cur_tag.tag == morph.tag and cur_tag.normal_form == morph.normal_form:
                stress = homonym
        if stress is not None:
            stress = stress.replace(self.main_stress_mark, '+')
            stress = stress.replace(self.secondary_stress_mark, '=')
        return stress

    def __stress_unknown_word(self, word):
        res = ""
        if count_vowels(word) == 1:
            res = self.__stress_single_vowel(word)
        else:
            for letter in word:
                if is_vowel(letter):
                    res += letter
                    res += "="
                else:
                    res += letter
        return res

    def __stress_single_vowel(self, word: str) -> str:
        n = len(word)
        idx = None
        for i in range(n):
            if is_vowel(word[i]):
                idx = i
                break
        if idx is not None:
            word = word[:idx] + "+" + word[idx:]
        return word
