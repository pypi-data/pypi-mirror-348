import asyncio
from enum import Enum
from mugennocore.model.interfaces import IManga  # type: ignore
from mugennoscraper.controller.scrappers.rawkuma.handler import search, manga, az_list
from mugennoscraper.controller.helper import (
    Sources,
    extract_az_params,
    extract_search_params,
    check_source,
)


async def search_query(query: str) -> IManga | None:
    source, title, lang, include_nsfw = await extract_search_params(query)
    source_enum = check_source(source, lang)

    if source_enum == Sources.RAWKUMA:
        resp = await search(title)
        if not resp:
            return None
        links = resp[0]
        if not links:
            return None
        # Executa todas as chamadas manga(link) em paralelo
        return await asyncio.gather(*(manga(link) for link in links))

    return None


async def az_query(query: str):
    source, lang, letter, page, include_nsfw = await extract_az_params(query)
    source_enum = check_source(source, lang)

    if source_enum == Sources.RAWKUMA:
        resp = await az_list(letter, page)
        if not resp:
            return None
        links = resp[0]
        if not links:
            return None

        return await manga(*links)

    return None
