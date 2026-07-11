# crawler-workhub

네이버 카페 "SW개발자 취업카페" 게시판 크롤러. `RenderCrawler` 구현 — 네이버 카페 게시판도 JS 렌더링이 필요해 `watch-playwright`를 거친다. 고정된 게시판 하나만 보므로 다른 크롤러와 달리 `params`로 받는 값이 없다.

## API

### POST /crawl

body 불필요(빈 객체도 허용). 고정 URL `https://cafe.naver.com/f-e/cafes/31258781/menus/8`을 `table.article-table tbody tr`이 나타날 때까지 대기한 뒤 렌더 결과를 파싱한다.

응답: `Item[]` — `data`에 `author`, `date` 포함

### GET /health

`{"status": "ok"}`

## id (중복 감지 키)

```python
items.append(Item(id=href, title=title, url=href, ...))
```

게시글 permalink(href)를 그대로 `id`로 쓴다 — 네이버 카페 게시글 URL은 세션에 따라 바뀌는 쿼리스트링이 없어 안정적이다. 카카오 채널과 달리 게시글 수정 시 재알림 요구사항도 없어 텍스트를 조합하지 않는다.

## 환경변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `WATCH_PLAYWRIGHT_URL` | `http://watch-playwright:8080` | |

## 포트

| 포트 | 용도 |
|---|---|
| 8080 | aiohttp — 컴포즈 내부에서만 노출 |
