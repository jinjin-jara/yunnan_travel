# 운남 여행자 친화적 UI 개선 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `index.html` 단일 파일에 ① Day 카드 상단 요약 스트립, ② 음식·장소 설명 태그, ③ 한자 보조 처리(기존 JS 활용)를 추가해 여행자 친화적 UI로 개선한다.

**Architecture:** 모든 변경은 `index.html` 하나에서 이루어진다. CSS는 `<style>` 블록(약 1147번째 줄 근처)에 추가하고, 각 Day 카드에 `.day-summary` 스트립과 `.desc-tag` 요소를 삽입한다. 한자 클립보드 버튼은 기존 `initPlaceHanCopyButtons()` JS가 `.place`·`.place-popover` 텍스트를 자동 처리하므로 별도 JS 수정 불필요.

**Tech Stack:** HTML, CSS (CSS custom properties 활용), 기존 Vanilla JS (변경 없음)

---

## 핵심 전제: 기존 JS 동작 이해

`initPlaceHanCopyButtons()` (약 3979번째 줄)는 페이지 로드 시:
1. 모든 `.place`, `.place-popover` 요소의 텍스트를 읽음
2. `이름(한자)` 패턴이면 한자를 추출해 `data-placeTitle`에 저장
3. 요소 텍스트를 `이름 [클립보드버튼]` 으로 교체

→ **`.place`·`.place-popover` 텍스트의 한자 처리는 이미 자동화됨. HTML 변경 불필요.**

`.desc-tag`는 반드시 `.place`·`.place-popover` 스팬 **바깥(형제 노드)**에 위치해야 함. 스팬 안에 넣으면 JS 텍스트 파싱이 깨짐.

---

## Task 1: CSS 추가

**Files:**
- Modify: `index.html` — `</style>` 직전 (약 1147번째 줄)

- [ ] **Step 1: `</style>` 직전에 아래 CSS 블록 삽입**

```css
      /* ─── Day summary strip ─── */
      .day-summary {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        padding: 12px var(--space-6);
        background: var(--color-surface-2);
        border-bottom: 1px solid var(--color-border-light);
      }
      .summary-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: var(--radius-full);
        font-size: var(--text-xs);
        font-weight: 500;
        line-height: 1.4;
      }
      .chip-budget  { background: #e6f4ea; color: #137333; }
      .chip-weather { background: #fef7e0; color: #7a4f00; }
      .chip-place   { background: #f3e8fd; color: #6a1b9a; }
      .chip-food    { background: #e8f0fe; color: #1557b0; }
      [data-theme="dark"] .chip-budget  { background: #1b3a2a; color: #81c995; }
      [data-theme="dark"] .chip-weather { background: #3c3520; color: #e8d5a0; }
      [data-theme="dark"] .chip-place   { background: #2e1f3e; color: #c58af9; }
      [data-theme="dark"] .chip-food    { background: #1a2d4a; color: #8ab4f8; }

      /* ─── Description tags ─── */
      .desc-tag {
        display: inline-block;
        margin-top: 3px;
        font-size: var(--text-xs);
        padding: 2px 8px;
        border-radius: 4px;
        line-height: 1.5;
        font-weight: 400;
      }
      .desc-tag.food {
        background: var(--color-primary-container);
        color: var(--color-primary-on-container);
      }
      .desc-tag.place {
        background: #f3e8fd;
        color: #6a1b9a;
      }
      [data-theme="dark"] .desc-tag.food {
        background: #1a2d4a;
        color: #8ab4f8;
      }
      [data-theme="dark"] .desc-tag.place {
        background: #2e1f3e;
        color: #c58af9;
      }

      @media (max-width: 768px) {
        .day-summary {
          padding: 10px var(--space-4);
          gap: 6px;
        }
      }
```

- [ ] **Step 2: 브라우저에서 `index.html` 열어 스타일 오류 없는지 확인**

개발자도구 Console에 CSS 오류 없어야 함.

- [ ] **Step 3: 커밋**

