class Sentence:
    '''
    0 -- повествовательное
    1 -- вопросительное
    2 -- восклицательное
    '''
    type = 0
    raw_data = ""
    words = []
    phonetic_words = []
    tagged_words = []

    def __init__(self, text: str):
        self.raw_data = text.strip()
        self.__init_type()

    def __init_type(self):
        n = len(self.raw_data) - 1
        if n < 0:
            return
        if self.raw_data[n] == '?':
            self.type = 1
        elif self.raw_data[n] == '!':
            self.type = 2
        else:
            self.type = 0

    def __repr__(self):
        return f"[{self.raw_data}]_{self.type}"
