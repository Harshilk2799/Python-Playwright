from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://quotes.toscrape.com/")
        # page.screenshot(path="demo.png")

        title = await page.query_selector("h1 a")
        print("Title: ", await title.inner_text())

        # page.wait_for_timeout(2000)
        
        login_button = await page.query_selector("p a[href='/login']")
        await login_button.click()

        user_input = await page.query_selector("input[id='username']")
        await user_input.type("Username")

        password_input = await page.query_selector("input[id='password']")
        await password_input.type("Password")

        login_button = await page.query_selector("input[value='Login']")
        await login_button.click()

        try:
            logout = await page.wait_for_selector("p a[href='/logout']", timeout=50000)
        except:
            print("Login Failed")
            exit()
        print(await logout.inner_text())

        try:
            while True:
                all_quotes = await page.query_selector_all(".quote")
                for quote in all_quotes:
                    text = await quote.query_selector("span[itemprop='text']")
                    print("Text: ", await text.inner_text())

                    author = await quote.query_selector("span small.author")
                    print("Author: ", await author.inner_text())

                    tags = await quote.query_selector_all(".tags a.tag")

                    all_tags = []
                    for tag in tags:
                        all_tags.append(await tag.inner_text())

                    print("All Tags: ", all_tags)
                next_button = await page.query_selector("li.next a")
                await next_button.click()
                print("*"*50)
        except:
            print("Does not have a any page")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
