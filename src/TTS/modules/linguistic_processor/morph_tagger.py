from pymorphy2.tagset import OpencorporaTag
from pymorphy2 import MorphAnalyzer
from modules.linguistic_processor.words_extractor import WordsExtractor


class MorphTagger:
    def __init__(self):
        self.__ma = MorphAnalyzer()

    def tag(self, words: []) -> []:
        tags = []
        n = len(words)
        for i in range(n):
            word = words[i]
            if "-" in word:
                tag = OpencorporaTag("PRCL")
                word = word.replace('-', '')
                words[i] = word
                morph_item = MorphologicalItem(tag, word, word, False, False)
            else:
                tag = self.__ma.parse(word)[0]
                morph_item = MorphologicalItem(tag.tag, tag.normal_form, tag.word, False)
                if WordsExtractor.is_service_word(word, tag.tag.POS) is True:
                    morph_item.is_stressed = False
            tags.append(morph_item)
        return tags


class MorphologicalItem:
    def __init__(self, tag: OpencorporaTag, normal_form: str, item: str, is_abbrev: bool, is_stressed=True):
        self.item = item
        self.tag = tag
        self.normal_form = normal_form
        self.is_abbrev = is_abbrev
        self.is_stressed = is_stressed

    def __repr__(self):
        return 'MorphologicalItem: item = {0}, tag = {1}, normal_form = {2}'.format(self.item, self.tag, self.normal_form)
