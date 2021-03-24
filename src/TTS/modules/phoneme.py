class Phoneme:
    Vowels = {'u', 'e', 'o', 'a', 'y', 'i'}
    Consonants = {"sh'", "ch'", "c", "h", "h'",
                  "m", "n", "l", "r", "b", "p", "d", "g",
                  "k", "z", "s", "v", "f", "t", "sh", "zh",
                  "j'", "b'", "v'", "g'", "d'", "z'",
                  "l'", "m'", "n'", "r'", "p'",
                  "f'", "k'", "t'", "s'"}
    Pauses = {"_", "#"}
    Stress = {"+", "="}
    SolidLabial = {"p", "f", "b", "m", "v"}
    FrontMiddleLingual = {"sh", "zh", "r", "t", "c", "s", "d", "z", "n", "l"}
    SolidBacklingualVowel = {"k", "h", "g", "u", "o", "a", "e", "y"}
    Soft = {"t'", "s'", "d'", "z'", "n'",
            "l'", "ch'", "sh'", "r'", "p'",
            "f'", "b'", "v'", "m'", "k'",
            "h'", "g'", "j'", "i"}
    FrontBackLingualSolidConsonantsVowels = FrontMiddleLingual | SolidBacklingualVowel
    VoicelessConsonants = {"k", "k'", "p", "p'", "s", "s'", "t", "t'", "f", "f'", "x", "x'", "c", "ch'", "sh", "sh'",
                           "h"}
    VoicedConsonants = {"b", "b'", "g", "g'", "d", "d'", "zh", "z", "z'", "j", "l", "l'", "m", "m'", "n", "n'",
                        "r", "r'", "v", "v'"}

    @staticmethod
    def is_voiseless_cons(phoneme) -> bool:
        return phoneme in Phoneme.VoicelessConsonants

    @staticmethod
    def is_voiced_cons(phoneme) -> bool:
        return phoneme in Phoneme.VoicedConsonants

    @staticmethod
    def is_front_back_solid_cons_vowel(phoneme) -> bool:
        return phoneme in Phoneme.FrontBackLingualSolidConsonantsVowels

    @staticmethod
    def is_soft(phoneme) -> bool:
        return phoneme in Phoneme.Soft

    @staticmethod
    def is_solid_backlingial_vowel(phoneme) -> bool:
        return phoneme in Phoneme.SolidBacklingualVowel

    @staticmethod
    def is_front_middle_lingial(phoneme) -> bool:
        return phoneme in Phoneme.FrontMiddleLingual

    @staticmethod
    def is_solid_labial(phoneme) -> bool:
        return phoneme in Phoneme.SolidLabial

    @staticmethod
    def is_pause(phoneme) -> bool:
        return phoneme in Phoneme.Pauses

    @staticmethod
    def is_stress(phoneme) -> bool:
        return phoneme in Phoneme.Stress

    @staticmethod
    def is_vowel(phoneme) -> bool:
        return phoneme in Phoneme.Vowels

    @staticmethod
    def is_consonant(phoneme) -> bool:
        return phoneme in Phoneme.Consonants
