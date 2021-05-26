from tts import TTS
import logging
import sys

Filename = "./example_input/ex_in2"
Mode = 4


def main():
    if len(sys.argv) != 2:
        logging.error("Using defaul file path")
        filename = Filename
    else:
        filename = sys.argv[1]
    text = get_text(filename)
    if text is not None:
        tts = TTS("./output/out.wav", "wav")
        tts.process(text, Mode)
    else:
        return -1
    return 0


def get_text(filename: str) -> str:
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
