import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):
    """
    This removes unwanted HTML tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content, tags: list[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            # If the tag is a link (a tag), append its href as well
            if tag == "a":
                href = element.get('href')
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
                else:
                    text_parts.append(element.get_text())
            else:
                text_parts.append(element.get_text())

    return ' '.join(text_parts)


def remove_unessesary_lines(content):
    # Split content into lines
    lines = content.split("\n")

    # Strip whitespace for each line
    stripped_lines = [line.strip() for line in lines]

    # Filter out empty lines
    non_empty_lines = [line for line in stripped_lines if line]

    # Remove duplicated lines (while preserving order)
    seen = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in seen or seen.add(line))]

    # Join the cleaned lines without any separators (remove newlines)
    cleaned_content = "".join(deduped_lines)

    return cleaned_content

import random
import time
# async def ascrape_playwright(url, tags: list[str] = ["h1", "h2", "h3", "span", "section"]) -> str:
#     print("Started scraping...")
#     results = ""
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         try:
#             context = await browser.new_context(
#                 user_agent=random.choice(USER_AGENTS),  # Use a random user agent
#                 bypass_csp=True,  # Bypass Content Security Policy (CSP)
#                 ignore_https_errors=True  # Ignore HTTPS errors
#             )

#             page = await context.new_page()
#             await page.goto(url, wait_until="networkidle")  # Wait for page to fully load

#             # Introduce a random delay to mimic human behavior
#             delay = random.uniform(2, 5)
#             time.sleep(delay)

#             page_source = await page.content()

#             soup = BeautifulSoup(page_source, "html.parser")
#             section = soup.find("section", class_="search-results")
#             if section:
#                 results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(str(section)), tags))
#             else:
#                 results = "No <section class='search-results'> element found on the page."

#             print("Content scraped")
#         except Exception as e:
#             results = f"Error: {e}"
#         await browser.close()
#     return results

async def ascrape_playwright(url, tags):
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            context = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),  # Use a random user agent
                bypass_csp=True,  # Bypass Content Security Policy (CSP)
                ignore_https_errors=True  # Ignore HTTPS errors
            )

            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")

            # Click/select the div with class="search-toolbar__sorting" to trigger a search
            # await page.locator('.search-toolbar__sorting').click()
            number_of_elements = await page.locator('.search-toolbar__sorting').count()
            element = await page.locator('.search-toolbar__sorting')
            visible = await page.locator('.search-toolbar__sorting').is_visible()
            enabled = await page.locator('.search-toolbar__sorting').is_enabled()
            print("number_of_elements: ", number_of_elements)
            print("element: ", element)
            print("visible: ", visible)
            print("enabled: ", enabled)
            
            # Introduce a random delay to mimic human behavior
            delay = random.uniform(2, 5)
            await page.wait_for_timeout(delay * 1000)

            page_source = await page.content()

            soup = BeautifulSoup(page_source, "html.parser")
            section = soup.find("section", class_="search-results")
            if section:
                results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(str(section)), tags))
            else:
                results = "No <section class='search-results'> element found on the page."

            print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
]

def extract_card_data(html_content):
    card_name = soup.select_one('.product-card__title.truncate').get_text(strip=True)
    card_list_from = float(soup.select_one('.inventory__price-with-shipping').get_text(strip=True)[1:])
    card_market_price = float(soup.select_one('.product-card__market-price--value').get_text(strip=True)[1:])
    card_set_name = soup.select_one('.product-card__set-name.bottom-margin').get_text(strip=True)
    card_set_rarity = soup.select_one('.product-card__rarity span:nth-child(1)').get_text(strip=True)
    card_set_number = int(soup.select_one('.product-card__rarity span:nth-child(3)').get_text(strip=True).split('#')[1].split('/')[0])
    
    return {
        'card_name': card_name,
        'card_list_from': card_list_from,
        'card_market_price': card_market_price,
        'card_set_name': card_set_name,
        'card_set_number': card_set_number,
        'card_set_rarity': card_set_rarity
    }


    # TESTING
if __name__ == "__main__":
    # url = "https://www.patagonia.ca/shop/new-arrivals"
    url = "https://www.tcgplayer.com/search/pokemon/sv-scarlet-and-violet-151?view=grid&productLineName=pokemon&setName=sv-scarlet-and-violet-151&ProductTypeName=Cards&page=1"
    # url = "https://www.yahoo.com/?guccounter=1"

    async def scrape_playwright():
        results = await ascrape_playwright(url)  # No need to pass tags here
        pprint.pprint(results)
        # card_data = extract_card_data(results)
        # pprint.pprint(card_data)

    pprint.pprint(asyncio.run(scrape_playwright()))