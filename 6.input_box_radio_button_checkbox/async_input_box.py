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
        # await page.fill("input#email", "harshil@gmail.com")
        # await page.fill("input#name", "Harshil")
        # await page.fill("input#phone", "7984985798")

        # Method 2
        # await page.locator("input#name").fill("harshil")
        # await page.locator("input#email").fill("harshil@gmail.com")
        # await page.locator("input#phone").fill("7984985798")

        # Method 3
        # await page.locator("input#name").type("harshil")
        # await page.locator("input#email").type("harshil@gmail.com")
        # await page.locator("input#phone").type("7984985798")

        # Method 4
        # await page.locator("input#name").press_sequentially("harshil")
        # await page.locator("input#email").press_sequentially("harshil@gmail.com")
        # await page.locator("input#phone").press_sequentially("7984985798")

        # await page.locator("input#phone").fill("7984985798")
        # await page.locator("input#phone").clear()

        phone_locator = page.locator("input#phone")
        await phone_locator.fill("64654532132")
        print("Phone value is: ", await phone_locator.input_value())

        await page.wait_for_timeout(5000)
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())