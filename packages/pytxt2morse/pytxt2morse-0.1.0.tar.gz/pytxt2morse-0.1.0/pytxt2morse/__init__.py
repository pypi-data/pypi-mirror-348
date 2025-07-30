from .pytxt2morse import txt2morse, morse2txt

class MorseConverter:
    def __init__(self):
        self.txt2morse = txt2morse
        self.morse2txt = morse2txt

import sys
sys.modules[__name__] = MorseConverter()