"""queue.json 앞에서 단어를 꺼내 words.json 끝에 '새 단계'로 공개합니다. (AI·API 키 필요 없음)

환경 변수: RELEASE_COUNT (기본 50)
"""
import os

from common import QUEUE, WORDS, categories, clean, load, save

COUNT = int(os.environ.get("RELEASE_COUNT") or 50)


def main():
    words, queue = load(WORDS), load(QUEUE)
    if not queue:
        print("대기열이 비어 있어 이번 주는 공개할 단어가 없습니다.")
        return
    cats = categories(words)
    taken = {x["w"].lower() for x in words}
    level = max(x.get("lv", 1) for x in words) + 1
    released, rest = [], list(queue)
    while rest and len(released) < COUNT:
        item, why = clean(rest.pop(0), cats, taken)
        if item is None:
            continue
        taken.add(item["w"].lower())
        released.append({"id": len(words) + len(released), "lv": level, **item})
    if not released:
        save(QUEUE, rest)
        print("공개할 수 있는 단어가 없었습니다.")
        return
    words.extend(released)
    save(WORDS, words)
    save(QUEUE, rest)
    print(f"{level}단계 새 단어 {len(released)}개 공개 (전체 {len(words)}개, 남은 대기 {len(rest)}개)")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"level={level}\ncount={len(released)}\nleft={len(rest)}\n")


if __name__ == "__main__":
    main()
