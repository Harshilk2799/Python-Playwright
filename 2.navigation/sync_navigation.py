from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.goto("https://quotes.toscrape.com/") # Navigate to a URL
    # page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")
    # page.goto("https://quotes.toscrape.com/", wait_until="networkidle")
    # page.goto("https://quotes.toscrape.com/", wait_until="commit")

    # page.goto("https://quotes.toscrape.com/", timeout=60000)

    page.goto("https://quotes.toscrape.com/", wait_until="commit")
    # time.sleep(5)

    # page.reload()
    # page.reload(timeout=60000)
    # page.reload(wait_until="domcontentloaded")

    # page.goto("https://getbootstrap.com/docs/5.3/components/navbar/")
    # print("Current page:", page.url)
    # print(page.title())

    # # Go back to the previous page
    # page.go_back()
    # print("After go_back:", page.url)


    page.goto("https://getbootstrap.com/docs/5.3/components/navbar/")
    # Go back first
    page.go_back()
    print("After go_back:", page.url)
    print(page.title())

    # Now go forward
    page.go_forward()
    print("After go_forward:", page.url) 

    print(page.title())
    page.close()