```bash
git add index.html
git commit -m "style: add day-summary strip and desc-tag CSS"
```

---

## Task 2: Day 1 요약 스트립 + 설명 태그 (쿤밍 도착 · 5/2)

**Files:**
- Modify: `index.html` — Day 1 섹션 (`<!-- DAY 1 -->` ~ `<!-- DAY 2 -->`, 약 1368–1580번째 줄)

### 2-1. 요약 스트립 삽입

- [ ] **Step 1: Day 1 `.day-head` 닫는 태그 `</div>` 바로 다음 줄에 삽입**

찾을 위치: `<div class="pill">직항 4시간 30분</div>` 를 포함하는 `.day-head` 블록 직후.

삽입할 HTML:
```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 130–200위안</span>
            <span class="summary-chip chip-weather">⛅ 해발 1,890m · 낮 22–26°C · 자외선 강함</span>
            <span class="summary-chip chip-place">🏞 다관공원 · 디엔치 호수</span>
            <span class="summary-chip chip-food">🍜 윈난 쌀국수 · 윈난 가정식</span>
          </div>
```

### 2-2. 음식 설명 태그 추가

`.desc-tag`는 `.place-popover` 닫는 태그 `</span>` **바로 다음**에 줄바꿈 후 삽입. 스팬 안에 넣지 말 것.

- [ ] **Step 2: NEW WORLD YUN QIAN YI XIAN 팝오버 뒤에 desc-tag 추가**

팝오버 스팬 닫힌 직후 `윈난 쌀국수.` 앞에:
```html
                    <br><span class="desc-tag food">🍜 윈난식 쌀국수·소수민족 간식 전문점 · 취호 인근 · 1인 20–40위안</span>
```

- [ ] **Step 3: 회향희루 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🥘 윈난 전통 가정식 · 버섯·채소 볶음 위주 · 1인 50–80위안</span>
```

- [ ] **Step 4: 윈핑펑웨이위안 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍲 기화계(증기 통닭)·볶음요리 전문 · 1인 50–80위안</span>
```

- [ ] **Step 5: 사방소초 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🥘 윈난 볶음요리 전문 · 다양한 채소·고기 볶음 · 1인 40–60위안</span>
```

- [ ] **Step 6: 일커인 쿤밍 라오팡즈 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🏮 전통 민가(老院子) 분위기 윈난 요리 · 맛·분위기 평가 좋음 · 1인 60–100위안</span>
```

### 2-3. 장소 설명 태그 추가

- [ ] **Step 7: 다관공원 `.place` 스팬 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏞 디엔치 호수 조망 명소 · 다관루 3층 전망대 · 연꽃 정원 · 입장 무료</span>
```

- [ ] **Step 8: 디엔치 호수 `.place` 스팬 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🌅 쿤밍 최대 호수(298㎢) · 호수변 산책로 · 석양 포인트 · 전기자전거 대여 가능</span>
```

- [ ] **Step 9: 브라우저에서 Day 1 카드 확인**

요약 스트립이 헤더 아래 회색 배경으로 보이고, 설명 태그가 각 음식·장소 아래에 파란/보라 뱃지로 표시되는지 확인. 다크모드 전환 시 색상이 바뀌는지 확인.

- [ ] **Step 10: 커밋**

```bash
git add index.html
git commit -m "feat: Day 1 summary strip and description tags"
```

---

## Task 3: Day 2 요약 스트립 + 설명 태그 (석림 · 5/3)

**Files:**
- Modify: `index.html` — Day 2 섹션 (약 1581–1804번째 줄)

- [ ] **Step 1: Day 2 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 200–280위안</span>
            <span class="summary-chip chip-weather">⛅ 해발 1,750m · 낮 24–28°C · 햇빛·자외선 강함</span>
            <span class="summary-chip chip-place">🗿 석림풍경구 (유네스코 세계자연유산)</span>
            <span class="summary-chip chip-food">🍜 현지 간이식 · 기화계</span>
          </div>
