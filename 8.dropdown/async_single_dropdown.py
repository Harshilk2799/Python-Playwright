from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://testautomationpractice.blogspot.com/")
        await page.wait_for_load_state("load")

        # Method 1
        # await page.locator("#country").select_option("India")
        # await page.select_option("#country", "India")

        # Method 2
        # await page.locator("#country").select_option(value="india")
        # await page.select_option("#country", value="india")

        # Method 3
        # await page.locator("#country").select_option(index=9)
        # await page.select_option("#country", index=9)


        dropdown_options = page.locator("#country > option")
        print("count: ", await dropdown_options.count())
        print("Content: ", await dropdown_options.all_text_contents())

        options_text = [text.strip() for text in await dropdown_options.all_text_contents()]
        print(options_text)


        await page.wait_for_timeout(5000)
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())