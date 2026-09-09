# accouting-work — Claude 작업 가이드

## 앱 구조
단일 파일 모바일 웹앱 (`index.html`), 바닐라 JS, 다크테마. Netlify 배포 (main 브랜치 push → 자동 배포).

**탭 3개**:
1. **전표입력** — SAP 전표 양식 (DEFAULT_FORMS 기반)
2. **전표요약** — 매월 반복 전표 체크리스트 (SUMMARY 기반)
3. **숙소현황** — 직원 숙소 정보

---

## 핵심 데이터 구조

### SUMMARY (line ~308)
전표요약 탭. 86개 항목, 매월 반복 처리 전표 목록.
```js
{ord:1, date:"처리시기", name:"항목명", img:"파일명.png", 적요:"전표적요", pjt:"BBW1002", acct:"계정설명", chk:"정산|비정산|-"}
```
- `img`: `/images/` 폴더 기준 파일명 (SUMMARY_BASE = GitHub Pages URL)
- `chk`: "정산" = 초록, "비정산" = 빨강, 그 외 = 회색

### DEFAULT_FORMS (line ~777)
전표입력 탭 양식 템플릿. 57개 항목.
```js
{type:'tax|normal|jiro|silmool|chaekwon|kita', kita:'arap|jeondo|gl', title:'표시명', _default:true, fields:{...}}
```
- `f-dept`: 현장코드 (BBW1002=구미, BBW1003=구미증설, BBW1004=김천)
- `f-bikmok`: 계약비목 — CC_BIKMOK 룩업 후 select로 표시됨

### CC_BIKMOK (line ~730)
계약비목 드롭다운 옵션. CC코드별로 다름.

---

## 이미지 관리

### 파일 위치
- 로컬: `/home/user/accouting-work/images/`
- 배포: `https://dudwnddl79-bot.github.io/accouting-work/images/`

### 네이밍 규칙
`{업무종류}_{현장}_{월}.{ext}`
- 현장: gumi(구미), up(증설/BBW1003), gimcheon(김천)
- 월: jul(7월), aug(8월), sep(9월) ...
- 예: `sikdae_gumi_aug.png`, `utility_pesu_jul.png`

### ZIP 파일 처리
사용자가 제공하는 zip에 #U 인코딩 한글 파일명이 들어있음.
```python
# 디코딩: #U4F4D → chr(0x4F4D) = '位'
re.sub(r'#U([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1),16)), encoded_name)
```

**→ `scripts/update_images.py` 사용** (아래 참고)

---

## 반복 작업 절차

### 1. 새 ZIP 이미지 반영
```bash
# zip을 scratchpad에 압축 해제 후:
python3 scripts/update_images.py --zipdir /tmp/.../zipcontents --mapping scripts/image_mapping.json
```

### 2. SUMMARY 이미지 업데이트
SUMMARY의 `img` 필드를 새 파일명으로 교체 (Python으로 직접 치환).

### 3. DEFAULT_FORMS 추가/수정
전표 이미지를 보고 필드값 추출. f-bikmok은 fOnCC 호출 이후에 재설정 필요 (버그 수정 이미 반영됨).

### 4. 커밋/푸시/머지
```bash
git add index.html images/
git commit -m "메시지\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin claude/remove-names-images-e3h4yn
# PR 생성 → merge (MCP github 툴 사용)
# 충돌 시: git fetch origin main && git rebase origin/main && git push --force-with-lease
```

---

## 현장 코드
| 코드 | 현장 |
|------|------|
| BBW1002 | 구미 코오롱 폐수 |
| BBW1003 | 구미 증설 |
| BBW1004 | 김천 코오롱 폐수 |

## 주요 공급업체
- 코오롱인더스트리(주) 구미공장 — 위탁운영비(구미)
- 코오롱인더스트리(주) 김천공장 — 위탁운영비(김천 1공장)
- 코오롱인더스트리(주) 김천3공장 — 위탁운영비(김천 3공장)
- (주)서브원 — 안전장비
- 코오롱글로벌(주)FS김천1점 — 카페 식대

## 중요 규칙 (사용자 지시)
- **반드시 존댓말 사용**
- **매 수정 후 동작 검증 필수**
- **결재서류 이미지 속 개인 이름 제거 (HTML 텍스트는 수정 금지)**
- 개발 브랜치: `claude/remove-names-images-e3h4yn`
