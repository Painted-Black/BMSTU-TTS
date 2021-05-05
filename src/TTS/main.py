from modules.linguistic_processor.linguistic_text_processor import LinguisticTextProcessor
from db_load import load_stress_db


def main():
    lp = LinguisticTextProcessor()
    s = lp.init()
    if s is False:
        print("Error")
        return
    text = "Кто-то бы к кругу кто-нибудь где-то"
    # text = "Тест деления на предложения и замок. " \
    #       "Это дескать приемная комиссия ВШЭ? " \
    #       "Текст от ГИБДД со скобками! "
    res = lp.process(text)
    #for s in res:
    #    print(s.stressed_words)
    #text = "НИКТО+_ДРУГО+ГО_ИНЕЖДА+Л#"
    #pt = PhoneticProcessor()
    #res = pt.process(text)
    #ap = AcousticProcessor("./audio_db/", "./output/out.wav", "wav")
    #ap.process(res)
    #print(res)


if __name__ == '__main__':
    main()
