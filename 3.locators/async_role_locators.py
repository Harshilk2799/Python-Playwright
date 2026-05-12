from playwright.async_api import async_playwright
import asyncio

async def main():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # await page.goto("https://testautomationpractice.blogspot.com/")

        # 1. get_by_placeholder()
        # await page.get_by_placeholder("Enter Name").fill("Harshil")
        # await page.get_by_placeholder("Enter EMail").fill("harshil@gmail.com")
        # await page.get_by_placeholder("Enter Phone").fill("7984955789")

        await page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")

        # 2. get_by_text()
        # await page.get_by_text("List item 1")
        # await page.get_by_text("List item 1", exact=True)

        # 3. get_by_label()
        # await page.get_by_label("email").fill("harshil@gmail.com")
        # await page.get_by_label("password").fill("harshil")
        # await page.wait_for_timeout(5000)

        # 4. get_by_alt_text()
        # await page.get_by_alt_text("logo image", exact=True).is_visible()
        # print("Working")

        # 5. get_by_title()
        # print(await page.get_by_title("Home page link").is_visible())

        # 6. get_by_test_id()
        # print(await page.get_by_test_id("product-price").all_text_contents())

        # 7. get_by_role()
        print(await page.get_by_role("button", name="Primary Action").inner_text())
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())