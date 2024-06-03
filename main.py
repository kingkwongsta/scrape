# .venv\Scripts\activate
# in docker make sure to run playwright install

import asyncio
import pprint
# from scrape import ascrape_playwright

if __name__ == "__main__":
    token_limit = 16385
    url="https://www.tcgplayer.com/search/pokemon/sv-scarlet-and-violet-151?view=grid&productLineName=pokemon&setName=sv-scarlet-and-violet-151&ProductTypeName=Cards&page=1"
    
    async def scrape_with_playwright():
        html_content = await ascrape_playwright(url, tags)

    asyncio.run(scrape_with_playwright())
    
