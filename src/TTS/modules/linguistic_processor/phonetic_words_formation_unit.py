class PhoneticWordsFormationUnit:
    def __init__(self):
        self.__join_prev = ("бы", "де", "дескать", "ли", "же", "мол", "то", "ка", "либо", "нибудь")

    def form(self, stressed_words: [], tags: []) -> []:
        # сначала присоединяем энклитики
        phonetic_words = []
        n = len(stressed_words)
        tags_copy = []
        for i in range(n):
            word = stressed_words[i]
            tag = tags[i]
            if tag.is_stressed is True:
                phonetic_words.append(word)
                tags_copy.append(tag)
            else:
                if word in self.__join_prev and tag.tag.POS == "PRCL":
                    m = len(phonetic_words) - 1
                    if m >= 0:
                        phonetic_words[m] = phonetic_words[m] + word
                else:
                    phonetic_words.append(word)
                    tags_copy.append(tag)
        # теперь присоединяем проклитики
        new_phonetic_words = []
        m = len(phonetic_words) - 1
        for i in range(m, -1, -1):
            word = phonetic_words[i]
            tag = tags_copy[i]
            if tag.is_stressed is True:
                new_phonetic_words.append(word)
            else:
                n = len(new_phonetic_words) - 1
                if m >= 0:
                    new_phonetic_words[n] = word + new_phonetic_words[n]
        new_phonetic_words.reverse()
        return new_phonetic_words
