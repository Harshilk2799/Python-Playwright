from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://quotes.toscrape.com/login")

    page.locator("input#username").fill("harshil")
    page.locator("input#password").fill("harshil")
    page.locator("input[type='submit']").click()

    if page.get_by_role("link", name="Logout").is_visible():

        while True:

            records = page.locator(".quote").all()
            
            for record in records:
                author = record.locator("small.author").text_content()
                quote = record.locator("span.text").text_content()
                tags = record.locator("a.tag").all_text_contents()

                print(f"Author: {author}\n")
                print(f"Quote: {quote}\n")
                print(f"Tags: {tags}\n")
                print("-" * 50)

            next_button = page.locator("li.next a")
            if next_button.is_visible():
                next_button.click()
                page.wait_for_load_state("load")
            else:
                break
        

    page.close()