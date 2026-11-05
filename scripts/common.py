"""words.json / queue.json 공통 처리 (검사, 발음기호, 저장)."""
import json
import re
from pathlib import Path

from ipa import phrase_ipa

ROOT = Path(__file__).resolve().parent.parent
WORDS = ROOT / "words.json"   # 앱이 받아가는 공개 단어 목록 (순서·id 절대 변경 금지)
QUEUE = ROOT / "queue.json"   # 아직 공개 안 한 대기 단어 (매주 50개씩 words.json 으로 이동)

POS = {"n.", "v.", "adj.", "adv.", "prep.", "phr.", "interj."}
FIELDS = ("c", "w", "p", "m", "e", "k", "h")


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")


def categories(words):
    return list(dict.fromkeys(w["c"] for w in words))


def clean(entry, cats, taken):
    """형식이 맞으면 정리된 항목, 아니면 (None, 이유)"""
    e = {k: str(entry.get(k, "")).strip() for k in FIELDS + ("ipa",)}
    w = e["w"]
    if not w or len(w) > 40 or not re.fullmatch(r"[A-Za-z][A-Za-z '&\-]*", w):
        return None, "단어 형식"
    if w.lower() in taken:
        return None, "중복"
    if e["c"] not in cats:
        return None, f"분류 '{e['c']}' 없음"
    if e["p"] not in POS:
        return None, f"품사 '{e['p']}'"
    if not all(e[k] for k in ("m", "e", "k", "h")):
        return None, "빈 칸"
    if len(e["e"]) > 160:
        return None, "예문이 너무 김"
    if not re.search(r"[가-힣]", e["h"]) or not re.search(r"[가-힣]", e["m"]) or not re.search(r"[가-힣]", e["k"]):
        return None, "한글 뜻/해석/발음 없음"
    try:
        ipa = phrase_ipa(w)
    except KeyError:
        ipa = e["ipa"].strip("/ ")
    if not ipa:
        return None, "발음기호 없음 (ipa 칸을 채워 주세요)"
    return {"c": e["c"], "w": w, "ipa": f"/{ipa}/", "h": e["h"], "p": e["p"],
            "m": e["m"], "e": e["e"], "k": e["k"]}, None