```

- [ ] **Step 2: 석림풍경구 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🗿 2억 7천만 년 된 석회암 기둥 숲 · 유네스코 세계자연유산 · 대석림·소석림 코스</span>
```

- [ ] **Step 3: 쿤밍역 팝오버 뒤에 desc-tag 추가 (동차 이동 안내 단계)**

```html
                    <br><span class="desc-tag place">🚉 석림 동차 출발역 · 외국인은 유인 창구에서 여권 제시</span>
```

- [ ] **Step 4: 석림서역 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🚉 석림풍경구 최근접 역 · 石林站과 혼동 주의 · 셔틀 99번 탑승</span>
```

- [ ] **Step 5: 푸저루 기화계 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍲 기화계 전문 노포 · 증기압으로 쪄낸 맑은 통닭 국물 · 쿤밍 대표 맛집</span>
```

- [ ] **Step 6: 브라우저에서 Day 2 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 2 summary strip and description tags"
```

---

## Task 4: Day 3 요약 스트립 + 설명 태그 (쿤밍→샤시 · 5/4)

**Files:**
- Modify: `index.html` — Day 3 섹션 (약 1805–1986번째 줄)

- [ ] **Step 1: Day 3 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 100–150위안 (열차 이동일)</span>
            <span class="summary-chip chip-weather">🚄 고속열차 이동 · 샤시 도착 해발 2,040m · 선선함</span>
            <span class="summary-chip chip-place">🏘 샤시고진 · 사등가 · 옥진교</span>
            <span class="summary-chip chip-food">☕ 현지 간단식 · 샤시 첫 저녁</span>
          </div>
```

- [ ] **Step 2: 샤시고진 `.place` 스팬 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏘 당·송 시대 차마고도 교역 마을 · 대부분 옛 건물 보존 · 조용하고 아늑한 분위기</span>
```

- [ ] **Step 3: 사등가 `.place` 스팬 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🎭 샤시 중심 광장 · 고희대(옛 공연 무대) · 장날 바이족 문화 체험</span>
```

- [ ] **Step 4: 옥진교 `.place` 스팬 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🌉 샤시 마을 입구 옛 돌다리 · 흑혜강 위 · 석양 사진 포인트</span>
```

- [ ] **Step 5: 치차취차 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">☕ 샤시 1순위 티·디저트 카페 · 2층 고성 조망 · 늦은 오픈 (정오 이후 확인)</span>
```

- [ ] **Step 6: 차마고도반점 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍄 버섯 샤브샤브·소고기 요리 · 샤시 현지 식당</span>
```

- [ ] **Step 7: 브라우저 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 3 summary strip and description tags"
```

---

## Task 5: Day 4 요약 스트립 + 설명 태그 (샤시고진 · 5/5)

**Files:**
- Modify: `index.html` — Day 4 섹션 (약 1987–2259번째 줄)

- [ ] **Step 1: Day 4 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 120–180위안</span>
            <span class="summary-chip chip-weather">⛅ 해발 2,040m · 낮 20–25°C · 일교차 큼 · 겉옷 필요</span>
            <span class="summary-chip chip-place">🏘 사등가 · 흥교사 · 옥진교 · 오봉산</span>
            <span class="summary-chip chip-food">☕ 반산 카페 · 우주빵집 · 샤시 현지식</span>
          </div>
```

- [ ] **Step 2: 사등가 & 고성 골목 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🎭 이른 아침 현지 주민 일상 풍경 · 골목길 탐방 추천 시간대</span>
```

- [ ] **Step 3: 옥진교(두 번째 등장) `.place` 뒤에 desc-tag 추가**

해당 스팬은 `data-place-gallery="yujin"` 속성으로 구분.

```html
                    <br><span class="desc-tag place">🌉 옛 돌다리 · 이른 아침 안개와 함께 고즈넉한 분위기</span>
```

