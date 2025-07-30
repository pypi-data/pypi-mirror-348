num_words = {
    0: "صفر", 1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج", 6: "شش", 7: "هفت", 8: "هشت", 9: "نه",
    10: "ده", 11: "یازده", 12: "دوازده", 13: "سیزده", 14: "چهارده", 15: "پانزده", 20: "بیست", 30: "سی",
    40: "چهل", 50: "پنجاه", 60: "شصت", 70: "هفتاد", 80: "هشتاد", 90: "نود", 100: "صد",
    1000: "هزار", 1_000_000: "میلیون", 1_000_000_000: "میلیارد", 1_000_000_000_000: "تریلیون"
}

def number_to_persian_words(num: int) -> str:
    """Convert large numbers to Persian words (supports up to 999 trillion)."""
    if num in num_words:
        return num_words[num]

    def convert_chunk(n):
        """Convert numbers under 1000."""
        if n in num_words:
            return num_words[n]
        if n < 20:
            return num_words[n - n % 10] + " و " + num_words[n % 10]
        if n < 100:
            return num_words[n - n % 10] + " و " + num_words[n % 10] if n % 10 else num_words[n]
        return num_words[100] + " و " + convert_chunk(n % 100) if n % 100 else num_words[100]

    def split_number(n):
        """Split number into trillions, billions, millions, thousands, and hundreds."""
        units = [("تریلیون", 1_000_000_000_000), ("میلیارد", 1_000_000_000),
                 ("میلیون", 1_000_000), ("هزار", 1_000)]
        result = []
        for name, value in units:
            if n >= value:
                result.append(convert_chunk(n // value) + " " + name)
                n %= value
        if n:
            result.append(convert_chunk(n))
        return " و ".join(result)

    return split_number(num)