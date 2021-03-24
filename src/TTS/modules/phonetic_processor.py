from pymorphy2 import MorphAnalyzer
from pymorphy2.tagset import OpencorporaTag
from modules.database.db_access_manager import db_access_manager
from confg import *
import pickle
import logging
from modules.letter_phoneme_transcriptor import LetterPhonemeTranscriptor
from modules.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor


class PhoneticProcessor:
    def __init__(self):
        self.lft = LetterPhonemeTranscriptor()
        self.pat = PhonemeAllophoneTranscriptor()

    def process(self, text):
        phonemes = self.lft.transcript(text)
        allophones = self.pat.transcript(phonemes)
        print(allophones)

    @staticmethod
    def __count_homonyms(morph, stresses) -> int:
        count = 0
        for s in stresses:
            s_form = s.replace(ZALIZNAK_MAIN_STRESS_MARK, '')
            s_form = s_form.replace(ZALIZNAK_SECONDARY_STRESS_MARK, '')
            if morph.item == s_form:
                count += 1
        return count

    @staticmethod
    def __remove_homonymy(morph, stresses):
        #logging.warning("Homonymy removal is now not supported")
        stress = None
        analyzer = MorphAnalyzer()
        homonyms = []
        for s in stresses:
            s_form = s.replace(ZALIZNAK_MAIN_STRESS_MARK, '')
            s_form = s_form.replace(ZALIZNAK_SECONDARY_STRESS_MARK, '')
            if s_form == morph.item:
                homonyms.append(s)
        index = 0
        max_idx = len(analyzer.parse(morph.item))
        for homonym in homonyms:
            if index == max_idx or stress is not None:
                break
            s_form = homonym.replace(ZALIZNAK_MAIN_STRESS_MARK, '')
            s_form = s_form.replace(ZALIZNAK_SECONDARY_STRESS_MARK, '')
            cur_tag = analyzer.parse(s_form)[index]
            if cur_tag.tag == morph.tag and cur_tag.normal_form == morph.normal_form:
                stress = homonym
        return stress

    @staticmethod
    def __mark_stress(morph, stresses):
        stress = None
        for s in stresses:
            s_form = s.replace(ZALIZNAK_MAIN_STRESS_MARK, '')
            s_form = s_form.replace(ZALIZNAK_SECONDARY_STRESS_MARK, '')
            if s_form == morph.item:
                stress = s
                break
        return stress

    @staticmethod
    def __word_stress_marking(morphs):
        stress_db = db_access_manager.create_db(STRESS_DB_PATH, STRESS_DB_NAME)
        for morph in morphs:
            if morph.tag == OpencorporaTag('PNCT'):
                continue
            stress = None
            stresses = stress_db.read(pickle.dumps(morph.normal_form))
            if stresses is None:
                logging.warning("Cannot find word '" + morph.item + "' in stress dictionary")
                continue
            stresses = pickle.loads(stresses)
            homonyms_count = PhoneticProcessor.__count_homonyms(morph, stresses)
            if homonyms_count == 0:
                logging.warning("Cannot find stress for word '" + morph.item + "'")
            elif homonyms_count > 1:
                logging.warning("Need to remove homonymy for word '" + morph.item + "'")
                stress = PhoneticProcessor.__remove_homonymy(morph, stresses)
            else:
                stress = PhoneticProcessor.__mark_stress(morph, stresses)
            print(stress)

