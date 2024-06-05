# .venv\Scripts\activate
# https://github.com/trancethehuman/entities-extraction-web-scraper
# in docker make sure to run playwright install

import asyncio
import pprint

from extract import extract
from scrape import ascrape_playwright
from schemas import PokemonCards, Pokemon

if __name__ == "__main__":
    token_limit = 16385
    url="https://www.tcgplayer.com/search/pokemon/sv-scarlet-and-violet-151?view=grid&productLineName=pokemon&setName=sv-scarlet-and-violet-151&ProductTypeName=Cards&page=1"
    
    async def scrape_with_playwright(url: str, tags, **kwargs):
        html_content = await ascrape_playwright(url, tags)
        # print("Extracting content with LLM")

        # html_content_fits_context_window_llm = html_content[:token_limit]
        # extracted_content = extract(content=html_content_fits_context_window_llm, **kwargs,)
        # pprint.pprint(extracted_content)
        
        pprint.pprint(html_content)

    asyncio.run(scrape_with_playwright(
        url=url,
        tags=["section"],
        schema_pydantic=Pokemon
    ))
    
