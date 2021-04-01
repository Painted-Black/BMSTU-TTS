class LetterPhonemeTranscriptor:
    M1 = {'_'}
    M2 = {'#'}
    M3 = {'+', '='}
    M4 = {'Ь', }
    M5 = {'Ъ', }
    M6 = {'О', 'У', 'А', 'Ы', 'Э'}
    M7 = {'Е', 'Ё', 'Ю', 'Я', 'И'}
    M8 = {'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'К', 'Л', 'М', 'Н',
          'П', 'Р', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ'}
    M9 = {'К', 'П', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ'}
    M10 = {'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'Л', 'М', 'Н', 'Р'}
    M11 = {'П', 'Ф'}
    M12 = {'Б', 'В', 'М'}
    M13 = {'Т', 'С'}
    M14 = {'Н', 'Д', 'З', 'Л'}
    M15 = {'Х', 'Ц', 'Ч', 'Щ'}
    M16 = {'Б', 'Г', 'Д', 'Ж', 'З'}
    M17 = {'К', 'П', 'С', 'Т', 'Ф', 'Ш'}
    M18 = {'Ц', 'Ш', 'Ж'}
    M19 = {'С', 'Ш', 'Ж'}
    M20 = {'Б', 'В'}
    M21 = {'Д', 'З'}
    M22 = {'К', 'Х'}
    SoftnessPairs = {"b": "b'",
                     "v": "v'",
                     "g": "g'",
                     "d": "d'",
                     "z": "z'",
                     "l": "l'",
                     "m": "m'",
                     "n": "n'",
                     "r": "r'",
                     "p": "p'",
                     "f": "f'",
                     "k": "k'",
                     "t": "t'",
                     "s": "s'",
                     "h": "h'"}
    VoicednessDeafnessPairs = {"b": "p",
                               "b'": "p'",
                               "v": "f",
                               "v'": "f'",
                               "d": "t",
                               "d'": "t'",
                               "g": "k",
                               "g'": "k'",
                               "z": "s",
                               "z'": "s'",
                               "zh": "sh"}

    DeafnessVoicednessPairs = {"p": "b",
                               "p'": "b'",
                               "f": "v",
                               "f'": "v'",
                               "t": "d",
                               "t'": "d'",
                               "k": "g",
                               "k'": "d'",
                               "s": "z",
                               "s'": "z'",
                               "sh": "zh"}

    PairedVoiced = {"b", "g", "d", "z", "v", "zh", "b'", "g'", "d'", "z'", "v'"}
    PairedVoicedMinusV = {"b", "g", "d", "z", "zh", "b'", "g'", "d'", "z'"}
    PairedDVoiceless = {"p", "k", "t", "s", "f", "sh", "p'", "k'", "t'", "s'", "f'"}

    VoicelessConsonants = {"k", "k'", "p", "p'", "s", "s'", "t", "t'", "f", "f'", "x", "x'", "c", "ch'", "sh", "sh'",
                           "h"}
    VoicedConsonants = {"b", "b'", "g", "g'", "d", "d'", "zh", "z", "z'", "j", "l", "l'", "m", "m'", "n", "n'",
                        "r", "r'"}
    VoicedV = {"v", "v'"}

    Softening = {"m": ["p'", "f'", "b'", "m'", "v'"],
                 "n": ["t'", "s'", "z'", "d'", "n'", "l'", "ch'"],
                 "l": ["l'"],
                 "r": ["r'"],
                 "bpvf": ["b'", "v'", "m'", "p'", "f'"],
                 "dtzs": ["n'", "d'", "z'", "t'", "s'"],
                 "gkh": ["g'", "k'", "h'"]}

    text = ''

    additional_symbols = ['_', '#', '+', '=']

    def transcript(self, text: str) -> [str]:
        self.text = text
        phonemes = self.get_raw_phonemes(text)
        phonemes = phonemes.strip(',')
        phonemes = phonemes.split(',')
        softened_phonemes = self.softness_assimilation(phonemes)
        softened_phonemes = self.__remove_extra_symb(softened_phonemes)
        final_phonemes = self.deafness_voicedness_assimilation(softened_phonemes)
        return final_phonemes

    def __remove_extra_symb(self, phonemes: []) -> []:
        count = len(phonemes)
        new_phonemes = []
        for i in range(count):
            if phonemes[i] != "Ъ":
                new_phonemes.append(phonemes[i])
        return new_phonemes

    def deafness_voicedness_assimilation(self, phonemes: []) -> []:
        phonemes = self.deafness_assimilation(phonemes)
        phonemes = self.voicedness_assimilation(phonemes)
        return phonemes

    def voicedness_assimilation(self, phonemes: []) -> []:
        phonemes_count = len(phonemes)
        if phonemes_count <= 1:
            return phonemes
        phonemes_count -= 1
        for i in range(phonemes_count, -1, -1):
            if i != phonemes_count:  # and i != 0:
                pi = phonemes[i]
                pi1 = phonemes[i + 1]
                assimilated = False
                if pi in self.PairedDVoiceless - {"f", "f'"}:
                    if pi1 in self.PairedVoicedMinusV:
                        assimilated = True
                    elif pi1 in self.M1 | self.M2:
                        pi2 = None
                        if i + 2 <= phonemes_count:
                            pi2 = phonemes[i + 2]
                        if pi2 is not None and pi2 in self.PairedVoicedMinusV:
                            assimilated = True
                elif pi in {"f", "f'"}:
                    if pi1 in self.PairedVoicedMinusV | self.VoicedV:
                        assimilated = True
                    elif pi1 in self.M1 | self.M2:
                        pi2 = None
                        if i + 2 <= phonemes_count:
                            pi2 = phonemes[i + 2]
                        if pi2 is not None and pi2 in self.PairedVoicedMinusV | self.VoicedV:
                            assimilated = True
                if assimilated:
                    phonemes[i] = self.DeafnessVoicednessPairs[pi]

        return phonemes

    def deafness_assimilation(self, phonemes: []) -> []:
        phonemes_count = len(phonemes)
        if phonemes_count < 1:
            return phonemes
        elif phonemes_count == 1:
            if phonemes[0] in self.PairedVoiced:
                phonemes[0] = self.VoicednessDeafnessPairs[phonemes[0]]
            return phonemes
        phonemes_count -= 1
        for i in range(phonemes_count, -1, -1):
            pi = phonemes[i]
            if i == phonemes_count and pi in self.PairedVoiced:
                phonemes[i] = self.VoicednessDeafnessPairs[pi]
            elif i != phonemes_count:
                if pi in self.PairedVoiced:
                    pi1 = phonemes[i + 1]
                    if pi1 in self.VoicelessConsonants | self.VoicedV:
                        phonemes[i] = self.VoicednessDeafnessPairs[pi]
                    elif pi1 in self.M1 | self.M2:
                        pi2 = None
                        if i + 2 <= phonemes_count:
                            pi2 = phonemes[i + 2]
                        if pi2 is not None and pi2 in self.VoicelessConsonants | self.VoicedV:
                            phonemes[i] = self.VoicednessDeafnessPairs[pi]
        return phonemes

    def softness_assimilation(self, phonemes: []) -> []:
        for i in range(len(phonemes) - 2, -1, -1):
            pi = phonemes[i]
            softened_before = self.is_softened(pi)
            if softened_before is not None:
                pi1 = phonemes[i + 1]
                is_softened = pi1 in softened_before
                if is_softened:
                    phonemes[i] = self.SoftnessPairs[pi]
        return phonemes

    def is_softened(self, phoneme):
        keys = self.Softening.keys()
        for key in keys:
            if key.find(phoneme) != -1:
                return self.Softening[key]
        return None

    def get_raw_phonemes(self, text: str) -> str:
        phonemes = ''
        for i in range(len(text)):
            phonemes += self.get_phoneme(i)
        phonemes = phonemes[:-1]
        return phonemes

    def get_phoneme(self, i):
        if self.idx(i) == 'Ъ':
            return 'Ъ,'
        PhonemeGenerators = [self.f_space, self.f_lattice, self.f_plus, self.f_equ,
                             self.f_u, self.f_e, self.f_o, self.f_a, self.f_y, self.f_i,
                             self.f_sh_s, self.f_ch_s, self.f_c, self.f_h, self.f_h_s,
                             self.f_m, self.f_n, self.f_l, self.f_r, self.f_b, self.f_p, self.f_d, self.f_g,
                             self.f_k, self.f_z, self.f_s, self.f_v, self.f_f, self.f_t, self.f_sh, self.f_zh,
                             self.f_j_s, self.f_b_s, self.f_v_s, self.f_g_s, self.f_d_s, self.f_z_s,
                             self.f_l_s, self.f_m_s, self.f_n_s, self.f_r_s, self.f_p_s,
                             self.f_f_s, self.f_k_s, self.f_t_s, self.f_s_s]
        Phonemes = ['_', '#', '+', '=',
                    'u', 'e', 'o', 'a', 'y', 'i',
                    "sh'", "ch'", "c", "h", "h'",
                    "m", "n", "l", "r", "b", "p", "d", "g",
                    "k", "z", "s", "v", "f", "t", "sh", "zh",
                    "j'", "b'", "v'", "g'", "d'", "z'",
                    "l'", "m'", "n'", "r'", "p'",
                    "f'", "k'", "t'", "s'"]
        idx1 = None
        idx2 = None
        for j in range(len(PhonemeGenerators)):
            res = PhonemeGenerators[j](i)
            if res is True and idx1 is None:
                idx1 = j
            elif res is True and idx2 is None:
                idx2 = j
            if idx1 is not None and idx2 is not None:
                break
        res = ''
        if idx2 is not None and idx1 is not None:
            res = Phonemes[idx2] + ',' + Phonemes[idx1] + ','
        elif idx1 is not None:
            res = Phonemes[idx1] + ','
        return res

    def idx(self, i):
        if (i < 0) or i >= len(self.text):
            return None
        return self.text[i]

    def f_space(self, i):
        return self.idx(i) == '_'

    def f_lattice(self, i):
        return self.idx(i) == '#'

    def f_plus(self, i):
        return self.idx(i) == '+'

    def f_equ(self, i):
        return self.idx(i) == '='

    def f_u(self, i):
        li = self.idx(i)
        return (li == 'У') or (li == 'Ю')

    def f_e(self, i):
        li = self.idx(i)
        return (li == 'Э') or (li == 'Е')

    def f_o(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        return (li == 'Ё') or ((li == 'О') and (li1 in self.M3))

    def f_a(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        return (li == 'А') or (li == 'Я') or ((li == 'О') and (li1 not in self.M3))

    def f_y(self, i):
        li = self.idx(i)
        return (li == 'Ы') or ((li == 'И') and self.f1(i))

    def f_i(self, i):
        li = self.idx(i)
        return (li == 'И') and not self.f1(i)

    def f_sh_s(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        return (li == 'Щ') or ((li in self.M19) and (li1 == 'Ч'))

    def f_ch_s(self, i):
        li = self.idx(i)
        li_1 = self.idx(i - 1)
        li1 = self.idx(i + 1)
        f15 = self.f15(i)
        f14 = self.f14(i)
        r1 = ((li == 'Ч') and (li_1 not in self.M19)) and not f15 and not f14
        r2 = ((li == 'Т') and (li1 == 'Ч')) and not f15
        r3 = ((li == 'Д') and (li1 == 'Ч')) and not f14
        return r1 or r2 or r3

    def f_c(self, i):
        li = self.idx(i)
        res = (li == 'Ц') or self.f17(i)
        return res

    def f_h(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        return ((li == 'Х') and not self.f2(i + 1)) or ((li == 'Г') and (li1 == 'К') and not self.f2(i + 2))

    def f_h_s(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        return ((li == 'Х') and self.f2(i + 1)) or ((li == 'Г') and (li1 == 'К') and self.f2(i + 2))

    def f_j_s(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li_1 = self.idx(i - 1)
        res = (li == 'Й') or ((li == 'И') and (li_1 in self.M4)) or (
                    (li == 'О') and (li_1 in self.M4) and (li1 in self.M3)) or \
              (((li == 'Я') or (li == 'Е') or (li == 'Ю') or (li == 'Ё')) and self.f3(i))
        return res

    def f_m(self, i):
        li = self.idx(i)
        return li == 'М' and not self.f2(i + 1)

    def f_m_s(self, i):
        li = self.idx(i)
        return li == 'М' and self.f2(i + 1)

    def f_n(self, i):
        li = self.idx(i)
        return li == 'Н' and not self.f2(i + 1)

    def f_n_s(self, i):
        li = self.idx(i)
        return li == 'Н' and self.f2(i + 1)

    def f_l(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li2 = self.idx(i + 2)
        res = (li == 'Л') and ((li1 != 'Н') or (li2 != 'Ц')) and not self.f2(i + 1)
        return res

    def f_l_s(self, i):
        li = self.idx(i)
        res = (li == 'Л') and self.f2(i + 1)
        return res

    def f_r(self, i):
        li = self.idx(i)
        res = li == 'Р' and not self.f2(i + 1)
        return res

    def f_r_s(self, i):
        li = self.idx(i)
        res = li == 'Р' and self.f2(i + 1)
        return res

    def f_b(self, i):
        li = self.idx(i)
        res = li == 'Б' and not self.f2(i + 1)
        return res

    def f_b_s(self, i):
        li = self.idx(i)
        res = li == 'Б' and self.f2(i + 1)
        return res

    def f_p(self, i):
        li = self.idx(i)
        return li == 'П' and not self.f2(i + 1)

    def f_p_s(self, i):
        li = self.idx(i)
        return li == 'П' and self.f2(i + 1)

    def f_v(self, i):
        li = self.idx(i)
        res = (li == 'В' or self.f12(i)) and not self.f2(i + 1)
        return res

    def f_v_s(self, i):
        li = self.idx(i)
        res = li == 'В' and self.f2(i + 1)
        return res

    def f_f(self, i):
        li = self.idx(i)
        return li == 'Ф' and not self.f2(i + 1)

    def f_f_s(self, i):
        li = self.idx(i)
        return li == 'Ф' and self.f2(i + 1)

    def f_d(self, i):
        li = self.idx(i)
        res = li == 'Д' and not self.f14(i) and not self.f2(i + 1)
        return res

    def f_d_s(self, i):
        li = self.idx(i)
        res = li == 'Д' and not self.f14(i) and self.f2(i + 1)
        return res

    def f_t(self, i):
        li = self.idx(i)
        res = li == 'Т' and not self.f15(i) and not self.f2(i + 1)
        return res

    def f_t_s(self, i):
        li = self.idx(i)
        res = li == 'Т' and self.f2(i + 1) and not self.f15(i)
        return res

    def f_g(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        res = li == 'Г' and li1 != 'К' and not self.f12(i) and not self.f2(i + 1)
        return res

    def f_g_s(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        res = li == 'Г' and self.f2(i + 1)
        return res

    def f_k(self, i):
        li = self.idx(i)
        return li == 'К' and not self.f2(i + 1)

    def f_k_s(self, i):
        li = self.idx(i)
        return li == 'К' and self.f2(i + 1)

    def f_z(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        res = li == 'З' and li1 != 'Ж' and not self.f2(i + 1)
        return res

    def f_z_s(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        res = li == 'З' and self.f2(i + 1)
        return res

    def f_s(self, i):
        li = self.idx(i)
        res = li == 'С' and not self.f16(i) and not self.f2(i + 1)
        return res

    def f_s_s(self, i):
        li = self.idx(i)
        res = li == 'С' and self.f2(i + 1) and not self.f16(i)
        return res

    def f_zh(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        r1 = li == 'З' and li1 == 'Ж'
        r2 = li == 'Ж' and li1 == 'Ч'
        res = (li == 'Ж' or r1) and not r2
        return res

    def f_sh(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        r1 = li == 'С' and li1 == 'Ш'
        r2 = li == 'Ш' and li1 == 'Ч'
        res = (li == 'Ш' or r1) and not r2
        return res

    def f16(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li_1 = self.idx(i - 1)
        li_2 = self.idx(i - 2)
        sch = li1 == 'Ч'
        ssh = li1 == 'Ш'
        ts = li_1 == 'Т'
        tss = li_1 == 'Ь' and li_2 == 'Т'
        res = li == 'С' and (sch or ssh or ts or tss)
        return res

    def f17(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li2 = self.idx(i + 2)
        li_1 = self.idx(i - 1)
        r1 = li == 'Т' and (li1 == 'С' or (li1 == 'Ь' and li2 == 'С'))
        r2 = li == 'Т' and li1 == 'Ц' or li_1 == 'Т' and li == 'Ц'
        r3 = (li == 'Д' and li1 == 'С' or li_1 == 'Д' and li == 'С')
        r4 = (li == 'Д' and li1 == 'Ц' or li_1 == 'Д' and li == 'Ц') and not self.f18(i)
        return r1 or r2 or r3 or r4

    def f15(self, i):  # Т в непроизносимых сочетаниях
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li2 = self.idx(i + 2)
        li_1 = self.idx(i - 1)
        stn = li_1 == 'С' and li1 == 'Н'
        stl = li_1 == 'С' and li1 == 'Л'
        ntg = li_1 == 'Н' and li1 == 'Г'
        tc = li1 == 'Ц'
        ts = li1 == 'С'
        tss = li1 == 'Ь' and li2 == 'С'
        tch = li1 == 'Ч'
        return li == 'Т' and (stn or stl or ntg or tc or ts or tss or tch)

    def f14(self, i):  # Д в непроизносимых сочетаниях
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li_1 = self.idx(i - 1)
        dc = li1 == 'Ц'
        ds = li1 == 'С'
        dch = li1 == 'Ч'
        zdn = li_1 == 'З' and li1 == 'Н'
        ndsh = li_1 == 'Н' and li1 == 'Ш'
        ndt = li_1 == 'Н' and li1 == 'Т'
        gdt = li_1 == 'Г' and li1 == 'Т'
        rdch = li_1 == 'Р' and li1 == 'Ч'
        res = li == 'Д' and (dch or dc or ds or zdn or ndsh or ndt or gdt or rdch or self.f18(i))
        return res

    def f18(self, i):
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li_1 = self.idx(i - 1)
        zdc = li_1 == 'З' and li1 == 'Ц'
        ndc = li_1 == 'Н' and li1 == 'Ц'
        rdc = li_1 == 'Р' and li1 == 'Ц'
        res = li == 'Д' and (zdc or ndc or rdc)
        return res

    def f13(self, i):
        li1 = self.idx(i + 1)
        li2 = self.idx(i + 2)
        r1 = li1 is not None
        r2 = not (li2 is None and li1 in self.M1 | self.M2)
        r3 = not (li1 in self.M4 and li2 is None)
        return r1 and r2 and r3

    def f12(self, i):  # если ОГО или ЕГО
        li = self.idx(i)
        li1 = self.idx(i + 1)
        li_1 = self.idx(i - 1)
        li_2 = self.idx(i - 2)
        li_3 = self.idx(i - 3)
        li_4 = self.idx(i - 4)
        li_5 = self.idx(i - 5)
        mnogo = (li_1 == 'О' and li_2 == 'Н' and li_3 == 'М') or \
                (li_1 == '+' and li_2 == 'О' and li_3 == 'Н' and li_4 == 'М')
        dorogo = (li_1 == 'О' and li_2 == 'Р' and li_3 == 'О' and li_4 == 'Д') or \
                 (li_1 == 'О' and li_2 == 'Р' and li_3 == '+' and li_4 == 'О' and li_5 == 'Д')
        r1 = (li == 'Г')
        r2 = (li_1 == 'Е' or li_1 == 'О' or (li_1 == '+' and (li_2 == 'Е' or li_2 == 'О')))
        r3 = (li1 == 'О')

        return r1 and r2 and r3 and not mnogo and not dorogo

    def f7(self, k):  # если фонема парная глухая
        lk = self.idx(k)
        return lk in self.M17

    def f6(self, k):  # если разделитель между словами
        lk = self.idx(k)
        return lk in self.M1 | self.M5

    def f5(self, k):  # если фонема парная звонкая
        lk = self.idx(k)
        return lk in self.M16

    def f4(self, k):  # если фонема глухая
        lk = self.idx(k)
        return lk in self.M9

    def f3(self, i):
        li_1 = self.idx(i - 1)
        union = self.M1 | self.M2 | self.M3 | self.M4 | self.M5 | self.M6 | self.M7
        return li_1 in union or li_1 is None  # !!

    def f2(self, k):  # если мягкая
        lk = self.idx(k)
        return lk in (self.M4 | self.M7)

    def f1(self, i):
        li_1 = self.idx(i - 1)
        li_2 = self.idx(i - 2)
        return (li_1 in self.M18) or ((li_1 in (self.M1 | self.M5)) and (li_2 in self.M8))