- [ ] **Step 4: 흑혜강 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏞 샤시 마을을 흐르는 강 · 강변 산책로 · 한적한 풍경</span>
```

- [ ] **Step 5: 백족 서점 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">📚 바이(백)족 문화 서적·공예품 · 샤시 고성 내 · 아늑한 분위기</span>
```

- [ ] **Step 6: 반산 카페 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">☕ 산중턱 뷰 카페 · 샤시고진 전경 조망 · 커피·음료</span>
```

- [ ] **Step 7: 우주빵집 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🥐 샤시 유명 수제 빵집 · 다양한 빵·케이크 · 현지 여행자 필수 코스</span>
```

- [ ] **Step 8: 샹12 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍽 샤시 현지 식당 · 윈난 가정식 · 소박하고 저렴한 한 끼</span>
```

- [ ] **Step 9: 피터스 키친 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍽 외국인 여행자 친화적 퓨전 식당 · 영어 메뉴 · 샤시 고성 내</span>
```

- [ ] **Step 10: 오봉산 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">⛰ 샤시 인근 야산 · 조용한 트레킹 코스 · 마을 전경 조망</span>
```

- [ ] **Step 11: 치차취차(Day 4 등장분) 팝오버 뒤에 desc-tag 추가**

Day 3과 동일한 desc-tag:
```html
                    <br><span class="desc-tag food">☕ 샤시 1순위 티·디저트 카페 · 2층 고성 조망 · 늦은 오픈 (정오 이후 확인)</span>
```

- [ ] **Step 12: 일루유산 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍽 뷰 좋은 샤시 레스토랑 · 윈난식 요리 · 고성 내 위치</span>
```

- [ ] **Step 13: 브라우저 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 4 summary strip and description tags"
```

---

## Task 6: Day 5 요약 스트립 + 설명 태그 (샤시→리장 · 5/6)

**Files:**
- Modify: `index.html` — Day 5 섹션 (약 2260–2450번째 줄)

- [ ] **Step 1: Day 5 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 150–220위안</span>
            <span class="summary-chip chip-weather">🚌 이동일 · 리장 도착 해발 2,400m · 낮 18–24°C</span>
            <span class="summary-chip chip-place">🏘 수허고성 · 리장 고성</span>
            <span class="summary-chip chip-food">🍜 리장 현지식 · 미선</span>
          </div>
```

- [ ] **Step 2: 수허고성 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏘 리장 인근 조용한 나시족 마을 · 고성보다 한적 · 고성에서 도보 30분</span>
```

- [ ] **Step 3: 식전주미 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍽 윈난 가정식·지역 요리 · 목부(木府) 인근 · 1인 40–70위안</span>
```

- [ ] **Step 4: 도이채원 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🥗 채소·버섯 위주 윈난 건강 요리 · 리장 고성 내</span>
```

- [ ] **Step 5: Hungry Buddha 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍛 외국인 여행자 친화적 식당 · 서양식·인도 퓨전 · 영어 메뉴</span>
```

- [ ] **Step 6: 위천석궈위 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🐟 돌솥 생선찌개 전문 · 리장 특산 요리 · 진한 국물 맛</span>
```

- [ ] **Step 7: 브라우저 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 5 summary strip and description tags"
```

---

## Task 7: Day 6 요약 스트립 + 설명 태그 (옥룡설산·인상여강 · 5/7)

**Files:**
- Modify: `index.html` — Day 6 섹션 (약 2451–2649번째 줄)

- [ ] **Step 1: Day 6 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 500–700위안 (입장료 포함)</span>
            <span class="summary-chip chip-weather">🏔 옥룡설산 최고 해발 4,506m · 방한복·장갑 필수 · 고산증 주의</span>
            <span class="summary-chip chip-place">🏔 옥룡설산 · 람월곡 · 인상여강 공연</span>
            <span class="summary-chip chip-food">🍽 현지 간단식 · 고성 복귀 후 저녁</span>
          </div>
```

- [ ] **Step 2: 옥룡설산 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏔 해발 5,596m 설산 · 리장 대표 랜드마크 · 빙하 전망대 · 방한복 필수</span>
```

