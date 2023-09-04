from .. import *


async def search(word: str) -> List[Entry]:
    headers_ = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://sozluk.gov.tr/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.51 "
        "Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    async with ClientSession(headers=headers_) as session:
        async with session.get(general_search(word)) as response:
            words = json.loads(await response.read())
            if not isinstance(words, list):
                if isinstance(words, dict) and "error" in words:
                    if words["error"] == "Sonuç bulunamadı":  # No results
                        return []
                    raise RuntimeError(
                        f'The server responded with an error: {words["error"]} ({word})'
                    )
                else:
                    raise RuntimeError(
                        f"Invalid response type {type(words).__name__} received. (expected list)"
                    )
            else:
                entry_parser = Entry.parse
                return list(map(entry_parser, words))
