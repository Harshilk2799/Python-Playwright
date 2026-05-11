from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")

# p = sync_playwright().start()
# browser = p.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto("https://quotes.toscrape.com/")
# time.sleep(5)
# page.close()