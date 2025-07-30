def ta_marbuta(word, position):
    """
    Exeption function for the letter t when transliterating from English script
    Arabic to Arabic script. If the t is at the end of the word then it is
    transliterated to a Ta Marbuta (ة) instead of a Ta (ت)
    """
    return 'ة' if position == len(word) - 1 else 'ت'

def alif_rule(word, position):
    """
    Exception for a. In most cases this is omitted because the conversion is to
    a vowel sign that is usually not printed. Only at the beginning of the word is
    this converteed to an أ
    """
    return 'أ' if position == 0 else ''

def heh_ar(word, position):
    """
    Exception function for the letter heh in Hebrew.
    If at the end of the word, then use Ta Marbuta instead of Ta
    :param word: for testing if the letter is at the end
    :param position: for testing if the letter is at the end
    :return: Ta or Ta Marbuta
    """
    return 'ة' if position == len(word) - 1 else 'ه'


def heh_en(word, position):
    """
    Exception function for the letter heh in Hebrew.
    If at the end of the word, then use 'a' instead of 'h'
    :param word: for testing if the letter is at the end
    :param position: for testing if the letter is at the end
    :return: h or [a, e]
    """
    return ['a', 'e'] if position == len(word) - 1 else 'h'

def s_de_he(word, position):
    """
    Exception function for s in German to hebrew transliteration.
    If the following letter is t or p return ש otherwise return ז
    :param word:
    :param position:
    :return:
    """
    # if last letter in word, return 'ז'
    if position == len(word) - 1:
        return 'ז'

    # check exception rule
    return 'ש' if word[position + 1] in ['t', 'p'] else 'ז'

# Set of final letter exception functions for Arabic --> Hebrew
def fin_kaf_ar(word, position):
    return ['ּך', 'ק'] if position == len(word) - 1 else ['כּ', 'ק']


def fin_mem_ar(word, position):
    return 'ם' if position == len(word) - 1 else 'מ'


def fin_nun_ar(word, position):
    return 'ן' if position == len(word) - 1 else 'נ'


def fin_zad_ar(word, position):
    return 'ץ' if position == len(word) - 1 else 'צ'

def fin_zad_de(word, position):
    return 'ץ' if position == len(word) - 2 else 'צ'

def fin_zhad_ar(word, position):
    return "ץ'" if position == len(word) - 1 else "צ'"


def fin_peh_ar(word, position):
    return 'ף' if position == len(word) - 1 else 'פ'


def hamza_ya(word, position):  # Hamza is pronounced like Ya
    return 'י' if word[position - 1] == 'ا' else 'א'


def fin_a(word, position):
    return 'ה' if position == len(word) - 1 else ''


HE_AR = {"א": "ا", "ב": "ب", "בּ": "ب", "ג": "چ", "ג'": "ج", "ד": ["د", "ض"], "ד'": "ذ", "ה": heh_ar, "ו": "و",
         "ז": "ز",
         "ח": "ح", "ח'": "خ", "ט": ["ط", "ظ"], "י": "ي", "כּ": "ك", "ךּ": "ك", "כ": "ك", "ך": "ك", "ל": "ل", "מ": "م",
         "ם": "م", "נ": "ن",
         "ן": "ن",
         "ס": "س", "ע": "ع", "ע'": "غ", "פ": "ف", "ף": "ف", "פּ": "ب", "ףּ": "ب", "צ": "ص", "ץ": "ص", "צ'": "ض",
         "ץ'": "ض", "ק": "ق", "ר": "ر", "ש": ["ش", "س"], "ת": "ت", "ת'": "ث", "ָ": "َ", "ַ": "َ", "ִ": "ِ", "ֻ": "ُ",
         "וּ": "ُ", "-": "-", "'": "", "]": "", "׳": "", "[": "",
         "ְ": "ْ"}
# Done: duplicate key  "ד":"ض",
# Done: duplicate key "ט":"ظ",
# Done: Differ between dagesh kal and dagesh hazak
# Done: handle Shin/Sin markings if exist
# Done: handle Kamatz vowel

