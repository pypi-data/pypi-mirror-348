from mugennocore.model.interfaces import IManga  # type: ignore
from mugennoscraper.controller.scrappers.rawkuma.const import (
    URL_AZ_DEEP,
    URL_SEARCH_DEEP,
)
from mugennoscraper.controller.scrappers.rawkuma.manga import (
    create_manga_instance,
    extract_chapters,
)
from mugennoscraper.controller.scrappers.rawkuma.page import extract_image_urls
from mugennoscraper.controller.scrappers.rawkuma.search import (
    extract_links,
    extract_pagination,
    extract_titles,
)
from mugennoscraper.utils.html import get_html, parse_html


async def search(query: str, page: int = 1) -> tuple[list[str], list[str]]:
    url = URL_SEARCH_DEEP.format(page=page, query=query)
    html = await get_html(url)
    soup = await parse_html(html)
    links = await extract_links(soup)
    titles = await extract_titles(soup)
    return links, titles


async def manga(url: str) -> IManga:
    html = await get_html(url)
    soup = await parse_html(html)
    print(await extract_chapters(soup))
    return await create_manga_instance(soup)


async def az_list(letter: str, page: int = 1) -> tuple[list[str], list[str]]:
    html = await get_html(URL_AZ_DEEP.format(page=page, letter=letter))
    soup = await parse_html(html)
    links = await extract_links(soup)
    titles = await extract_titles(soup)
    return links, titles

async def pages(url: str) -> list[str]:
    html = await get_html(url)
    soup = await parse_html(html)
    pages = await extract_image_urls(soup)
    return pages