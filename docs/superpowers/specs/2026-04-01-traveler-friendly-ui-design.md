# 운남 여행 일정표 — 여행자 친화적 UI 개선 스펙

**날짜:** 2026-04-01  
**파일:** `index.html` (단일 파일 프로젝트)

---

## 배경

현재 일정표에는 기화계(汽锅鸡), 미선(米线) 등 처음 보는 여행자에겐 낯선 음식·장소 이름이 한자 병기만으로 적혀 있어 직관적이지 않다. 전체 UI도 정보 밀도가 높아 "오늘 뭘 하고 얼마 쓰지?"를 빠르게 파악하기 어렵다.

---

## 확정된 개선 항목 (5가지)

### 1. Day 카드 상단 요약 스트립 (신규)

각 `article.day` 카드의 `.day-head`와 `.grid` 사이에 `.day-summary` 요소를 삽입한다.

**구조:**
```html
<div class="day-summary">
  <span class="summary-chip chip-budget">💰 예산 약 130–200위안</span>
  <span class="summary-chip chip-weather">⛅ 해발 1,890m · 낮 22–26°C · 자외선 강함</span>
  <span class="summary-chip chip-place">🏞 다관공원 · 디엔치 호수</span>
  <span class="summary-chip chip-food">🍜 윈난 쌀국수 · 가정식</span>
</div>
```

**스타일:**
- 배경: `var(--color-surface-2)` (`#f8f9fa`)
- 패딩: `12px 24px`
- 하단 경계선: `1px solid var(--color-border-light)`
- 칩은 색상으로 구분: 예산(초록), 날씨(노랑), 장소(보라), 식사(파랑)
- 모바일에서 `flex-wrap: wrap`으로 줄바꿈

**8일치 내용 (사실 기반):**

| Day | 예산 | 날씨/해발 | 주요 장소 | 주요 식사 |
|-----|------|-----------|-----------|-----------|
| 1 (쿤밍 도착) | 130–200위안 | 해발 1,890m · 낮 22–26°C · 자외선 강함 | 다관공원 · 디엔치 호수 | 윈난 쌀국수 · 가정식 |
| 2 (석림) | 200–280위안 | 해발 1,750m · 낮 24–28°C · 햇빛 강함 | 석림풍경구 | 현지 간이식 · 기화계 |
| 3 (쿤밍→샤시) | 100–150위안 | 열차 이동일 · 샤시 해발 2,040m | 샤시고진 · 사등가 · 옥진교 | 간단 조식 · 샤시 현지식 |
| 4 (샤시고진) | 120–180위안 | 해발 2,040m · 낮 20–25°C · 선선함 | 사등가 · 흥교사 · 옥진교 | 샤시 미선 · 바이족 요리 |
| 5 (샤시→리장) | 150–220위안 | 리장 해발 2,400m · 낮 18–24°C | 리장 고성 · 사방가 | 리장 현지식 |
| 6 (옥룡설산·인상여강) | 500–700위안 | 해발 4,506m 빙하 · 방한복 필수 | 옥룡설산 · 남니설산 · 남교 | 현지 간단식 |
| 7 (리장 탐방) | 150–250위안 | 해발 2,400m · 낮 20–25°C | 수허고진 · 문해 · 백사고진 | 리장 바바 · 동파 요리 |
| 8 (리장→쿤밍 귀국) | 100–150위안 | 이동일 | 취호 | 쿤밍 도시락 or 공항식 |

---

### 2. 음식 설명 태그 (신규)

**방식:** 음식 이름 바로 다음 줄에 `<span class="desc-tag food">` 항상 표시. 호버 불필요.

**한자 처리:**
- 본문 텍스트에서 한자 인라인 병기 제거
- 대신 기존 `.han-copy-btn` 패턴의 클립보드 버튼을 음식명 옆에 추가
- 버튼 클릭 시 한자가 클립보드에 복사됨 (검색·내비 활용)

**예시:**
```html
기화계
<button class="han-copy-btn" data-han="汽锅鸡" aria-label="한자 복사">
  <span class="material-symbols-rounded" style="font-size:14px">content_copy</span>
</button>
<span class="desc-tag food">🍲 증기압으로 쪄낸 통닭 국물 요리 · 맑고 깊은 맛 · 윈난 대표 보양식</span>
```

**음식별 사실 기반 설명 목록:**

| 음식명 | 한자 | 설명 태그 |
|--------|------|-----------|
| 미선 | 米线 | 🍜 쌀로 만든 윈난식 쌀국수 · 국물·비빔 선택 가능 · 아침 대표 간식 |
| 기화계 | 汽锅鸡 | 🍲 증기압으로 쪄낸 통닭 국물 요리 · 맑고 깊은 맛 · 윈난 대표 보양식 |
| 과교미선 | 过桥米线 | 🍜 뜨거운 기름 국물에 재료를 직접 익혀 먹는 윈난 대표 쌀국수 |
| 리장 바바 | 丽江粑粑 | 🥐 밀가루 반죽을 납작하게 구운 리장 전통 빵 · 짠맛·단맛 선택 |
| 동파 요리 | 东巴菜 | 🍽 나시족 전통 요리 · 리장 고성 특산 · 훈제·발효 식재료 활용 |
| 바이족 요리 | 白族菜 | 🥘 바이족 전통 음식 · 샤시·따리 지역 특산 · 시큼하고 매콤한 맛 |
| 윈난 가정식 | 云南家常菜 | 🥗 버섯·야채 볶음 위주의 윈난 가정 요리 · 담백하고 신선한 맛 |
| 사방소초 | 四方小炒 | 🥘 윈난식 볶음요리 전문 · 다양한 채소·고기 볶음 · 1인 40–60위안 |

