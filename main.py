# .venv\Scripts\activate
# in docker make sure to run playwright install

import asyncio
import pprint

from extract import extract
from scrape import ascrape_playwright
from schemas import PokemonCards

if __name__ == "__main__":
    token_limit = 16385
    url="https://www.tcgplayer.com/search/pokemon/sv-scarlet-and-violet-151?view=grid&productLineName=pokemon&setName=sv-scarlet-and-violet-151&ProductTypeName=Cards&page=1"
    
    async def scrape_with_playwright(url: str, tags, **kwargs):
        html_content = await ascrape_playwright(url, tags)
        print("Extracting content with LLM")

        html_content_fits_context_window_llm = html_content[:token_limit]
        extracted_content = extract(**kwargs,
                                    content=html_content_fits_context_window_llm)

        pprint.pprint(extracted_content)

        
    asyncio.run(scrape_with_playwright(
        url=url,
        tags=["span"],
        schema_pydantic=PokemonCards
    ))
    