# TODO New rule for ئ - if follows an א then only add י and not אי
AR_HE = {"ال": "אל", "ا": "א", "إ": "א", "أ": "א", "آ": "א", "ب": "בּ", "چ": "ג", "ج": "ג'", "ؤ": "או", "ئ": hamza_ya,
         "ح": "ח", "خ": "ח'",
         "د": "ד", "ذ": "ד'", "ه": "ה", "ة": "ה", "ز": "ז", "ر": "ר", "ت": "ת", "ث": "ת'", "ط": "ט", "ظ": "ט'",
         "س": "ס", "ش": "ש", "ع": "ע", "غ": "ע'", "ص": fin_zad_ar, "ض": fin_zhad_ar, "ف": fin_peh_ar, "پ": "פּ",
         "ق": "ק", "ك": fin_kaf_ar, "ل": "ל", "م": fin_mem_ar, "ن": fin_nun_ar, "ي": "י", "ى": "א", "ء": "א",
         "و": "ו", "َ": "ַ", "ِ": "ִ", "ُ": ["ֻ", "וּ"], "ْ": "ְ"}
# Done: duplicate key, "ُ": "וּ"
# Done: Add final letter rule for סופיות

# Done: add he/ar vowels
HE_EN = {"א": ["a", "ā", "e"], "או": ["ū", "o", "u"], "אי": ["ʾI", "I"], "ב": ["b", "v"], "בּ": "b", "ג": "g",
         "ג'": ["g", "j"], "ד": ["d", "ḍ"], "ד'": "dh", "ה": heh_en, "ו": ["u", "o"], "ז": ["z", "s"], "ח": "ḥ",
         "ח'": "kh", "ט": ["t", "ṭ"], "י": "ī", "כ": ["k", "c", "q"], "ך": "kh", "ל": "l", "מ": "m", "ם": "m", "נ": "n",
         "ן": "n", "ס": "s", "ע": "ʿ", "ע'": "gh", "פ": ["f", "p"], "ף": "f", "פּ": "p", "ףּ": "p",
         "צ": ["ṣ", "ts", "z"], "ץ": ["ṣ", "ts", "z"], "ז'": ["ẓ", "z", "s"], "צ'": ["ḍ", "ch"], "ץ'": ["ḍ", "ch"],
         "ק": ["k", "q", "c"], "ר": "r", "ש": ["ṣ", "sh"], "ת": "t", "ת'": ["th", "ẓ"], "ַ": "a", "ִ": "i", "ֻ": "u",
         "-": "-", "'": "", "]": "", "׳": "", "[": "",
         "וּ": "u"}

AR_EN = {"ال": "al", "ة": "ah", "ع": "ʿ", "طّ": "ṭṭ", "غ": "gh", "ش": "sh", "ذ": "dh", "خ": "kh", "ث": "th", "ص": "ṣ",
         "ئ": "'ī", "ؤ": "'ū",
         "د": "d", "ا": "ā", "و": "ū", "أ": "a", "آ": "ʼā", "ب": "b", "ت": "t", "پ": "p", "چ": "g", "ه": "h", "ر": "r",
         "ز": "z", "ج": "j", "س": "s", "ض": "ḍ", "ط": "ṭ", "ظ": "ẓ", "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m",
         "ن": "n", "ح": "ḥ", "ي": "ī", "إ": ["ʾi", "ī"], "ى": "a", "ء": "ʾ", "َ": "a", "ِ": "i", "ُ": "u", "ْ": "ʼ"}

