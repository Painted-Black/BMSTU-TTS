from modules.linguistic_processor.linguistic_text_processor import LinguisticTextProcessor
from modules.linguistic_processor.phonetix_exceptions_processor import PhonetixExceptionsProcessor
from confg import *
from modules.database.db_access_manager import db_access_manager
from db_load import load_jo_db


def main():
    load_jo_db()
    return
    abbrev_db_connection = db_access_manager.create_db(PH_EXC_DB_PATH, PH_EXC_DB_NAME)
    pep = PhonetixExceptionsProcessor(abbrev_db_connection)
    res = pep.process(['исключе+ния', 'моде+ль', 'тельави+ва'])
    print(res)
    #lp = LinguisticTextProcessor()
    #text = "Тест извлечения предложений. " \
    #       "Это приемная комиссия ВШЭ? " \
    #       "Текст от ГИБДД со скобками! "
    #res = lp.process(text)
    #text = "НИКТО+_ДРУГО+ГО_ИНЕЖДА+Л#"
    #pt = PhoneticProcessor()
    #res = pt.process(text)
    #ap = AcousticProcessor("./audio_db/", "./output/out.wav", "wav")
    #ap.process(res)
    #print(res)


if __name__ == '__main__':
    main()
