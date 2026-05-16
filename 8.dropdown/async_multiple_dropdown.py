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
        # await page.locator("#colors").select_option(value=["red", "blue", "green", "white"])
        # await page.select_option("#colors", value=["red", "blue", "green", "white"])

        # Method 2
        # await page.locator("#colors").select_option(label=["Red", "Blue", "Green"])
        # await page.select_option("#colors", label=["Red", "Blue", "Green"])

        # Method 3
        # await page.locator("#colors").select_option(index=[0, 2, 3])
        # await page.select_option("#colors", index=[0, 2, 3])


        # dropdown_options = page.locator("#colors > option")
        # print("count: ", await dropdown_options.count())
        # print("Content: ", await dropdown_options.all_text_contents())

        # options_text = [text.strip() for text in await dropdown_options.all_text_contents()]
        # print(options_text)


        # sorted dropdow
        # dropdown_options = page.locator("#colors>option")
        dropdown_options = page.locator("#animals>option")
        
        options_text = [text.strip() for text in await dropdown_options.all_text_contents()]
        
        original_list = options_text.copy()
        sorted_list = sorted(options_text)

        print("Original list: ", original_list)
        print("Sorted list: ", sorted_list)

        if original_list == sorted_list:
            print("Dropdown options are sorted order...")
        else:
            print("Dropdown options are not sorted order...")

        await page.wait_for_timeout(5000)
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())