DE_HE = {"A": "א", "a": fin_a, "b": "ב", "c": ["צ", "ק", "כ"], "d": "ד", "E": "א", "e": fin_a, "f": "פ", "g": "ג", "h": "ה", "i": "י",
         "j": "י", "k": "ק", "l": "ל", "m": fin_mem_ar, "n": fin_nun_ar, "o": "ו", "p": fin_peh_ar, "q": "ק", "r": "ר", "S": "ז", "s": s_de_he,
         "t": ["ת","ט"], "u": ["ו", "י"], "v": ["ו", "פ"], "w": "ו", "x": ["קס", "כס"], "y": "י", "z": fin_zad_ar, "ä": "א", "ö": "ו", "ü": "ו",
         "ß": "ס", "eo": "או", "ei": "יי", "ch": fin_kaf_ar, "sch": "ש", "nn": fin_nun_ar, "mm": fin_mem_ar, "pp": "פ", "ßß": "ס", "ie": "י",
         "B": "ב", "C": ["צ", "ק", "כ"], "D": "ד", "F": fin_peh_ar, "G": "ג", "H": "ה", "I": "י", "J": "י", "K": "ק", "L": "ל", "M": fin_mem_ar,
         "N": fin_nun_ar, "O": "או", "P": fin_peh_ar, "Q": "ק", "R": "ר", "T": ["ת","ט"], "U": "ו", "V": ["ו", "פ"], "W": "ו",
         "X": ["קס", "כס"], "Y": "י", "Z": fin_zad_ar, "Ä": "א", "Ö": "ו", "Ü": "ו", "ẞ": "ס", "tz": fin_zad_de, "ll":"ל", "Au":"או", "au":"או" ,
         "ia": "יא", "äu": "וי", "eu": "וי", "Sch": "ש", "-": "-", "tt": "ט", "tsch": "טש"}

EN_AR = {
    "ʾ": "ء", "a": alif_rule, "A": "ا", "ā": "ا", "Ā": "ا", "b": "ب", "B": "ب", "t": ta_marbuta, "T": "ت",
    "th": "ث", "Th": "ث", "TH": "ث", "j": "ج", "J": "ج", "ḥ": "ح", "Ḥ": "ح", "kh": "خ", "Kh": "خ", "KH": "خ",
    "d": "د", "D": "د", "dh": "ذ", "Dh": "ذ", "DH": "ذ", "r": "ر", "R": "ر", "z": "ز", "Z": "ز",
    "s": "س", "S": "س", "sh": "ش", "Sh": "ش", "SH": "ش", "ṣ": "ص", "Ṣ": "ص", "ḍ": "ض", "Ḍ": "ض",
    "ṭ": "ط", "Ṭ": "ط", "ẓ": "ظ", "Ẓ": "ظ", "ʿ": "ع", "gh": "غ", "Gh": "غ", "GH": "غ", "f": "ف", "F": "ف",
    "q": "ق", "Q": "ق", "k": "ك", "K": "ك", "l": "ل", "L": "ل", "m": "م", "M": "م", "n": "ن", "N": "ن",
    "h": "ه", "H": "ه", "w": "و", "W": "و", "y": "ي", "Y": "ي", "i": "", "I": "ي", "ī": "ي", "Ī": "ي",
    "u": "و", "U": "و", "ū": "و", "Ū": "و", "'": "ء", "-": "", " ": " ", "bb": "بّ", "BB": "بّ",
    "dd": "دّ", "DD": "دّ", "ff": "فّ", "FF": "فّ", "gh": "غّ", "GH": "غّ", "jj": "جّ", "JJ": "جّ", "kk": "كّ", "KK": "كّ",
    "ll": "لّ", "LL": "لّ", "mm": "مّ", "MM": "مّ", "nn": "نّ", "NN": "ن", "rr": "رّ", "RR": "رّ", "ss": "سّ", "SS": "سّ",
    "th": "تّ", "TH": "تّ", "tt": "تّ", "TT": "تّ", "ww": "وّ", "WW": "وّ", "yy": "يّ", "YY": "يّ", "zz": "زّ", "ZZ": "ز",
}

def non_vowel_at_start(word, position):  # Vav at the beginning of a word is pronounced like V. Otherwise like o or u
    if len(word) > 0 and position == 0:
        return False
    return True


def vowel_at_end(word, position):  # Heh at the end of a word is not pronounced
    if len(word) > 1 and position == len(word) - 1:
        return True
    return False


heb_vowels = {"א": non_vowel_at_start, "וּ": True, "ו": non_vowel_at_start, "י": non_vowel_at_start, "ה": vowel_at_end,
              "ַ": True, "ִ": True, "ֻ": True}
