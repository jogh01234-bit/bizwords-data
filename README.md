# 출장 영단어 데이터

'출장 영단어' 안드로이드 앱이 하루 두 번쯤 이 저장소의 `words.json` 을 받아 새 단어를 추가합니다.

| 파일 | 역할 |
|---|---|
| `words.json` | 앱이 받아가는 공개 단어. **기존 항목의 순서·id 는 바꾸거나 지우지 마세요**(학습 기록이 번호로 저장됨). 뜻·예문 오타 수정은 OK |
| `queue.json` | 아직 공개 안 한 대기 단어 |
| `.github/workflows/weekly-release.yml` | 매주 월요일 오전 9시쯤 대기열에서 50개를 꺼내 다음 단계로 공개 (무료, API 키 불필요) |
| `scripts/add_to_queue.py` | 새 단어 후보를 검사해 대기열에 추가 (중복·형식 검사, 발음기호 자동 계산). 항목: c 분류, w 단어, p 품사, m 뜻, n 뜻 설명, e 예문, k 해석, h 한글 발음 |

대기열은 Claude Code 예약 작업(루틴)이 매주 자동으로 보충합니다.

```bash
pip install cmudict
python scripts/add_to_queue.py candidates.json   # 후보 추가
python scripts/release_weekly.py                 # (보통은 Actions 가 실행)
```
