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


class ReductionsAccessManager:
    __filename = './modules/database/data/reductions'

    def parse_reduction(self, text):
        buff = text.split('><')
        if len(buff) != 2:
            logging.error('Error while parsing reductions db file: ' + text + ' ?')
            return None
        buff[0] = buff[0].lstrip('<')
        buff[1] = buff[1].rstrip('>')
        decodings = buff[1].split(',')

        if len(decodings) == 1 and len(decodings[0]) == 0:
            logging.error('Error while parsing reductions db file: ' + text + ' ?')
            return None
        for i in range(len(decodings)):
            decodings[i] = decodings[i].strip()
        reduction = Reduction()
        if reduction.build(buff[0], decodings) is False:
            logging.error('Error while parsing reductions db file: ' + text + ' ?')
        return reduction

    def find(self, red):
        with open(self.__filename, 'r', encoding='utf8') as f:
            run = True
            reduction = None
            while run:
                text = f.readline()
                if len(text) == 0:
                    run = False
                else:
                    cur_reduction = self.parse_reduction(text)
                    if cur_reduction.name == red:
                        run = False
                        reduction = cur_reduction
        return reduction


class AbberviationsAccessManager:
    __filename = 'data/abbreviations'

    def find(self, abbr):
        with open(self.__filename, 'r', encoding='utf8') as f:
            pass