ar_vowels = {"ي": True, "ى": True, "ء": True, "و": non_vowel_at_start, "َ": True, "ِ": True, "ُ": True, "ْ": True}
en_vowels = {"o": non_vowel_at_start, "u": non_vowel_at_start, "O": non_vowel_at_start, "U": non_vowel_at_start
    , "a": non_vowel_at_start, "e": non_vowel_at_start, "i": non_vowel_at_start}

table_lookup = {('he', 'ar'): HE_AR, ('ar', 'he'): AR_HE, ('he', 'en'): HE_EN, ('ar', 'en'): AR_EN, ('de', 'he'): DE_HE,
                'he': heb_vowels, 'ar': ar_vowels, 'en': en_vowels}

SYC_AR = {
    "ܐ": "ا",  # Alaph
    "ܒ": "ب",  # Beth
    "ܓ": "ج",  # Gamal
    "ܕ": "د",  # Dalath
    "ܗ": "ه",  # Heh
    "ܘ": "و",  # Waw
    "ܙ": "ز",  # Zain
    "ܚ": "ح",  # Heth
    "ܛ": "ط",  # Teth
    "ܜ": "ظ",  # not in the standard Syriac alphabet
    "ܝ": "ي",  # Yudh
    "ܟ": "ك",  # Kaph
    "ܠ": "ل",  # Lamadh
    "ܡ": "م",  # Mim
    "ܢ": "ن",  # Nun
    "ܣ": "س",  # Semkath
    "ܥ": "ع",  # 'E
    "ܦ": "ف",  # Peh
    "ܨ": "ص",  # Sadhe
    "ܩ": "ق",  # Qoph
    "ܪ": "ر",  # Resh
    "ܫ": "ش",  # Shin
    "ܬ": "ت",  # Taw
    " ̈": "",  # not verbalized
}

AR_SYC = {
    "ا": "ܐ",  # Alef
    "ب": "ܒ",  # Ba
    "ت": "ܬ",  # Ta
    "ث": "ܬ",  # Tha mapped to Taw
    "ج": "ܓ",  # Jim
    "ح": "ܚ",  # Ha
    "خ": "ܟ",  # Kha mapped to Kaph
    "د": "ܕ",  # Dal
    "ذ": "ܕ",  # Dhal mapped to Dalath
    "ر": "ܪ",  # Ra
    "ز": "ܙ",  # Zay
    "س": "ܣ",  # Sin
    "ش": "ܫ",  # Shin
    "ص": "ܨ",  # Sad
    "ض": "ܨ",  # Dad mapped to Sadhe
    "ط": "ܛ",  # Ta
    "ظ": "ܛ",  # Za mapped to Teth
    "ع": "ܥ",  # Ayn
    "غ": "ܓ",  # Ghayn mapped to Gamal
    "ف": "ܦ",  # Fa
    "ق": "ܩ",  # Qaf
    "ك": "ܟ",  # Kaf
    "ل": "ܠ",  # Lam
    "م": "ܡ",  # Mim
    "ن": "ܢ",  # Nun
    "ه": "ܗ",  # Ha
    "و": "ܘ",  # Waw
    "ي": "ܝ",  # Ya
}

# Update the table_lookup dictionary
table_lookup[('sy', 'ar')] = SYC_AR
table_lookup[('ar', 'sy')] = AR_SYC

SYC_HE = {
    "ܐ": "א",  # Alaph
    "ܒ": "ב",  # Beth
    "ܓ": "ג",  # Gamal
    "ܕ": "ד",  # Dalath
    "ܗ": "ה",  # Heh
    "ܘ": "ו",  # Waw
    "ܙ": "ז",  # Zain
    "ܚ": "ח",  # Heth
    "ܛ": "ט",  # Teth
    "ܜ": "ט'",  # not in the standard Syriac alphabet
    "ܝ": "י",  # Yudh
    "ܟ": "כ",  # Kaph - if at the end  / beginnning shouldn't it be ק?
    "ܠ": "ל",  # Lamadh
    "ܡ": fin_mem_ar,  # Mim
    "ܢ": fin_nun_ar,  # Nun
    "ܣ": "ס",  # Semkath
    "ܥ": "ע",  # 'E
    "ܦ": fin_peh_ar,  # Peh
    "ܨ": "צ",  # Sadhe
    "ܩ": "ק",  # Qoph
    "ܪ": "ר",  # Resh
    "ܫ": "ש",  # Shin
    "ܬ": "ת",  # Taw
    " ̈": "",  # not verbalized
}