- [ ] **Step 3: 람월곡 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">💎 에메랄드빛 빙하 녹은 호수 · 옥룡설산 기슭 · 리장 최고 사진 명소</span>
```

- [ ] **Step 4: 인상여강쇼 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🎭 장이모우 연출 대형 야외 공연 · 해발 3,100m 자연 무대 · 나시족 문화 · 방한복 필수</span>
```

- [ ] **Step 5: 디엔시왕자 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🏔 윈난 산골 가정식 · 현지 식재료 요리 · 리장 고성 인근</span>
```

- [ ] **Step 6: 윈셜리 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🏮 나시족 토사 귀족 문화 컨셉 윈난 요리 · 목부 인근 · 분위기 있는 식당</span>
```

- [ ] **Step 7: 브라우저 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 6 summary strip and description tags"
```

---

## Task 8: Day 7 요약 스트립 + 설명 태그 (리장 탐방 · 5/8)

**Files:**
- Modify: `index.html` — Day 7 섹션 (약 2650–2910번째 줄)

- [ ] **Step 1: Day 7 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 150–250위안</span>
            <span class="summary-chip chip-weather">⛅ 해발 2,400m · 낮 20–25°C · 일교차 큼</span>
            <span class="summary-chip chip-place">🏘 수허고진 · 문해 · 백사고진 · 리장고성</span>
            <span class="summary-chip chip-food">🍜 수허 쌀국수 · 리장 바바 · 버섯 요리</span>
          </div>
```

- [ ] **Step 2: 수허고성(Day 7) `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏘 리장 인근 조용한 나시족 마을 · 고성보다 한적 · 고성에서 도보 30분</span>
```

- [ ] **Step 3: 정종리가토계미선점 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍜 토종닭 쌀국수 전문 · 수허고진 인근 · 진한 닭 육수 쌀국수</span>
```

- [ ] **Step 4: 부한소과반 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍱 윈난 과반(덮밥) 전문 · 간단하고 저렴한 현지 한끼 · 1인 20–35위안</span>
```

- [ ] **Step 5: 문해 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🌊 리장 북서쪽 고산 호수 · 해발 3,100m · 철새 도래지 · 비포장 도로 · 미니버스 필요</span>
```

- [ ] **Step 6: 옥호촌 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏘 옥룡설산 기슭 나시족 마을 · 한적하고 전통 분위기 · 문해 방문 시 경유</span>
```

- [ ] **Step 7: 백사고진 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🎨 나시족 벽화로 유명한 작은 마을 · 고성 북쪽 · 도교·불교·라마교 혼합 문화</span>
```

- [ ] **Step 8: Snow Mountain Cafe 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">☕ 백사고진 인근 설산 뷰 카페 · 여행자 휴식 포인트</span>
```

- [ ] **Step 9: HYGGE cafe 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">☕ 리장 고성 분위기 카페 · 북유럽 감성 인테리어 · 커피·디저트</span>
```

- [ ] **Step 10: 리장고성 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏘 나시족 800년 전통 고성 · 유네스코 세계문화유산 · 돌바닥 골목 · 입장 무료(관리비 80위안)</span>
```

- [ ] **Step 11: 목부 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🏯 나시족 귀족 저택 박물관 · 리장 고성 내 · 입장료 약 60위안</span>
```

- [ ] **Step 12: 아포칭라파이구훠궈 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍖 훈제 돼지갈비 훠궈 · 나시족 전통 요리법 · 리장 고성 인기 맛집</span>
```

- [ ] **Step 13: 수사게 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍲 소고기 국물 샤브샤브 · 새콤한 쏸탕(酸汤) 베이스 · 리장 현지인 맛집</span>
```

- [ ] **Step 14: 균자유 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍄 윈난 야생 버섯 요리 전문 · 다양한 버섯 종류 · 고성점</span>
```

- [ ] **Step 15: 브라우저 확인 후 커밋**

