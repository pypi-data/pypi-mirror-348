import re


# from .const import ORDINAL_INDICATOR_LIST, PREFIX_LIST, SUFFIX_LIST, BRACKETS_LIST


PREFIX_LIST = [
    "",
]

ORDINAL_INDICATOR_LIST = [
    ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十", "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八", "三十九", "四十", "四十一", "四十二", "四十三", "四十四", "四十五", "四十六", "四十七", "四十八", "四十九", "五十", "五十一", "五十二", "五十三", "五十四", "五十五", "五十六", "五十七", "五十八", "五十九", "六十", "六十一", "六十二", "六十三", "六十四", "六十五", "六十六", "六十七", "六十八", "六十九", "七十", "七十一", "七十二", "七十三", "七十四", "七十五", "七十六", "七十七", "七十八", "七十九", "八十", "八十一", "八十二", "八十三", "八十四", "八十五", "八十六", "八十七", "八十八", "八十九", "九十", "九十一", "九十二", "九十三", "九十四", "九十五", "九十六", "九十七", "九十八", "九十九", ...],
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", ...],
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ...],
    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ...],
    ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", ...],
    ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx", ...],
    ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "葵", ...],
    # ["第一章", "第二章", "第三章", "第四章", "第五章", "第六章", "第七章", "第八章", "第九章", "第十章", "第十一章", "第十二章", "第十三章", "第十四章", "第十五章", "第十六章", "第十七章", "第十八章", "第十九章", "第二十章", ...],
    # ["第一节", "第二节", "第三节", "第四节", "第五节", "第六节", "第七节", "第八节", "第九节", "第十节", "第十一节", "第十二节", "第十三节", "第十四节", "第十五节", "第十六节", "第十七节", "第十八节", "第十九节", "第二十节", ...],
]

SUFFIX_LIST = [
    ".",
    "、",
    ",",
    "，",
    ")",
    "）",
    "．",
    "",
]

BRACKETS_LIST = [
    ("(", ")"),
    ("（", "）"),
    ("[", "]"),
    ("第", "章"),
    ("第", "节"),
]

SPACE_CHARS = [            
    re.escape("\u3000"),    # \u3000 ideographic space
    re.escape("\u2003"),    # \u2003 em space
    re.escape("\xa0"),      # \u00a0 non-breaking space
]
REGEX_SPACE_CHARS = re.compile("[" + "".join(SPACE_CHARS) + "]")



PREFIX_REGEX = r"(?P<prefix>" + "|".join([re.escape(x) for x in PREFIX_LIST]) + r")"
SUFFIX_REGEX = r"(?P<suffix>" + "|".join([re.escape(x) for x in SUFFIX_LIST]) + r")"
ORDINAL_INDICATOR_REGEX = r"(?P<ordinal_indicator>" + "|".join([re.escape(x[0]) for x in ORDINAL_INDICATOR_LIST]) + r")"
PATTERN1 = r"^\s*" + PREFIX_REGEX + r"\s*" + ORDINAL_INDICATOR_REGEX + r"\s*" + SUFFIX_REGEX + r"\s*"

BRACKETS_REGEX_LIST = []

if __name__ == "__main__":
    s = " 1. "
    print(PATTERN1)
    pattern = re.compile(PATTERN1)
    result = pattern.search(s)
    assert result is not None
    print(result)
    prefix = result.group("prefix")
    suffix = result.group("suffix")
    ordinal_indicator = result.group("ordinal_indicator")
    print(prefix, ordinal_indicator, suffix)