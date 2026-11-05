"""영어 단어/표현 -> 미국식 발음기호(IPA). CMU 발음 사전 기반 + 수동 보정.

english-words-app/tools/ 와 bizwords-data/scripts/ 에 같은 파일이 있습니다(둘 다 고치세요).
"""
import re
import cmudict

D = cmudict.dict()

V = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "EH": "ɛ", "ER": "ɜr",
     "EY": "eɪ", "IH": "ɪ", "IY": "i", "OW": "oʊ", "OY": "ɔɪ", "UH": "ʊ", "UW": "u"}
C = {"B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "g", "HH": "h", "JH": "dʒ", "K": "k",
     "L": "l", "M": "m", "N": "n", "NG": "ŋ", "P": "p", "R": "r", "S": "s", "SH": "ʃ", "T": "t",
     "TH": "θ", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
ONSETS = {"pl", "pr", "bl", "br", "tr", "dr", "kl", "kr", "gl", "gr", "fl", "fr", "θr", "ʃr", "sp", "st",
          "sk", "sm", "sn", "sl", "sw", "tw", "kw", "dw", "pj", "bj", "kj", "fj", "mj", "vj", "hj",
          "spr", "str", "skr", "spl", "skw", "skj"}
# CMU 사전에 없거나 읽기가 특수한 것
OVERRIDE = {"atm": "ˌeɪtiˈɛm", "cc": "ˌsiˈsi", "linkedin": "ˈlɪŋktɪn",
            "diem": "ˈdiəm", "per": "pər", "ride-hailing": "ˈraɪd ˌheɪlɪŋ", "counteroffer": "ˈkaʊntərˌɔfər",
            "deal-breaker": "ˈdil ˌbreɪkər", "carry-on": "ˈkæri ˌɑn", "wake-up": "ˈweɪk ˌʌp",
            "check-in": "ˈtʃɛk ˌɪn", "medium-rare": "ˌmidiəm ˈrɛr", "round-trip": "ˌraʊnd ˈtrɪp",
            "one-way": "ˌwʌn ˈweɪ", "long-term": "ˌlɔŋ ˈtɜrm", "non-smoking": "ˌnɑn ˈsmoʊkɪŋ",
            "itemized": "ˈaɪtəˌmaɪzd", "a": "ə", "the": "ðə", "to": "tə", "of": "əv", "for": "fər",
            "and": "ənd", "at": "ət", "on": "ɑn", "in": "ɪn", "your": "jər", "as": "æz",
            "layover": "ˈleɪˌoʊvər", "housekeeping": "ˈhaʊsˌkipɪŋ", "checkout": "ˈtʃɛkˌaʊt",
            "overcharge": "ˌoʊvərˈtʃɑrdʒ", "rebook": "ˌriˈbʊk", "handout": "ˈhænˌdaʊt",
            "attendee": "əˌtɛnˈdi", "shortcut": "ˈʃɔrtˌkʌt", "reschedule": "ˌriˈskɛdʒul",
            "brainstorm": "ˈbreɪnˌstɔrm", "deadline": "ˈdɛdˌlaɪn", "feedback": "ˈfidˌbæk",
            "downtown": "ˌdaʊnˈtaʊn", "landmark": "ˈlændˌmɑrk", "overview": "ˈoʊvərˌvju",
            "souvenir": "ˌsuvəˈnɪr", "networking": "ˈnɛtˌwɜrkɪŋ", "headquarters": "ˈhɛdˌkwɔrtərz",
            "background": "ˈbækˌgraʊnd", "contactless": "ˈkɑnˌtæktləs", "cuisine": "kwɪˈzin",
            "itinerary": "aɪˈtɪnəˌrɛri", "excess": "ˈɛkˌsɛs", "upgrade": "ˌʌpˈgreɪd", "direct": "dəˈrɛkt",
            "directions": "dəˈrɛkʃənz", "arrival": "əˈraɪvəl", "overhead": "ˌoʊvərˈhɛd", "address": "ˈædrɛs",
            "vegetarian": "ˌvɛdʒəˈtɛriən", "restriction": "rɪˈstrɪkʃən", "elaborate": "ɪˈlæbəˌreɪt",
            "interrupt": "ˌɪntəˈrʌpt", "lead time": "ˈlid ˌtaɪm", "invite": "ɪnˈvaɪt", "include": "ɪnˈklud",
            "vat refund": "ˌviˌeɪˈti ˈriˌfʌnd", "insurance": "ɪnˈʃʊrəns", "sightseeing": "ˈsaɪtˌsiɪŋ",
            "schedule": "ˈskɛdʒul", "discount": "ˈdɪsˌkaʊnt", "updated": "ʌpˈdeɪtɪd", "passport": "ˈpæspɔrt",
            "refund": "ˈriˌfʌnd", "reminder": "rɪˈmaɪndər", "report": "rɪˈpɔrt",
            "waitlist": "ˈweɪtˌlɪst", "minibar": "ˈmɪniˌbɑr", "q&a": "ˌkjuənˈeɪ", "stomachache": "ˈstʌməkˌeɪk",
            "pin": "pɪn", "suite": "swit", "buffet": "bəˈfeɪ", "concierge": "ˌkɑnsiˈɛrʒ", "detour": "ˈdiˌtʊr",
            "e-ticket": "ˈiˌtɪkɪt", "overbooked": "ˌoʊvərˈbʊkt", "in-flight": "ˈɪnˌflaɪt", "duty-free": "ˌdutiˈfri",
            "red-eye": "ˈrɛd ˌaɪ", "gluten-free": "ˈglutən ˌfri", "non-alcoholic": "ˌnɑn ˌælkəˈhɔlɪk",
            "win-win": "ˌwɪn ˈwɪn", "double-booked": "ˌdʌbəl ˈbʊkt", "follow-up": "ˈfɑloʊ ˌʌp",
            "jet-lagged": "ˈdʒɛt ˌlægd", "upfront": "ˌʌpˈfrʌnt", "carpool": "ˈkɑrˌpul", "acknowledge": "əkˈnɑlɪdʒ",
            "outage": "ˈaʊtɪdʒ", "dear": "dɪr", "i'm": "aɪm", "i": "aɪ", "dutch": "dʌtʃ",
            "legroom": "ˈlɛgˌrum", "navigation": "ˌnævəˈgeɪʃən", "subject": "ˈsʌbdʒɪkt", "inquiry": "ˈɪnkwəri",
            "accept": "əkˈsɛpt", "excuse": "ɪkˈskjuz", "ingredient": "ɪnˈgridiənt", "impressive": "ɪmˈprɛsɪv",
            "installment": "ɪnˈstɔlmənt", "hospital": "ˈhɑspɪtəl", "headache": "ˈhɛdˌeɪk", "company": "ˈkʌmpəni",
            "halfway": "ˈhæfˌweɪ", "stopover": "ˈstɑpˌoʊvər", "leftovers": "ˈlɛftˌoʊvərz", "our": "aʊər",
            "per diem": "pər ˈdiəm"}


def syllabify(phones):
    out = []  # list of IPA segments with stress marks inserted
    segs = []
    for p in phones:
        m = re.match(r"([A-Z]+)(\d)?", p)
        base, st = m.group(1), m.group(2)
        if base in V:
            ipa = V[base]
            if st == "0":
                ipa = {"ʌ": "ə", "ɜr": "ər"}.get(ipa, ipa)
            segs.append(("V", ipa, st))
        else:
            segs.append(("C", C[base], None))
    nvow = sum(1 for s in segs if s[0] == "V")
    for i, (kind, ipa, st) in enumerate(segs):
        if kind == "V" and st in ("1", "2") and nvow > 1:
            # 앞쪽 자음 중 합법적인 음절 첫소리만큼 강세 기호 앞으로 이동
            j = len(out)
            k = i - 1
            onset = ""
            while k >= 0 and segs[k][0] == "C":
                cand = segs[k][1] + onset
                if len(onset) == 0 or cand in ONSETS:
                    onset = cand
                    k -= 1
                else:
                    break
            n = i - 1 - k  # 이동할 자음 개수
            pos = len(out) - n
            # 단어 첫머리에 다른 음절이 앞에 없으면 그대로 둬도 OK
            out.insert(pos, "ˈ" if st == "1" else "ˌ")
        out.append(ipa)
    return "".join(out)


def word_ipa(w):
    lw = w.lower()
    if lw in OVERRIDE:
        return OVERRIDE[lw]
    if lw in D:
        return syllabify(D[lw][0])
    if "-" in lw:
        return " ".join(word_ipa(x) for x in lw.split("-"))
    raise KeyError(w)


def phrase_ipa(phrase):
    """발음기호를 못 만들면 KeyError"""
    lp = phrase.lower()
    if lp in OVERRIDE:
        return OVERRIDE[lp]
    return " ".join(word_ipa(t) for t in lp.split())