```bash
git add index.html
git commit -m "feat: Day 7 summary strip and description tags"
```

---

## Task 9: Day 8 요약 스트립 + 설명 태그 (리장→쿤밍 귀국 · 5/9)

**Files:**
- Modify: `index.html` — Day 8 섹션 (약 2911번째 줄~)

- [ ] **Step 1: Day 8 `.day-head` 직후에 요약 스트립 삽입**

```html
          <div class="day-summary">
            <span class="summary-chip chip-budget">💰 예산 약 100–150위안</span>
            <span class="summary-chip chip-weather">🚄 이동일 · 쿤밍 공항 22:25 출발</span>
            <span class="summary-chip chip-place">🦢 취호공원 · 쿤밍 시내</span>
            <span class="summary-chip chip-food">🍜 쿤밍 쌀국수 · 마지막 윈난식</span>
          </div>
```

- [ ] **Step 2: 취호공원 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🦢 쿤밍 도심 속 호수 공원 · 겨울 철새(갈매기) 명소 · 윈난대학 인근 · 입장 무료</span>
```

- [ ] **Step 3: 난핑제 `.place` 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag place">🛍 쿤밍 시내 번화가 · 쇼핑·먹거리 집결지 · 공항 가기 전 마지막 쇼핑</span>
```

- [ ] **Step 4: 천시더우화미선 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍜 두부(豆花)를 얹은 쌀국수 · 쿤밍 아침식사 명소 · 1인 10–20위안</span>
```

- [ ] **Step 5: 반포소궈미선 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍜 개인 소솥 쌀국수 · 직접 재료를 익혀 먹는 윈난식 쌀국수 · 1인 15–25위안</span>
```

- [ ] **Step 6: 소석궈위찬팅 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🐟 돌솥 생선 요리 전문 · 공항 가기 전 마지막 윈난 식사로 추천</span>
```

- [ ] **Step 7: 총수루 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍃 보이차·약초 식재료 활용 윈난 생태 요리 · 건강식 컨셉</span>
```

- [ ] **Step 8: 윈핑펑웨이위안(Day 8) 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🍲 기화계(증기 통닭)·볶음요리 전문 · 1인 50–80위안</span>
```

- [ ] **Step 9: 리기 베트남소권분 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🌯 베트남식 라이스페이퍼 롤 · 쿤밍 소수민족 거리 간식 · 1인 10–20위안</span>
```

- [ ] **Step 10: 일커인 쿤밍 라오팡즈(Day 8) 팝오버 뒤에 desc-tag 추가**

```html
                    <br><span class="desc-tag food">🏮 전통 민가(老院子) 분위기 윈난 요리 · 맛·분위기 평가 좋음 · 1인 60–100위안</span>
```

- [ ] **Step 11: 브라우저 전체 확인 — Day 1~8 모두 스트립·태그 정상 표시 여부**

- [ ] **Step 12: 최종 커밋**

```bash
git add index.html
git commit -m "feat: Day 8 summary strip and description tags — traveler UI complete"
```

---

## Self-Review

**스펙 커버리지:**
- ✅ Day 카드 상단 요약 스트립 (8일치)
- ✅ 음식 설명 태그 (`.desc-tag.food`)
- ✅ 장소 설명 태그 (`.desc-tag.place`)
- ✅ 한자 클립보드 버튼 — 기존 `initPlaceHanCopyButtons()` JS 그대로 활용, HTML 변경 불필요
- ✅ 모달·팝오버 동작 변경 없음 (`.desc-tag`는 스팬 외부에 위치)
- ✅ 다크모드 CSS 대응

**플레이스홀더 스캔:** 없음 — 모든 desc-tag 내용이 구체적으로 명시됨.

**타입 일관성:** `.desc-tag.food`, `.desc-tag.place`, `.day-summary`, `.summary-chip`, `.chip-budget/weather/place/food` — Task 1 CSS 정의와 Task 2–9 사용 일치.
