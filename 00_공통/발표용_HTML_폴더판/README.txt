건설소재 역설계 도구 개발을 위한 AI와 분자동역학 활용 — 발표용 강의 덱 (17개, 2026-09-22)

[여는 방법]
덱은 브라우저에서 로컬 웹 서버로 열어야 합니다. 파일을 더블클릭(file://)하면 슬라이드 런타임이 동작하지 않습니다.

  Windows : 「열기_Windows.bat」 더블클릭
  macOS / Linux : 터미널에서 이 폴더로 이동 후  sh 열기_mac_linux.sh
  직접 실행 : 이 폴더에서  python3 -m http.server 8765  →  브라우저에서 http://localhost:8765/

첫 화면(index.html)에서 주차별 덱을 고릅니다.
덱 안에서 ← → 슬라이드 이동, Home / End 처음 · 끝, 「라이브」 슬라이드는 버튼으로 조작합니다.

[필요 조건]
- Python 3 (로컬 서버용)
- 인터넷 연결 : React 런타임(unpkg.com)과 글꼴(jsdelivr · Google Fonts)을 온라인에서 받습니다.

[구성]
  index.html        주차별 목록 (표지 썸네일 · 강의계획서 차시 · 슬라이드 수)
  발표용/            발표용 덱 17개 (.dc.html)
  assets/ · uploads/ 슬라이드 그림
  _ds/              NACMID 디자인 시스템 (색 · 글꼴 토큰)
  support.js · deck-stage.js   슬라이드 런타임

발표용 버전은 보존용 부록(이전 구성 원문)을 뺀 것입니다. 원본 덱과 수정 이력은 강의자료 저장소(git)에 있습니다.
HTML판은 두 파트(_HTML_1of2 · _HTML_2of2)로 나뉘어 있습니다. 두 파일을 같은 곳에 풀면 한 폴더로 합쳐집니다(둘 다 필요).
PDF 판은 별도 압축 파일(…_PDF_1 · 2 · 3)에 있습니다.
