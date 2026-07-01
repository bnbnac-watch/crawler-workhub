from watch_contract import BaseCrawler, Item, CrawlerException

_BOARD_URL = "https://cafe.naver.com/f-e/cafes/31258781/menus/8"
_BASE_URL = "https://cafe.naver.com"

# 아래 셀렉터는 실제 페이지 구조 확인 후 수정 필요
_ARTICLE_SELECTOR = "li.article-item"
_TITLE_SELECTOR = "a.article-title"
_AUTHOR_SELECTOR = ".article-author"
_DATE_SELECTOR = ".article-date"


class WorkhubCrawler(BaseCrawler):
    async def crawl(self, page) -> list[Item]:
        try:
            await page.goto(_BOARD_URL, wait_until="networkidle", timeout=30000)

            await page.wait_for_selector(_ARTICLE_SELECTOR, timeout=10000)
            articles = await page.query_selector_all(_ARTICLE_SELECTOR)

            items = []
            for article in articles:
                try:
                    title_el = await article.query_selector(_TITLE_SELECTOR)
                    if not title_el:
                        continue

                    title = (await title_el.inner_text()).strip()
                    href = await title_el.get_attribute("href")
                    if not href:
                        continue
                    if not href.startswith("http"):
                        href = f"{_BASE_URL}{href}"

                    author_el = await article.query_selector(_AUTHOR_SELECTOR)
                    author = (await author_el.inner_text()).strip() if author_el else ""

                    date_el = await article.query_selector(_DATE_SELECTOR)
                    date = (await date_el.inner_text()).strip() if date_el else ""

                    items.append(Item(
                        id=href,
                        title=title,
                        url=href,
                        data={"author": author, "date": date},
                    ))
                except Exception:
                    continue

            return items
        except Exception as e:
            raise CrawlerException(str(e)) from e
