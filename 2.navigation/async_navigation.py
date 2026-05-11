from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await  context.new_page()
        # await page.goto("https://quotes.toscrape.com/") # Navigate to a URL
        # await page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")
        # await page.goto("https://quotes.toscrape.com/", wait_until="networkidle")
        # await page.goto("https://quotes.toscrape.com/", wait_until="commit")

        # await page.goto("https://quotes.toscrape.com/", timeout=60000)

        await page.goto("https://quotes.toscrape.com/", wait_until="commit")
        # await asyncio.timeout(5)

        # await page.reload()
        # await page.reload(timeout=60000)
        # await page.reload(wait_until="domcontentloaded")

        # await page.goto("https://getbootstrap.com/docs/5.3/components/navbar/")
        # print("Current page:", page.url)
        # print(await page.title())

        # # Go back to the previous page
        # await page.go_back()
        # print("After go_back:", page.url)


        await page.goto("https://getbootstrap.com/docs/5.3/components/navbar/")
        # Go back first
        await page.go_back()
        print("After go_back:", page.url)
        print(await page.title())

        # Now go forward
        await page.go_forward()
        print("After go_forward:", page.url) 

        print(await page.title())
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())