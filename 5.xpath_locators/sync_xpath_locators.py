from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://quotes.toscrape.com/login")

    page.locator("//input[@id='username']").fill("harshil")
    page.locator("//input[@id='password']").fill("harshil")
    page.locator("//input[@type='submit']").click()

    page.wait_for_load_state("load")

    if page.get_by_role("link", name="Logout").is_visible():

        while True:
            records = page.locator("xpath=//div[@class='quote']").all()

            for record in records:
                author = record.locator("xpath=.//span/small[@class='author']").text_content()
                quote = record.locator("xpath=.//span[@class='text']").text_content()
                tags = record.locator("xpath=.//div[@class='tags']/a[@class='tag']").all_text_contents()

                print(f"Author: {author}\n")
                print(f"Quote: {quote}\n")
                print(f"Tags: {tags}\n")
                print("-" * 50)

            next_button = page.locator("xpath=//li[@class='next']/a")

            if next_button.is_visible():
                next_button.click()
                page.wait_for_load_state("load")
            else:
                break

    browser.close()