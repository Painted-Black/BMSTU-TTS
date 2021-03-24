from abc import ABC
from modules.phoneme import Phoneme


class Allophone(ABC):
    phoneme = 0


class VowelAllophone(Allophone):
    '''
    Позиционный индекс:
        0 -- ударный
        1 -- безударный
    Индекс левого контекста:
        0 -- после паузы
        1 -- после твердых губных
        2 -- после передне- и среднеязычных
        3 -- после твёрдых заднеязычных и гласных
        4 -- после мягких
    Индекс правого контекста:
        0 -- перед паузой
        1 -- перед губными согласными
        2 -- перед переднеязычными и заднеязычными твёрдыми согласными и гласными /У/, /О/, /А/, /Э/, /Ы/
        3 -- перед мягкими согласными и гласной /И/
    '''
    def __init__(self):
        self.positional_idx = 0
        self.left_context_idx = 0
        self.right_context_idx = 0

    def set_positional_idx(self, next_phoneme):
        if next_phoneme == '+':
            self.positional_idx = 0
        else:
            self.positional_idx = 1

    def set_left_context_idx(self, left_context):
        if Phoneme.is_pause(left_context) or left_context is None:
            self.left_context_idx = 0
        elif Phoneme.is_solid_labial(left_context):
            self.left_context_idx = 1
        elif Phoneme.is_front_middle_lingial(left_context):
            self.left_context_idx = 2
        elif Phoneme.is_solid_backlingial_vowel(left_context):
            self.left_context_idx = 3
        elif Phoneme.is_soft(left_context):
            self.left_context_idx = 4

    def set_right_context_idx(self, rigth_context):
        if Phoneme.is_pause(rigth_context) or rigth_context is None:
            self.right_context_idx = 0
        elif Phoneme.is_solid_labial(rigth_context):
            self.right_context_idx = 1
        elif Phoneme.is_front_back_solid_cons_vowel(rigth_context):
            self.right_context_idx = 2
        elif Phoneme.is_soft(rigth_context):
            self.right_context_idx = 3

    def __repr__(self):
        return f"{self.phoneme}_{self.positional_idx}{self.left_context_idx}{self.right_context_idx}"


class ConsonantAllophone(Allophone):
    '''
    Индекс правого контекста:
        0 -- Пауза
        1 -- Глухой согласный
        2 -- Звонкий согласный
        3 -- Безударный гласный
        4 -- Ударный гласный
    '''
    def __init__(self):
        self.right_context_idx = 0

    def set_right_context_idx(self, right_context, right_contex1):
        if Phoneme.is_pause(right_context) or right_context is None:
            self.right_context_idx = 0
        elif Phoneme.is_voiseless_cons(right_context):
            self.right_context_idx = 1
        elif Phoneme.is_voiced_cons(right_context):
            self.right_context_idx = 2
        elif Phoneme.is_vowel(right_context) and not Phoneme.is_stress(right_contex1):
            self.right_context_idx = 3
        elif Phoneme.is_vowel(right_context) and Phoneme.is_stress(right_contex1):
            self.right_context_idx = 4

    def __repr__(self):
        return f"{self.phoneme}_{self.right_context_idx}"
