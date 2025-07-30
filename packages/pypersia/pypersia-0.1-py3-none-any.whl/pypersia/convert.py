def detect_digit_language(number: str) -> str:
    """Detect whether the number contains Persian ('fa') or English ('en') digits."""
    fa_digits = set("۰۱۲۳۴۵۶۷۸۹")
    en_digits = set("0123456789")

    if any(digit in fa_digits for digit in number):
        return "fa"
    elif any(digit in en_digits for digit in number):
        return "en"
    return "unknown"  

def convert_digits(number: str, lang: str) -> str:

    fa_digits = '۰۱۲۳۴۵۶۷۸۹'
    en_digits = '0123456789'

    translations = {
        "fa": str.maketrans(en_digits, fa_digits),
        "en": str.maketrans(fa_digits, en_digits)
    }

    if lang not in translations:
        raise ValueError("Invalid language! Use 'fa' for Persian or 'en' for English.")

    return number.translate(translations[lang])

