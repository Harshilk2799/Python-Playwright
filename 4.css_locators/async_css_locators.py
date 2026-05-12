from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://quotes.toscrape.com/login")

        await page.locator("input#username").fill("harshil")
        await page.locator("input#password").fill("harshil")
        await page.locator("input[type='submit']").click()
        await page.wait_for_load_state("load")

        if await page.get_by_role("link", name="Logout").is_visible():

            while True:

                records = await page.locator(".quote").all()
                
                for record in records:
                    author = await record.locator("small.author").text_content()
                    quote = await record.locator("span.text").text_content()
                    tags = await record.locator("a.tag").all_text_contents()

                    print(f"Author: {author}\n")
                    print(f"Quote: {quote}\n")
                    print(f"Tags: {tags}\n")
                    print("-" * 50)

                next_button = page.locator("li.next a")
                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_load_state("load")
                else:
                    break
            
        await page.close()    

if __name__ == "__main__":
    asyncio.run(main())