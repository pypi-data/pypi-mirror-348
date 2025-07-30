import asyncio
import typer
import mugennoscraper.controller.scrappers.rawkuma.handler as handler
from mugennoscraper.controller.router import search_query

app = typer.Typer()  # Cria um app principal


@app.command()
def search(query: str, page: int = 1):
    """Busca títulos de mangá com a query dada."""

    async def run():
        resp = await handler.search(query, page)
        typer.secho("Titles:", fg=typer.colors.MAGENTA, bold=True)
        print(resp[1])  # prints readable titles
        typer.secho("URLs:", fg=typer.colors.MAGENTA, bold=True)
        print(resp[0])

    asyncio.run(run())


@app.command()
def manga(url: str):
    """Busca detalhes de um mangá dado a URL."""

    async def run():
        resp = await handler.manga(url)
        print(resp)

    asyncio.run(run())

@app.command()
def pages(url: str):
    """Busca paginas de um mangá dado a URL do chapter."""

    async def run():
        resp = await handler.pages(url)
        print(resp)

    asyncio.run(run())


@app.command()
def az_list(letter: str, page: int = 1):
    """Busca títulos de mangá com a letra dada."""

    async def run():
        resp = await handler.az_list(letter, page)
        typer.secho("Titles:", fg=typer.colors.MAGENTA, bold=True)
        print(resp[1])  # prints readable titles
        typer.secho("URLs:", fg=typer.colors.MAGENTA, bold=True)
        print(resp[0])

    asyncio.run(run())


@app.command()
def query(query: str):
    "Busca mangas"

    async def run():
        resp = await search_query(query)
        typer.secho("Mangas:", fg=typer.colors.MAGENTA, bold=True)
        print(resp)

    asyncio.run(run())


if __name__ == "__main__":
    app()
