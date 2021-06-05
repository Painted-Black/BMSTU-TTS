from confg import *
from fill_db import fill_db, parse_consonants_pronunciation, parse_stress_string, parse_abbrev_string, \
    parse_ph_exc_string, parse_jo_string
import os


def load_cons_db():
    fill_db(CONS_FILE_PATH, CONS_DB_NAME, CONS_DB_PATH, parse_consonants_pronunciation)


def load_stress_db():
    fill_db(ZALIZNAK_STRESS_FILE_PATH, STRESS_DB_NAME, STRESS_DB_PATH, parse_stress_string)


def load_abbrev_db():
    fill_db(ABBREV_FILE_PATH, ABBREV_DB_NAME, ABBREV_DB_PATH, parse_abbrev_string)


def load_ph_exc_db():
    fill_db(PH_EXC_FILE_PATH, PH_EXC_DB_NAME, PH_EXC_DB_PATH, parse_ph_exc_string)


def load_jo_db():
    fill_db(JO_FILE_PATH, JO_DB_NAME, JO_DB_PATH, parse_jo_string)


def main():
    cons_path = os.path.join(CONS_DB_PATH, CONS_DB_NAME)
    stress_path = os.path.join(STRESS_DB_PATH, STRESS_DB_NAME)
    abbrev_path = os.path.join(ABBREV_DB_PATH, ABBREV_DB_NAME)
    ph_ex_path = os.path.join(PH_EXC_DB_PATH, PH_EXC_DB_NAME)

    os.rmdir(cons_path)
    os.rmdir(stress_path)
    os.rmdir(abbrev_path)
    os.rmdir(ph_ex_path)

    load_cons_db()
    load_stress_db()
    load_abbrev_db()
    load_ph_exc_db()


main()
