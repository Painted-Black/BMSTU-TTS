from modules.phoneme import Phoneme
from modules.allophone import VowelAllophone, ConsonantAllophone


class PhonemeAllophoneTranscriptor:
    def transcript(self, phonemes: [str]):
        allophones = self.get_allophones(phonemes)
        return allophones

    def get_allophones(self, phonemes: [str]):
        allophones = []
        n = len(phonemes)
        for i in range(n):
            phoneme = phonemes[i]
            if Phoneme.is_vowel(phoneme):
                a = VowelAllophone()
                a.phoneme = phoneme
                next_symb = self.get_symb(i+1, phonemes)
                a.set_positional_idx(next_symb)
                prev_phoneme = self.get_phoneme(i-1, phonemes, -1)
                next_phoneme = self.get_phoneme(i+1, phonemes, 1)
                a.set_left_context_idx(prev_phoneme)
                a.set_right_context_idx(next_phoneme)
                allophones.append(a)
            elif Phoneme.is_consonant(phoneme):
                a = ConsonantAllophone()
                a.phoneme = phoneme
                next_phoneme = self.get_symb(i+1, phonemes)
                next_phoneme1 = self.get_symb(i+2, phonemes)
                a.set_right_context_idx(next_phoneme, next_phoneme1)
                allophones.append(a)
        return allophones

    def get_phoneme(self, idx: int, phonemes: [str], step: int):
        res = None
        n = len(phonemes)
        if idx < 0 or idx >= n:
            return res
        res = phonemes[idx]
        if Phoneme.is_pause(res) or Phoneme.is_stress(res):
            idx += step
            if idx < 0 or idx >= n:
                return None
            res = phonemes[idx]
        return res

    def get_symb(self, idx: int, phonemes: [str]):
        n = len(phonemes)
        res = None
        if n > idx >= 0:
            res = phonemes[idx]
        return res