HE_SYC = {
    "א": "ܐ",  # Aleph
    "ב": "ܒ",  # Bet
    "ג": "ܓ",  # Gimel
    "ד": "ܕ",  # Dalet
    "ה": "ܗ",  # He
    "ו": "ܘ",  # Vav
    "ז": "ܙ",  # Zayin
    "ח": "ܚ",  # Chet
    "ט": "ܛ",  # Tet
    "י": "ܝ",  # Yod
    "כ": "ܟ",  # Kaf
    "ך": "ܟ",  # Final Kaf
    "ל": "ܠ",  # Lamed
    "מ": "ܡ",  # Mem
    "ם": "ܡ",  # Final Mem
    "נ": "ܢ",  # Nun
    "ן": "ܢ",  # Final Nun
    "ס": "ܣ",  # Samekh
    "ע": "ܥ",  # Ayin
    "פ": "ܦ",  # Pe
    "ף": "ܦ",  # Final Pe
    "צ": "ܨ",  # Tsadi
    "ץ": "ܨ",  # Final Tsadi
    "ק": "ܩ",  # Qof
    "ר": "ܪ",  # Resh
    "ש": "ܫ",  # Shin
    "ת": "ܬ",  # Tav
}

# Update the table_lookup dictionary
table_lookup[('syc', 'he')] = SYC_HE
table_lookup[('he', 'syc')] = HE_SYC

SYC_EN = {
    "ܐ": ["a", "e", "i", "o"],  # Alaph can represent vowels or a glottal stop. TODO: if the aleph is at the end of the word and there is a Teame ( ̈) anywhere in the word then choose e for English and aleph / aliph for other semitic languages
    "ܒ": "b",                   # Beth
    "ܓ": "g",                   # Gamal
    "ܕ": "d",                   # Dalath
    "ܗ": "h",                   # Heh
    "ܘ": ["w", "u", "o"],       # Waw
    "ܙ": "z",                   # Zain
    "ܚ": ["h", "kh"],           # Heth
    "ܛ": ["t", "ṭ"],            # Teth
    "ܜ": "ẓ",                # not in the standard Syriac alphabet
    "ܝ": ["y", "i", "e"],       # Yudh
    "ܟ": "k",                   # Kaph
    "ܠ": "l",                   # Lamadh
    "ܡ": "m",                   # Mim
    "ܢ": "n",                   # Nun
    "ܣ": "s",                   # Semkath
    "ܥ": ["'", "ʿ"],            # 'E
    "ܦ": ["p", "f"],            # Peh
    "ܧ": "p",                   # Reversed Peh
    "ܨ": ["s", "ṣ"],            # Sadhe
    "ܩ": "q",                   # Qoph
    "ܪ": "r",                   # Resh
    "ܫ": "sh",                  # Shin
    "ܬ": "t",                   # Taw
    " ̈": ""  # not verbalized
}

