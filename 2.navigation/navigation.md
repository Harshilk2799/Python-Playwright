# 🎭 Playwright Page Navigation Methods

Playwright provides powerful navigation methods to control browser page movement programmatically. This guide covers the essential navigation methods with practical examples.

---

## Table of Contents

- [🎭 Playwright Page Navigation Methods](#-playwright-page-navigation-methods)
  - [Table of Contents](#table-of-contents)
  - [1. `page.goto(url)` — Navigate to a URL](#1-pagegotourl--navigate-to-a-url)
    - [`wait_until` Options](#wait_until-options)
    - [Key Parameters](#key-parameters)
  - [2. `page.reload()` — Reload the Current Page](#2-pagereload--reload-the-current-page)
    - [Common Use Cases](#common-use-cases)
  - [3. `page.go_back()` — Navigate Back](#3-pagego_back--navigate-back)
  - [4. `page.go_forward()` — Navigate Forward](#4-pagego_forward--navigate-forward)
  - [5. Complete Example — All Methods Together](#5-complete-example--all-methods-together)
  - [⚡ Async Version](#-async-version)
  - [📋 Quick Reference Table](#-quick-reference-table)
    - [Shared Options for All Navigation Methods](#shared-options-for-all-navigation-methods)
  - [💡 Tips \& Best Practices](#-tips--best-practices)

---

## 1. `page.goto(url)` — Navigate to a URL

Navigates the page to a given URL and waits for the page to load before continuing.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Basic navigation
    page.goto("https://example.com")

    # With options: timeout and wait_until
    page.goto(
        "https://example.com",
        timeout=60000,             # Wait up to 60 seconds
        wait_until="networkidle"  # Wait until network is idle
    )

    print(page.title())
    browser.close()
```

### `wait_until` Options

| Option               | Description                                  |
| -------------------- | -------------------------------------------- |
| `"load"`             | Wait for the `load` event _(default)_        |
| `"domcontentloaded"` | Wait until the DOM is fully parsed and ready |
| `"networkidle"`      | Wait until no network requests for 500ms     |
| `"commit"`           | Wait until response headers are received     |

### Key Parameters

| Parameter    | Type    | Description                               |
| ------------ | ------- | ----------------------------------------- |
| `url`        | `str`   | The URL to navigate to                    |
| `timeout`    | `float` | Max time in milliseconds (default: 30000) |
| `wait_until` | `str`   | When to consider navigation complete      |
| `referer`    | `str`   | Optional HTTP Referer header              |

---

## 2. `page.reload()` — Reload the Current Page

Reloads the current page, equivalent to pressing **F5** in the browser.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://example.com")

    # Simple reload
    page.reload()

    # Reload with options
    page.reload(
        timeout=30000,
        wait_until="domcontentloaded"
    )

    print("Page reloaded:", page.url)
    browser.close()
```

### Common Use Cases

- Refreshing dynamic or real-time content
- Resetting page state between test steps
- Simulating a user pressing F5 or Ctrl+R
- Clearing JavaScript state without changing the URL

---

## 3. `page.go_back()` — Navigate Back

Goes back to the previous page in the browser history — like clicking the browser's **Back** button.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://example.com")
    page.goto("https://example.com/about")
    print("Current page:", page.url)   # https://example.com/about

    # Go back to the previous page
    page.go_back()
    print("After go_back:", page.url)  # https://example.com

    browser.close()
```

> **Note:** `go_back()` returns `None` if there is no previous page in history.

---

## 4. `page.go_forward()` — Navigate Forward

Goes forward to the next page in the browser history — like clicking the browser's **Forward** button.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://example.com")
    page.goto("https://example.com/about")

    # Go back first
    page.go_back()
    print("After go_back:", page.url)     # https://example.com

    # Now go forward
    page.go_forward()
    print("After go_forward:", page.url)  # https://example.com/about

    browser.close()
```

> **Note:** `go_forward()` returns `None` if there is no next page in history.

---

## 5. Complete Example — All Methods Together

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True for CI
    page = browser.new_page()

    # Step 1: goto - Navigate to the home page
    page.goto("https://example.com", wait_until="load")
    print("Step 1 - goto:", page.url)

    # Step 2: goto - Navigate to a second page
    page.goto("https://example.com/about", wait_until="load")
    print("Step 2 - goto /about:", page.url)

    # Step 3: go_back - Return to the previous page
    page.go_back(wait_until="load")
    print("Step 3 - go_back:", page.url)

    # Step 4: go_forward - Move forward again
    page.go_forward(wait_until="load")
    print("Step 4 - go_forward:", page.url)

    # Step 5: reload - Refresh the current page
    page.reload(wait_until="networkidle")
    print("Step 5 - reload:", page.url)

    browser.close()
```

**Expected Output:**

```
Step 1 - goto: https://example.com/
Step 2 - goto /about: https://example.com/about
Step 3 - go_back: https://example.com/
Step 4 - go_forward: https://example.com/about
Step 5 - reload: https://example.com/about
```

---

## ⚡ Async Version

For use with async frameworks like FastAPI, aiohttp, or pytest-asyncio:

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to pages
        await page.goto("https://example.com")
        await page.goto("https://example.com/contact")

        # Navigate through history
        await page.go_back()
        await page.go_forward()

        # Reload the page
        await page.reload(wait_until="networkidle")

        print("Final URL:", page.url)
        await browser.close()

asyncio.run(main())
```

---

## 📋 Quick Reference Table

| Method              | Description                  | Returns            |
| ------------------- | ---------------------------- | ------------------ |
| `page.goto(url)`    | Navigate to a URL            | `Response \| None` |
| `page.reload()`     | Reload current page          | `Response \| None` |
| `page.go_back()`    | Go to previous history entry | `Response \| None` |
| `page.go_forward()` | Go to next history entry     | `Response \| None` |

### Shared Options for All Navigation Methods

| Option       | Type    | Default  | Description                       |
| ------------ | ------- | -------- | --------------------------------- |
| `timeout`    | `float` | `30000`  | Maximum wait time in milliseconds |
| `wait_until` | `str`   | `"load"` | When to consider navigation done  |

---

## 💡 Tips & Best Practices

1. **Always set `wait_until`** — Use `"networkidle"` for SPAs and dynamic pages, `"domcontentloaded"` for faster tests when full load isn't needed.
2. **Handle `None` returns** — `go_back()` and `go_forward()` return `None` if there's no history to navigate.
3. **Use `timeout` wisely** — Increase timeout for slow pages; decrease for fast unit tests.
4. **Prefer `async` in production** — Async Playwright is better suited for concurrent browser automation tasks.
5. **Check URL after navigation** — Always assert `page.url` in tests to confirm you landed on the correct page.

---

_Generated with Playwright Python SDK — [Official Docs](https://playwright.dev/python/docs/navigations)_
