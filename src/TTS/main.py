from tts import TTS
import logging
from db_load import load_stress_db

Filename = "./example_input/ex_in1"


def main():
    text = get_text(Filename)
    if text is not None:
        tts = TTS("./output/out.wav", "wav")
        tts.process(text)


def get_text(filename: str) -> str:
    #return "Привет"
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        logging.warning(f"File '{filename}' not found")
        return None
    text_lines = f.readlines()
    text = lines_to_str(text_lines)
    return text


def lines_to_str(lines: [str]) -> str:
    text = ""
    for line in lines:
        text += line.strip('\n')
    return text


if __name__ == '__main__':
    main()


# интерфейс
# презентация: постановка задачи, задачи, разработка, заключение
# во вторник 12 в 141
