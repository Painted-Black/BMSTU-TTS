from modules.allophone import Allophone


class OpenSyllableUnit:
    def process(self, allophones: [Allophone]) -> [[Allophone]]:
        count_syllable = self.__count_vowels(allophones)
        if count_syllable <= 1:
            return [allophones]
        syllables = [[]]
        for i in range(len(allophones)):
            allophone = allophones[i]
            n = len(syllables) - 1
            syllables[n].append(allophone)
            if allophone.is_vowel() and i != len(allophones) - 1:
                syllables.append([])
        n = len(syllables) - 1
        if n >= 1:
            m = len(syllables[n]) - 1
            if m == 0 and syllables[n][m].is_vowel() is False:
                prev_syllable = syllables[n-1]
                prev_syllable.append(syllables[n][m])
                syllables = syllables[:-1]
        return syllables

    def __count_vowels(self, allophones: [Allophone]) -> int:
        count = 0
        for allophone in allophones:
            if allophone.is_vowel():
                count += 1
        return count