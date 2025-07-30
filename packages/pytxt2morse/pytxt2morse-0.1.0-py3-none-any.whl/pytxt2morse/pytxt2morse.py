MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',

    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',

    '.': '.-.-.-',    ',': '--..--',    '?': '..--..',
    "'": '.----.',    '!': '-.-.--',    '/': '-..-.',
    '(': '-.--.',     ')': '-.--.-',    '&': '.-...',
    ':': '---...',    ';': '-.-.-.',    '=': '-...-',
    '+': '.-.-.',     '-': '-....-',    '_': '..--.-',
    '"': '.-..-.',    '$': '...-..-',   '@': '.--.-.',

    ' ': '/'
}

REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def txt2morse(text):
    result = []
    for char in text:
        upper_char = char.upper()               
        morse = MORSE_CODE_DICT.get(upper_char)  
        if morse:
            result.append(morse)                 
    return ' '.join(result)                    

def morse2txt(morse):
    result = []
    morse_chars = morse.split()               
    for code in morse_chars:
        char = REVERSE_DICT.get(code)       
        if char:
            result.append(char)               
    return ''.join(result)        