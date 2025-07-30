from enum import Enum
import re


class Sources(Enum):
    RAWKUMA = "rawkuma"


# Define as fontes suportadas e seus idiomas
SOURCES = {"rawkuma": {"en", "jp"}}


async def extract_search_params(query: str) -> tuple[str, str, str, bool]:
    """
    Extrai o título do mangá, fonte, idioma e flag NSFW a partir de uma string como:
    "One Piece source?=rawkuma lang?=pt nsfw?=true"
    """
    # Regex para capturar parâmetros opcionais no formato chave?=valor
    pattern = re.compile(r"(\w+)\?=([^\s]+)")
    matches = pattern.findall(query)

    # Extrai parâmetros encontrados
    params = {key.lower(): value for key, value in matches}

    # Remove os parâmetros da string original para deixar só o título
    title = pattern.sub("", query).strip()

    # Define valores padrão
    source = params.get("source", "rawkuma").lower()
    lang = params.get("lang", "en").lower()
    include_nsfw = params.get("nsfw", "false").lower() in ("true", "1", "yes")

    return source, title, lang, include_nsfw


async def extract_az_params(string: str) -> tuple[str, str, str, int, bool]:
    """
    Exemplo de string: "rawkuma:en:A:1:nsfw"
    """
    parts = string.split(":")
    if len(parts) < 2:
        raise ValueError(
            "Formato inválido. Esperado: fonte:lang[:letter[:page[:nsfw]]]"
        )

    source = parts[0].lower()
    lang = parts[1].lower() if len(parts) > 1 else "en"
    letter = parts[2].lower() if len(parts) > 2 else "a"
    page = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 1
    include_nsfw = len(parts) > 4 and parts[4].lower() == "nsfw"

    return source, lang, letter, page, include_nsfw


def check_source(source: str, lang: str) -> Sources | None:
    "Verifica se a fonte e o idioma são válidos"
    if source in SOURCES and lang in SOURCES[source]:
        return Sources[source.upper()]
    return None
