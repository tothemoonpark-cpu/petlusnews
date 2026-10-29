펫러스뉴스 자동 게재 장치 (2026-10-29 설치)
- 매일 한국 00:05(재시도 02:35·06:05) GitHub Actions 「펫러스뉴스 자동 게재」가 _src/publish.py 를 실행한다.
- 기사 올리는 법: 검수가 끝난 기사 md 를 _queue/ 에 넣는다. 머리말에 반드시
    publish_date: YYYY-MM-DD   (게재할 날짜)
    reviewed: yes              (퍼플렉시티 → Claude 사실 검수 통과 표시)
    review_note: 검수 근거 한 줄 이상
    sources: 출처 (본문 sources 와 같은 형식)
    note: (선택) 「박근필 수의사의 한 줄」 상자 — 있을 때만 표시
  reviewed 가 yes 가 아니거나 review_note·sources 가 없으면 기계가 올리지 않고 실패로 끝낸다.
- 오늘 날짜 기사가 없으면 실패(누락 알림). 실행이 실패하면 저장소 Actions 탭에 빨간 표시와 GitHub 알림 메일이 간다.
- 올린 뒤 라이브 feed.xml 에 오늘 날짜가 보이는지 스스로 검사한다(15분).
- _src/·_queue/ 는 사이트로 공개되지 않는다(언더스코어 폴더). 게재된 기사는 _src/articles/ 로 옮겨진다.
- 네이버 서치어드바이저 수집 요청은 로그인이 필요해 어사이드가 한다.
