# winnext

WIN NEXT 2026 회장 운영 웹페이지. GitHub Pages: https://sollar99-dotcom.github.io/winnext/

## 페이지

| 주소 | 내용 |
|---|---|
| `/` | 정기모임 아카이브: 다음 모임 카드 + 월별 모임 목록 (발표자료·카페 후기 링크) |
| `/YYYY-MM/` | 그달 정기모임 회장 발표자료 (예: `/2026-11/`) |
| `/checklist/` | 정기모임 체크리스트 (Before · After, 완료/미완료) |

아카이브와 체크리스트 위에는 같은 메뉴가 붙어 있다. 발표자료는 화면 전체를 쓰므로 메뉴를 넣지 않는다.

## 폴더

```
index.html        아카이브 (tools/build_index.py가 만듦)
YYYY-MM/          월별 발표자료
checklist/        체크리스트 (tools/build_checklist.py가 만듦)
_data/            아카이브 데이터 (meetings.json)
tools/            페이지를 만드는 스크립트
```

## 갱신

**새 달 발표자료**
1. OneDrive 완성본을 `YYYY-MM/index.html`로 복사한다.
2. `_data/meetings.json` 그 모임에 `"deck": "YYYY-MM/"`를 넣는다. 카페 후기가 올라오면 `"cafe": [글번호]`.
3. `python3 tools/build_index.py` → 커밋 → 푸시.

**체크리스트**
- 정본은 옵시디언 `WINNEXT 7기/회장비서/정기모임 체크리스트.md`.
- `python3 tools/build_checklist.py` → 커밋 → 푸시.

## 올리지 않는 것
회원 명단·연락처·주소, 설문 응답, 시트 ID, 로그인 정보.
