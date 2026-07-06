import logging

from bs4 import BeautifulSoup
from watch_contract import RenderCrawler, Item, CrawlerException

logger = logging.getLogger(__name__)

_BOARD_URL = "https://cafe.naver.com/f-e/cafes/31258781/menus/8"

_ARTICLE_SELECTOR = "table.article-table tbody tr"
_TITLE_SELECTOR = "a.article"
_AUTHOR_SELECTOR = ".nickname"
_DATE_SELECTOR = ".type_date"


class WorkhubCrawler(RenderCrawler):
    def render_request(self, params: dict) -> dict:
        return {
            "url": _BOARD_URL,
            "wait_for": _ARTICLE_SELECTOR,
        }

    def parse(self, html: str, params: dict) -> list[Item]:
        try:
            soup = BeautifulSoup(html, "html.parser")
            items = []
            for article in soup.select(_ARTICLE_SELECTOR):
                try:
                    title_el = article.select_one(_TITLE_SELECTOR)
                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    href = title_el.get("href")
                    if not href:
                        continue

                    author_el = article.select_one(_AUTHOR_SELECTOR)
                    author = author_el.get_text(strip=True) if author_el else ""

                    date_el = article.select_one(_DATE_SELECTOR)
                    date = date_el.get_text(strip=True) if date_el else ""

                    items.append(Item(
                        id=href,
                        title=title,
                        url=href,
                        data={"author": author, "date": date},
                    ))
                except Exception:
                    continue

            logger.info("파싱 완료: %d개", len(items))
            return items
        except Exception as e:
            logger.error("parse 예외: %s", e)
            raise CrawlerException(str(e)) from e
