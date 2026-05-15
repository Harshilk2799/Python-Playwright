from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://quotes.toscrape.com/")
        # page.screenshot(path="demo.png")

        title = page.query_selector("h1 a")
        print("Title: ", title.inner_text())

        # page.wait_for_timeout(2000)
        
        login_button = page.query_selector("p a[href='/login']")
        login_button.click()

        user_input = page.query_selector("input[id='username']")
        user_input.type("Username")

        password_input = page.query_selector("input[id='password']")
        password_input.type("Password")

        login_button = page.query_selector("input[value='Login']")
        login_button.click()

        try:
            logout = page.wait_for_selector("p a[href='/logout']", timeout=50000)
        except:
            print("Login Failed")
            exit()
        print(logout.inner_text())

        try:
            while True:
                all_quotes = page.query_selector_all(".quote")
                for quote in all_quotes:
                    text = quote.query_selector("span[itemprop='text']")
                    print("Text: ", text.inner_text())

                    author = quote.query_selector("span small.author")
                    print("Author: ", author.inner_text())

                    tags = quote.query_selector_all(".tags a.tag")

                    all_tags = []
                    for tag in tags:
                        all_tags.append(tag.inner_text())

                    print("All Tags: ", all_tags)
                next_button = page.query_selector("li.next a")
                next_button.click()
                print("*"*50)
        except:
            print("Does not have a any page")
        browser.close()


if __name__ == "__main__":
    main()
