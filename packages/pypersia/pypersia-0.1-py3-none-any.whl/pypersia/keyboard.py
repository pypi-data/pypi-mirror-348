keyboard_map = {
    "a": "ش", "s": "س", "d": "ی", "f": "ب", "g": "ل", "h": "ا", "j": "ت",
    "k": "ن", "l": "م", ";": "ک", "q": "ض", "w": "ص", "e": "ث", "r": "ق",
    "t": "ف", "y": "غ", "u": "ع", "i": "ه", "o": "خ", "p": "ح", "[": "ج",
    "]": "چ", "z": "ظ", "x": "ط", "c": "ز", "v": "ر", "b": "ذ", "n": "د",
    "m": "پ", ",": "و", ".": ".", "/": "/"
}

def fix_persian_keyboard(text: str) -> str:
    """Convert Persian text typed in English layout to correct Persian characters."""
    return "".join(keyboard_map.get(char, char) for char in text)