---

### 3. 장소 설명 태그 (신규)

음식과 동일한 `desc-tag` 패턴, 색상만 보라색(`chip-place` 스타일).

- `.place` 클래스 (모달 오픈): 설명 태그 추가, 모달 동작 유지
- `.place-popover` 클래스 (지도 툴팁): 설명 태그 추가, 팝오버 동작 유지

**장소별 사실 기반 설명 목록:**

| 장소명 | 한자 | 설명 태그 |
|--------|------|-----------|
| 다관공원 | 大观公园 | 🏞 디엔치 호수 조망 명소 · 다관루 3층 전망 · 연꽃 정원 · 입장 무료 |
| 디엔치 호수 | 滇池 | 🌅 쿤밍 최대 호수(298㎢) · 호수변 산책로 · 석양 명소 · 전기자전거 대여 가능 |
| 석림풍경구 | 石林风景区 | 🗿 2억 7천만 년 된 석회암 기둥 숲 · 유네스코 세계자연유산 |
| 샤시고진 | 沙溪古镇 | 🏘 당·송 시대 차마고도 교역 마을 · 대부분 옛 건물 보존 · 조용하고 아늑함 |
| 사등가 | 四方街 | 🎭 샤시 중심 광장 · 고희대(옛 무대) · 장날 바이족 문화 체험 |
| 옥진교 | 玉津桥 | 🌉 샤시 마을 입구 옛 돌다리 · 석양 사진 포인트 · 흑혜강 위치 |
| 흥교사 | 兴教寺 | 🛕 명나라 시대 불교 사찰 · 샤시고진 내 · 벽화 보존 |
| 리장 고성 | 丽江古城 | 🏘 나시족 800년 전통 고성 · 유네스코 세계문화유산 · 입장 유료 |
| 옥룡설산 | 玉龙雪山 | 🏔 해발 5,596m · 리장 대표 랜드마크 · 빙하 트레킹 · 방한복 필수 |
| 수허고진 | 束河古镇 | 🏘 리장 인근 조용한 나시족 마을 · 고성보다 한적 · 도보 30분 거리 |
| 백사고진 | 白沙古镇 | 🎨 나시족 벽화로 유명한 작은 마을 · 고성 북쪽 · 도교·불교·라마교 혼합 |
| 문해 | 文海 | 🌊 리장 북서쪽 고산 호수 · 해발 3,100m · 철새 도래지 · 비포장 도로 |
| 취호 | 翠湖 | 🦢 쿤밍 도심 속 호수 공원 · 겨울 갈매기 · 윈난대학 인근 |

---

### 4. 한자 표기 정책

**Before:** `다관공원(大观公园)`, `기화계(汽锅鸡)` — 본문 인라인 병기  
**After:** `다관공원` + 클립보드 버튼(한자 복사) + 설명 태그

- 기존 `.han-copy-btn` CSS·JS 로직 재사용
- `data-han` 속성에 한자 저장, 클릭 시 복사
- 장소 모달 헤더(`place-modal-head h2`)는 "장소명 (한자)" 형식 유지 가능 — 모달은 상세 정보 공간이므로

---

### 5. 실용 팁 강화

기존 `.tip` 박스 유지. 요약 스트립의 날씨 칩이 첫 번째 실용 정보 계층 역할을 함. 고도 적응, 방한복 등 중요 경고는 `.tip` 박스에 계속 명시.

---

## 변경하지 않는 것

- `.place` 클래스의 사진 모달 동작
- `.place-popover` 클래스의 지도·검색 툴팁 팝오버 동작
- 전체 레이아웃 (`.grid`, `.day`, `.card` 구조)
- 다크 모드 토글
- 모바일 사이드바
- 열차 시간표, 체크리스트, 필독사항, 블로그 링크 섹션

---

## CSS 추가 사항

```css
/* 요약 스트립 */
.day-summary {
  display: flex; flex-wrap: wrap; gap: 8px;
  padding: 12px var(--space-6);
  background: var(--color-surface-2);
  border-bottom: 1px solid var(--color-border-light);
}
.summary-chip {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: var(--radius-full);
  font-size: var(--text-xs); font-weight: 500;
}
.chip-budget  { background: #e6f4ea; color: #137333; }
.chip-weather { background: #fef7e0; color: #7a4f00; }
.chip-place   { background: #f3e8fd; color: #6a1b9a; }
.chip-food    { background: #e8f0fe; color: #1557b0; }
[data-theme="dark"] .chip-budget  { background: #1e3a2a; color: #81c995; }
[data-theme="dark"] .chip-weather { background: #3c3520; color: #e8d5a0; }
[data-theme="dark"] .chip-place   { background: #2e1f3e; color: #c58af9; }
[data-theme="dark"] .chip-food    { background: #1e2d4a; color: #8ab4f8; }

/* 설명 태그 */
.desc-tag {
  display: inline-block; margin-top: 3px;
  font-size: var(--text-xs);
  padding: 2px 8px; border-radius: 4px;
  line-height: 1.5;
}
.desc-tag.food  { background: var(--color-primary-container); color: var(--color-primary-on-container); }
.desc-tag.place { background: #f3e8fd; color: #6a1b9a; }
[data-theme="dark"] .desc-tag.food  { background: #1e2d4a; color: #8ab4f8; }
[data-theme="dark"] .desc-tag.place { background: #2e1f3e; color: #c58af9; }
```
