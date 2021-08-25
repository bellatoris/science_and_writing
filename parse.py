import sys
from itertools import permutations

FIRST_HANJA_UNICODE = 0x4E00
LAST_HANJA_UNICODE = 0x9FFF

FIRST_HANJA_EXT_A_UNICODE = 0x3400
LAST_HANJA_EXT_A_UNICODE = 0x4DBF

FIRST_LATIN1_UNICODE = 0x0000  # NUL
LAST_LATIN1_UNICODE = 0x00FF  # 'ÿ'

CHO = (
    u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)

JOONG = (
    u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ',
    u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ', u'ㅣ'
)

JONG = (
    u'', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ',
    u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)

JAMO = CHO + JOONG + JONG[1:]

NUM_CHO = 19
NUM_JOONG = 21
NUM_JONG = 28

FIRST_HANGUL_UNICODE = 0xAC00  # '가'
LAST_HANGUL_UNICODE = 0xD7A3  # '힣'
#                      AB C DEFGHIJK L M N OPQR ST UVWXYZ
ENG_KOR_SUBSTITUENT = {'B': 'ㅂ', 'C': 'ㄱ', 'K': 'ㄱ',
                       'L': 'ㄹ', 'M': 'ㅁ', 'N': 'ㄴ', 'R': 'ㄹ', 'T': 'ㅅ'}


def is_hangul(phrase):
    for letter in phrase:
        code = ord(letter)
        if (code < FIRST_HANGUL_UNICODE or code > LAST_HANGUL_UNICODE) and not is_jamo(letter):
            return False

    return True


def is_jamo(letter):
    return letter in JAMO


def is_latin1(phrase):
    for unicode_value in map(lambda letter: ord(letter), phrase):
        if unicode_value < FIRST_LATIN1_UNICODE or unicode_value > LAST_LATIN1_UNICODE:
            return False
    return True


def hangul_index(letter):
    return ord(letter) - FIRST_HANGUL_UNICODE


def decompose_index(code):
    jong = int(code % NUM_JONG)
    code /= NUM_JONG
    joong = int(code % NUM_JOONG)
    code /= NUM_JOONG
    cho = int(code)

    return cho, joong, jong


def decompose(hangul_letter):
    """This function returns letters by decomposing the specified Hangul letter."""

    if not is_hangul(hangul_letter):
        return ''

    if hangul_letter in CHO:
        return hangul_letter, '', ''

    if hangul_letter in JOONG:
        return '', hangul_letter, ''

    if hangul_letter in JONG:
        return '', '', hangul_letter

    code = hangul_index(hangul_letter)
    cho, joong, jong = decompose_index(code)

    if cho < 0:
        cho = 0

    try:
        return CHO[cho], JOONG[joong], JONG[jong]
    except:
        print("%d / %d  / %d" % (cho, joong, jong))
        print("%s / %s " %
              (JOONG[joong].encode("utf8"), JONG[jong].encode('utf8')))
        return ''


def decompose_text(text, latin_filter=True, compose_code=u''):
    result = u""

    for c in list(text):
        if is_hangul(c):

            if is_jamo(c):
                result = result + c + compose_code
            else:
                result = result + "".join(decompose(c)) + compose_code

        else:
            if latin_filter:    # 한글 외엔 Latin1 범위까지만 포함 (한글+영어)
                if is_latin1(c):
                    result = result + c
            else:
                result = result + c

    return result


# while True:
#     for line in sys.stdin.readlines():
#         abbrev, origin = line.rstrip().split('\t')
#         typing_efficiency = float(
#             len(decompose_text(origin))) / len(decompose_text(abbrev))
#         origin = origin.replace(' ', '')
#         syllable_efficiency = float(len(origin)) / len(abbrev)

#         print('{0:0.2f}\t{1:0.2f}'.format(syllable_efficiency, typing_efficiency))

chos = []
joongs = []
jongs = []
for c in list("글롬자이"):
    cho, joong, jong = decompose(c)
    chos.append(cho)
    joongs.append(joong)
    jongs.append(jong)

permuted_chos = list(permutations(chos))
permuted_joongs = list(permutations(joongs))
permuted_jongs = list(permutations(jongs))

for chos in permuted_chos:
    for joongs in permuted_joongs:
        for jongs in permuted_jongs:
            print("{0}{1}{2} {3}{4}{5} {6}{7}{8} {9}{10}{11}".format(
                chos[0],
                joongs[0],
                jongs[0],
                chos[1],
                joongs[1],
                jongs[1],
                chos[2],
                joongs[2],
                jongs[2],
                chos[3],
                joongs[3],
                jongs[3]
            ))
