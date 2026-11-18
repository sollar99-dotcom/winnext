# winnext-site
WIN NEXT 정기모임 회장 발표자료 (웹). 월별 폴더: `YYYY-MM/index.html`

## 아카이브 갱신
1. 새 달 발표자료를 `YYYY-MM/index.html`로 넣는다 (회원 사진 제외본).
2. `_data/meetings.json` 해당 모임에 `"deck": "YYYY-MM/"`, 후기가 올라오면 `"cafe": [글번호]`를 넣는다.
3. `python3 tools/build_index.py` → 커밋 → 푸시.
