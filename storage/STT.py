from logging import Logger
from os import path
import logging

import speech_recognition as sr


class STT:
    def __init__(self, logger: Logger):
        self.logger = logger

    def file_to_text(self, file_path):
        audio_file = path.join(path.dirname(path.realpath(__file__)), file_path)
        audio = sr.AudioData.from_file(audio_file)
        r = sr.Recognizer()
        try:
            text = r.recognize_sphinx(audio)
            self.logger.info(f"successfully extract the text from audio: {file_path}")
            return text
        except sr.UnknownValueError:
            self.logger.error("Sphinx could not understand audio")
        except sr.RequestError as e:
            self.logger.error("Sphinx error; {0}".format(e))

