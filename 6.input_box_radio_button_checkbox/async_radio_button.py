from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://testautomationpractice.blogspot.com/")

        # Method 1
        # await page.locator("input#male").click()
        # is_male_selected = await page.locator("input[value='male']").is_checked()
        # is_female_selected = await page.locator("input[value='female']").is_checked()

        # print(f"Male selected: {is_male_selected}")
        # print(f"Female selected: {is_female_selected}")

        # Method 2
        await page.get_by_role("radio", name="Female").check()
        is_male_selected = await page.locator("input[value='male']").is_checked()
        is_female_selected = await page.locator("input[value='female']").is_checked()

        print(f"Male selected: {is_male_selected}")
        print(f"Female selected: {is_female_selected}")

        await page.wait_for_timeout(5000)
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())