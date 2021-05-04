import logging

class AccessManager:
    @staticmethod
    def find_abbreviation(abbr):
        am = AbberviationsAccessManager()
        found_abbr = am.find_abbreviation(abbr)
        return found_abbr

    @staticmethod
    def find_reduction(red):
        am = ReductionsAccessManager()
        found_red = am.find(red)
        return found_red


class Reduction:
    name = None
    decoding = None

    class __DecodingItem:
        def __init__(self, item, freq):
            self.item = item
            self.freq = freq

        def __str__(self):
            return '<DecodingItem object, item = {0}, freq = {1}>'.format(self.item, self.freq)

    def get_decoding(self):
        if len(self.decoding) == 0:
            return None
        max_freq = self.decoding[0].freq
        idx = 0
        for i in range(len(self.decoding)):
            if self.decoding[i].freq > max_freq:
                max_freq = self.decoding[i].frec
                idx = i
        return self.decoding[i].item

    def build(self, name, decoding):
        self.name = name
        self.decoding = []
        return self.parse_decoding(decoding)

    def parse_decoding(self, decoding):
        for d in decoding:
            buff = d.split('{')
            if len(buff) != 2:
                return False
            buff[1] = buff[1].rstrip('}')
            if len(buff[0]) == 0 or len(buff[1]) == 0:
                return False
            item = self.__DecodingItem(buff[0], buff[1])
            self.decoding.append(item)
        return True


class AbberviationsAccessManager:
    __filename = 'data/abbreviations'

    def find(self, abbr):
        with open(self.__filename, 'r', encoding='utf8') as f:
            pass