EN_SYC = {
    "a": "ܐ",        # Alaph
    "b": "ܒ",        # Beth
    "c": ["ܟ", "ܣ"], # Kaph or Semkath
    "d": "ܕ",        # Dalath
    "e": "ܐ",        # Alaph
    "f": "ܦ",        # Peh
    "g": "ܓ",        # Gamal
    "h": "ܗ",        # Heh
    "i": "ܝ",        # Yudh
    "j": "ܓ",        # Map 'j' to Gamal
    "k": "ܟ",        # Kaph
    "l": "ܠ",        # Lamadh
    "m": "ܡ",        # Mim
    "n": "ܢ",        # Nun
    "o": "ܐ",        # Alaph
    "p": "ܦ",        # Peh
    "q": "ܩ",        # Qoph
    "r": "ܪ",        # Resh
    "s": "ܣ",        # Semkath
    "t": "ܬ",        # Taw
    "u": "ܘ",        # Waw
    "v": "ܒ",        # Map 'v' to Beth
    "w": "ܘ",        # Waw
    "x": "ܟܣ",       # Kaph followed by Semkath
    "y": "ܝ",        # Yudh
    "z": "ܙ",        # Zain
    "sh": "ܫ",       # Shin
    "kh": "ܚ",       # Heth
    "th": "ܬ",       # Taw
    "ch": "ܟ",       # Kaph
}

# Update the table_lookup dictionary
table_lookup[('syc', 'en')] = SYC_EN
table_lookup[('en', 'syc')] = EN_SYC

def yiddish_shin(word, position):
    """Transliterate ש based on context."""
    if position == 0:
        return "sch"
    if word[position-1] == "ט":
        return "sh"

    return "s"


def yiddish_vov(word, position):
    """Transliterate ו based on context."""
    if position > 0 and word[position - 1] in ["a", "e", "i", "o", "u"]:
        return "v"
    return "u"

def yiddish_yud(word, position):
    """Transliterate י based on context."""
    if position > 0 and word[position - 1] in ["a", "e", "i", "o", "u"]:
        return "y"
    return "i"

YI_EN = {
    "א": "a",  # Alef
    "ב": "b",  # Beis
    "ג": "g",  # Gimel
    "ד": "d",  # Daled
    "ה": "h",  # Hei
    "וו": "w",  # Vov
    "ו": yiddish_vov,  # Vov
    "ז": "z",  # Zayin
    "ח": "kh", # Ches
    "ט": "t",  # Tes
    "י": yiddish_yud,  # Yud
    "כ": "kh", # Kaf
    "ך": "kh", # Final Kaf
    "ל": "l",  # Lamed
    "מ": "m",  # Mem
    "ם": "m",  # Final Mem
    "נ": "n",  # Nun
    "ן": "n",  # Final Nun
    "ס": "s",  # Samekh
    "ע": "e",  # Ayin
    "פ": "f",  # Pei
    "ף": "f",  # Final Pei
    "צ": "ts", # Tzadi
    "ץ": "ts", # Final Tzadi
    "ק": "k",  # Kuf
    "ר": "r",  # Reish
    "ש": yiddish_shin, # Shin
    "ת": "t",  # Tof
    "יי": "ei",  # Yud-Yud
    "יַי": "ai", # Yud-Yud with Patach
    "אַ": "a",  # Patach + aleph
    "ַ": "a",  # Patach
    "אָ": "o",  # Kamatz + aleph
    "ָ": "o",  # Kamatz
}

# Define English to Yiddish transliteration table
EN_YI = {
    "a": "א",  # Alef
    "b": "ב",  # Beis
    "g": "ג",  # Gimel
    "d": "ד",  # Daled
    "h": "ה",  # Hei
    "u": "ו",  # Vov
    "z": "ז",  # Zayin
    "kh": "ח", # Ches
    "t": "ט",  # Tes
    "y": "י",  # Yud
    "l": "ל",  # Lamed
    "m": "מ",  # Mem
    "n": "נ",  # Nun
    "s": "ס",  # Samekh
    "e": "ע",  # Ayin
    "f": "פ",  # Pei
    "ts": "צ", # Tzadi
    "k": "ק",  # Kuf
    "r": "ר",  # Reish
    "sh": "ש", # Shin
    "sch": "ש", # Shin
    "ey": "ײ", # Double Yud
    "ei": "יי", # Double Yud
    "v": "װ",  # Vov-Yud
    "ai": "יַי", # Yud-Vov
    "ay": "ײַ", # Yud-Vov
}

# Update the table_lookup dictionary
table_lookup[('yid', 'en')] = YI_EN
table_lookup[('en', 'yid')] = EN_YI