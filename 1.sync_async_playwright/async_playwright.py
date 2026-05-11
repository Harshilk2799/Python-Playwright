from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://quotes.toscrape.com/")
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())