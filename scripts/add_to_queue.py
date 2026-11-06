"""새 단어 후보(JSON 배열 파일)를 검사해서 queue.json 뒤에 추가합니다.

사용법: python scripts/add_to_queue.py candidates.json
후보 항목 형식: {"c": 분류, "w": 단어, "p": 품사, "m": 뜻(여러 뜻은 ; 로 구분), "n": 뜻 설명(쓰임·비슷한 말), "e": 영어 예문, "k": 예문 해석, "h": 한글 발음, "ipa": (선택) IPA}
- 분류는 words.json 에 있는 10개 중 하나, 품사는 n. v. adj. adv. prep. phr. interj.
- words.json·queue.json 에 이미 있는 단어는 버림. 발음기호는 CMU 사전으로 자동 계산(없으면 ipa 칸 사용)
"""
import json
import sys

from common import QUEUE, WORDS, categories, clean, load, save


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cands = json.loads(open(sys.argv[1], encoding="utf-8").read())
    if isinstance(cands, dict):
        cands = cands.get("words", [])
    words, queue = load(WORDS), load(QUEUE)
    cats = categories(words)
    taken = {x["w"].lower() for x in words + queue}
    added, dropped = [], []
    for c in cands:
        item, why = clean(c, cats, taken)
        if item is None:
            dropped.append(f"{c.get('w')!r}: {why}")
            continue
        taken.add(item["w"].lower())
        added.append(item)
    queue.extend(added)
    save(QUEUE, queue)
    print(f"대기열에 {len(added)}개 추가 → 대기 {len(queue)}개 (공개 {len(words)}개)")
    for d in dropped:
        print("  버림", d)


if __name__ == "__main__":
    main()
