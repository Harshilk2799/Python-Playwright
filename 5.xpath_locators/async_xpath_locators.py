from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://quotes.toscrape.com/login")

        await page.locator("//input[@id='username']").fill("harshil")
        await page.locator("//input[@id='password']").fill("harshil")
        await page.locator("//input[@type='submit']").click()

        await page.wait_for_load_state("load")

        if await page.get_by_role("link", name="Logout").is_visible():

            while True:
                records = await page.locator("xpath=//div[@class='quote']").all()

                for record in records:
                    author = await record.locator("xpath=.//span/small[@class='author']").text_content()
                    quote = await record.locator("xpath=.//span[@class='text']").text_content()
                    tags = await record.locator("xpath=.//div[@class='tags']/a[@class='tag']").all_text_contents()

                    print(f"Author: {author}\n")
                    print(f"Quote: {quote}\n")
                    print(f"Tags: {tags}\n")
                    print("-" * 50)

                next_button = page.locator("xpath=//li[@class='next']/a")

                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_load_state("load")
                else:
                    break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())