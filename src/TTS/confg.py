import os
from enum import Enum

# databases
STRESS_DB_PATH = os.getcwd() + '/modules/database/stress_db'
PH_EXC_DB_PATH = os.getcwd() + '/modules/database/stress_db'
ABBREV_DB_PATH = os.getcwd() + '/modules/database/stress_db'
CONS_DB_PATH = os.getcwd() + '/modules/database/stress_db'
JO_DB_PATH = os.getcwd() + '/modules/database/stress_db'
STRESS_DB_NAME = 'stress_db'
ABBREV_DB_NAME = 'abbrev_db'
CONS_DB_NAME = 'cons_db'
PH_EXC_DB_NAME = "ph_exc_db"
JO_DB_NAME = "jo_db"
ZALIZNAK_STRESS_FILE_PATH = 'modules/database/data/zaliznak_utf8'
ABBREV_FILE_PATH = 'modules/database/data/abbreviations'
CONS_FILE_PATH = 'modules/database/data/read_consonants'
PH_EXC_FILE_PATH = 'modules/database/data/phonetic_exceptions'
JO_FILE_PATH = 'modules/database/data/jos'
ZALIZNAK_MAIN_STRESS_MARK = "'"
ZALIZNAK_SECONDARY_STRESS_MARK = "`"

# genus
MASCULINE = 'м.'
FEMININE = 'ж.'
NEUTER = 'ср.'
NSPEC = '-'


class GenusEnum(Enum):
    MASCULINE = 0
    FEMININE = 1
    NEUTER = 2
    NSPEC = 3


class Genus:
    value = None

    def build(self, string: str):
        if string == MASCULINE:
            self.value = GenusEnum.MASCULINE
            return self.value
        elif string == FEMININE:
            self.value = GenusEnum.FEMININE
            return self.value
        elif string == NEUTER:
            self.value = GenusEnum.NEUTER
            return self.value
        elif string == NSPEC:
            self.value = GenusEnum.NSPEC
            return self.value
        else:
            return None
