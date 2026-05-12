# Python Playwright Locators — Complete In-Depth Guide

Playwright locators are the primary way to find and interact with elements on a page. They are **auto-waiting** and **retry-able** — Playwright will automatically wait for an element to be visible, enabled, and stable before interacting with it.

---

## Table of Contents

- [Python Playwright Locators — Complete In-Depth Guide](#python-playwright-locators--complete-in-depth-guide)
  - [Table of Contents](#table-of-contents)
  - [1. CSS Selector Locator](#1-css-selector-locator)
  - [2. XPath Locator](#2-xpath-locator)
  - [3. Text Locator](#3-text-locator)
  - [4. Role Locator (ARIA)](#4-role-locator-aria)
  - [5. Label Locator](#5-label-locator)
  - [6. Placeholder Locator](#6-placeholder-locator)
  - [7. Alt Text Locator](#7-alt-text-locator)
  - [8. Title Locator](#8-title-locator)
  - [9. Test ID Locator](#9-test-id-locator)
  - [10. Filter Locator](#10-filter-locator)
  - [11. Chaining Locators](#11-chaining-locators)
  - [12. nth Locator](#12-nth-locator)
  - [13. first and last Locators](#13-first-and-last-locators)
  - [14. has Locator](#14-has-locator)
  - [15. Frame Locator](#15-frame-locator)
  - [16. Shadow DOM Locator](#16-shadow-dom-locator)
  - [17. Locator.all() — Multiple Elements](#17-locatorall--multiple-elements)
  - [18. Locator Assertions](#18-locator-assertions)
  - [19. Custom Locator Strategies](#19-custom-locator-strategies)
  - [20. Best Practices](#20-best-practices)
    - [Key Rules](#key-rules)
    - [Auto-Waiting Summary](#auto-waiting-summary)
  - [Quick Reference Card](#quick-reference-card)

---

## 1. CSS Selector Locator

The most flexible locator. Uses standard CSS selectors — tags, classes, IDs, attributes, pseudo-selectors.

**Syntax:**

```python
page.locator("css=selector")
# OR shorthand (CSS is the default)
page.locator("selector")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # By tag name
    heading = page.locator("h1")
    print(heading.text_content())

    # By class name
    page.locator(".submit-btn").click()

    # By ID
    page.locator("#username").fill("admin")

    # By attribute
    page.locator("input[type='password']").fill("secret")

    # Nested selector
    page.locator("form .login-form input[name='email']").fill("user@test.com")

    # Pseudo-selector
    page.locator("li:nth-child(2)").click()

    # Multiple attributes
    page.locator("button[type='submit'][data-action='login']").click()

    browser.close()
```

---

## 2. XPath Locator

Use XPath expressions to locate elements. Powerful for traversing the DOM tree, especially parent-child-sibling relationships.

**Syntax:**

```python
page.locator("xpath=//expression")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Absolute XPath
    page.locator("xpath=/html/body/div/h1").text_content()

    # Relative XPath by tag
    page.locator("xpath=//button").click()

    # By attribute value
    page.locator("xpath=//input[@name='username']").fill("admin")

    # By partial text
    page.locator("xpath=//button[contains(text(),'Submit')]").click()

    # By exact text
    page.locator("xpath=//a[text()='Home']").click()

    # Parent to child
    page.locator("xpath=//form[@id='login']//input[@type='email']").fill("a@b.com")

    # Sibling axis
    page.locator("xpath=//label[text()='Username']/following-sibling::input").fill("john")

    # Ancestor axis
    page.locator("xpath=//span[@class='error']/ancestor::div[@class='field']")

    browser.close()
```

> **Tip:** Prefer role/text locators over XPath when possible — they are more readable and resilient.

---

## 3. Text Locator

Finds elements by their visible text content. One of the most human-readable locator strategies.

**Syntax:**

```python
page.get_by_text("exact text")
page.get_by_text("partial", exact=False)  # default is False
page.get_by_text("Exact!", exact=True)
```

**Examples:**

```python
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Partial match (default)
    page.get_by_text("Sign In").click()

    # Exact match
    page.get_by_text("Sign In", exact=True).click()

    # Case-insensitive partial (use regex)
    page.get_by_text(re.compile("sign in", re.IGNORECASE)).click()

    # Get text content
    message = page.get_by_text("Welcome back").text_content()
    print(message)

    # Works on any element containing that text
    page.get_by_text("Delete Account").nth(0).click()

    browser.close()
```

---

## 4. Role Locator (ARIA)

The **recommended** approach by Playwright. It queries elements by their ARIA role and accessible name — mirrors what assistive technologies and users see.

**Syntax:**

```python
page.get_by_role("role", name="accessible name")
```

**Common ARIA Roles:** `button`, `link`, `textbox`, `checkbox`, `radio`, `combobox`, `listbox`, `option`, `heading`, `img`, `dialog`, `alert`, `navigation`, `main`, `row`, `cell`, `tab`, `tabpanel`

**Examples:**

```python
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Click a button by accessible name
    page.get_by_role("button", name="Submit").click()

    # Click a link
    page.get_by_role("link", name="Home").click()

    # Fill a textbox
    page.get_by_role("textbox", name="Email").fill("user@example.com")

    # Check a checkbox
    page.get_by_role("checkbox", name="Remember me").check()

    # Select a radio button
    page.get_by_role("radio", name="Male").check()

    # Heading verification
    heading = page.get_by_role("heading", name="Dashboard")
    heading.wait_for()

    # Exact name match
    page.get_by_role("button", name="Login", exact=True).click()

    # Regex match
    page.get_by_role("button", name=re.compile(r"submit|send", re.IGNORECASE)).click()

    # Disabled check
    page.get_by_role("button", name="Save", disabled=True)

    # Expanded state (for dropdowns/menus)
    page.get_by_role("combobox", name="Country", expanded=False).click()

    browser.close()
```

---

## 5. Label Locator

Finds form inputs (`input`, `textarea`, `select`) that are associated with a `<label>` element — by the label's text.

**Syntax:**

```python
page.get_by_label("Label Text")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Works when <label for="id"> or <label><input></label>
    page.get_by_label("Username").fill("john_doe")
    page.get_by_label("Password").fill("MyP@ssw0rd")
    page.get_by_label("Email Address").fill("john@example.com")

    # Select dropdown by label
    page.get_by_label("Country").select_option("India")

    # Textarea by label
    page.get_by_label("Message").fill("Hello, this is a test message.")

    # Exact match
    page.get_by_label("Name", exact=True).fill("John")

    browser.close()
```

**HTML it targets:**

```html
<!-- Case 1: for/id association -->
<label for="user">Username</label>
<input id="user" type="text" />

<!-- Case 2: wrapping label -->
<label>
  Password
  <input type="password" />
</label>
```

---

## 6. Placeholder Locator

Finds `input` or `textarea` elements by their `placeholder` attribute value.

**Syntax:**

```python
page.get_by_placeholder("placeholder text")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Fill by placeholder
    page.get_by_placeholder("Enter your email").fill("user@test.com")
    page.get_by_placeholder("Search...").fill("playwright")
    page.get_by_placeholder("Enter password").fill("secure123")

    # Exact match
    page.get_by_placeholder("Search", exact=True).fill("locators")

    # Regex match
    page.get_by_placeholder(re.compile(r"enter.*email", re.IGNORECASE)).fill("a@b.com")

    browser.close()
```

**HTML it targets:**

```html
<input type="text" placeholder="Enter your email" />
<textarea placeholder="Write your message here..."></textarea>
```

---

## 7. Alt Text Locator

Finds `<img>` elements (and other elements with `alt` attributes) by their `alt` attribute value.

**Syntax:**

```python
page.get_by_alt_text("alt text")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Find image by alt text
    logo = page.get_by_alt_text("Company Logo")
    logo.wait_for()

    # Click an image button with alt text
    page.get_by_alt_text("User Avatar").click()

    # Partial match (default)
    page.get_by_alt_text("profile photo")

    # Exact match
    page.get_by_alt_text("Profile Photo", exact=True)

    # Verify visibility
    assert page.get_by_alt_text("Success Icon").is_visible()

    browser.close()
```

---

## 8. Title Locator

Finds elements by their `title` attribute value. Commonly used for tooltips and icon buttons.

**Syntax:**

```python
page.get_by_title("title text")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    # Find by title attribute
    page.get_by_title("Close dialog").click()
    page.get_by_title("Download PDF").click()

    # Tooltip elements
    tooltip_element = page.get_by_title("More information")
    tooltip_element.hover()

    # Partial match
    page.get_by_title("Delete")

    # Exact match
    page.get_by_title("Delete Item", exact=True).click()

    browser.close()
```

**HTML it targets:**

```html
<button title="Close dialog">x</button>
<a href="/report.pdf" title="Download PDF">Download</a>
```

---

## 9. Test ID Locator

Finds elements by a custom `data-testid` attribute (or any configured attribute). This is the most **stable** locator since test IDs are not affected by UI redesigns.

**Syntax:**

```python
page.get_by_test_id("test-id-value")
```

**Configure custom attribute:**

```python
playwright.selectors.set_test_id_attribute("data-qa")  # default is data-testid
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Change test ID attribute globally
    p.selectors.set_test_id_attribute("data-cy")  # e.g., for Cypress-style IDs

    page = browser.new_page()
    page.goto("https://example.com")

    # Default: data-testid
    page.get_by_test_id("login-button").click()
    page.get_by_test_id("username-input").fill("admin")
    page.get_by_test_id("password-input").fill("pass123")
    page.get_by_test_id("submit-btn").click()

    # Verify element exists
    assert page.get_by_test_id("success-message").is_visible()

    browser.close()
```

**HTML it targets:**

```html
<button data-testid="login-button">Login</button>
<input data-testid="username-input" type="text" />
```

---

## 10. Filter Locator

Narrows down a set of locators using `.filter()` with text or another locator condition.

**Syntax:**

```python
locator.filter(has_text="text")
locator.filter(has=page.locator("child-selector"))
locator.filter(has_not_text="text")
locator.filter(has_not=page.locator("selector"))
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/products")

    # Filter list items by text
    product = page.locator(".product-card").filter(has_text="Laptop")
    product.locator("button.add-to-cart").click()

    # Filter by child element presence
    active_users = page.locator(".user-row").filter(
        has=page.locator(".badge-active")
    )
    print(active_users.count())

    # Filter by NOT having text
    non_sold = page.locator(".product-card").filter(has_not_text="Sold Out")
    non_sold.first.click()

    # Filter by NOT having a child element
    available_rows = page.locator("tr").filter(
        has_not=page.locator("td.disabled")
    )

    # Chained filters
    rows = (
        page.locator("tr")
        .filter(has_text="Premium")
        .filter(has=page.locator("td.available"))
    )
    print(rows.count())

    browser.close()
```

---

## 11. Chaining Locators

Scope a locator inside another locator to narrow the search to a specific DOM subtree.

**Syntax:**

```python
parent_locator.locator("child-selector")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/dashboard")

    # Chain locators
    sidebar = page.locator("#sidebar")
    sidebar.get_by_role("link", name="Settings").click()

    # Table row interaction
    row = page.locator("table tbody tr").filter(has_text="John Doe")
    row.get_by_role("button", name="Edit").click()

    # Card-level scoping
    card = page.locator(".card").filter(has_text="Order #1234")
    card.locator(".status-badge").text_content()
    card.get_by_role("button", name="View Details").click()

    # Form section scoping
    address_section = page.locator("section#shipping-address")
    address_section.get_by_label("Street").fill("123 Main St")
    address_section.get_by_label("City").fill("New York")
    address_section.get_by_label("ZIP").fill("10001")

    browser.close()
```

---

## 12. nth Locator

When multiple elements match, select a specific one by its 0-based index.

**Syntax:**

```python
locator.nth(index)    # 0-based index
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/items")

    # Get the 1st item (index 0)
    page.locator(".item").nth(0).click()

    # Get the 3rd item (index 2)
    page.locator(".item").nth(2).text_content()

    # Get the 5th row in a table
    page.locator("table tr").nth(4).locator("td.price").text_content()

    # Get 2nd button in a form
    page.locator("form button").nth(1).click()

    # Combine with filter
    page.locator(".notification").filter(has_text="Error").nth(0).locator(".close").click()

    browser.close()
```

---

## 13. first and last Locators

Convenience shortcuts for `.nth(0)` and the last element.

**Syntax:**

```python
locator.first    # equivalent to .nth(0)
locator.last     # equivalent to the last matched element
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/list")

    all_items = page.locator(".list-item")

    # First element
    first_item = all_items.first
    print(first_item.text_content())

    # Last element
    last_item = all_items.last
    last_item.click()

    # First matching role
    page.get_by_role("button").first.click()

    # Last row in a table
    last_row = page.locator("tbody tr").last
    last_row.locator("button.delete").click()

    # First error message
    page.locator(".error-msg").first.text_content()

    browser.close()
```

---

## 14. has Locator

The `has` and `has_text` options allow you to find a parent element that contains a specific child element or text.

**Syntax:**

```python
# Inline with locator()
page.locator("parent", has=page.locator("child"))
page.locator("parent", has_text="some text")

# With filter()
page.locator("parent").filter(has=page.locator("child"))
page.locator("parent").filter(has_text="text")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/shop")

    # Find product card that contains an "On Sale" badge
    on_sale = page.locator(".product-card", has=page.locator(".badge-sale"))
    print(on_sale.count())
    on_sale.first.click()

    # Find a row containing "Active" status
    active_row = page.locator("tr", has_text="Active")
    active_row.locator("button.edit").click()

    # Find a div that contains a specific button
    card_with_delete = page.locator(".card", has=page.get_by_role("button", name="Delete"))
    card_with_delete.nth(0).highlight()

    # Negative: does NOT have
    out_of_stock = page.locator(".product", has_not=page.locator(".in-stock"))
    print(out_of_stock.count())

    browser.close()
```

---

## 15. Frame Locator

Interact with elements inside `<iframe>` elements. Returns a `FrameLocator`.

**Syntax:**

```python
page.frame_locator("iframe-selector")
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/page-with-iframe")

    # Target iframe by CSS selector
    frame = page.frame_locator("iframe#payment-frame")

    # Interact inside the iframe
    frame.get_by_label("Card Number").fill("4111 1111 1111 1111")
    frame.get_by_label("Expiry Date").fill("12/26")
    frame.get_by_label("CVV").fill("123")
    frame.get_by_role("button", name="Pay Now").click()

    # Nested iframes
    outer_frame = page.frame_locator("iframe#outer")
    inner_frame = outer_frame.frame_locator("iframe#inner")
    inner_frame.get_by_text("Submit").click()

    # By src attribute
    page.frame_locator("iframe[src*='payment']").get_by_role("button", name="Submit").click()

    # reCAPTCHA example
    captcha_frame = page.frame_locator("iframe[title='reCAPTCHA']")
    captcha_frame.get_by_role("checkbox", name="I'm not a robot").click()

    browser.close()
```

---

## 16. Shadow DOM Locator

Playwright **automatically pierces open shadow roots** — no special syntax needed. Standard locators work inside shadow DOMs.

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/shadow-dom-page")

    # Playwright auto-pierces shadow DOM
    page.locator("my-custom-element input").fill("hello")
    page.locator("user-card .name").text_content()
    page.get_by_role("button", name="Submit").click()  # even inside shadow DOM

    # Interacting with a custom element's shadow root input
    shadow_input = page.locator("search-widget").locator("input[type='search']")
    shadow_input.fill("playwright")
    shadow_input.press("Enter")

    browser.close()
```

> **Note:** This only works with **open** shadow roots. Closed shadow roots (`mode: "closed"`) cannot be accessed.

---

## 17. Locator.all() — Multiple Elements

Returns a list of all matching `Locator` objects so you can iterate over them.

**Syntax:**

```python
elements = locator.all()   # sync API
```

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/products")

    # Get all product names
    items = page.locator(".product-name").all()
    for item in items:
        print(item.text_content())

    # Click all unchecked checkboxes
    checkboxes = page.get_by_role("checkbox").all()
    for checkbox in checkboxes:
        if not checkbox.is_checked():
            checkbox.check()

    # Collect all link hrefs
    links = page.get_by_role("link").all()
    hrefs = [link.get_attribute("href") for link in links]
    print(hrefs)

    # Validate all error messages
    errors = page.locator(".error-message").all()
    error_texts = [e.text_content() for e in errors]
    assert "Field is required" in error_texts

    # Count elements
    rows = page.locator("table tbody tr").all()
    print(f"Total rows: {len(rows)}")

    browser.close()
```

---

## 18. Locator Assertions

Playwright provides powerful built-in assertions via `expect()` that auto-wait and retry.

**Import:**

```python
from playwright.sync_api import expect
```

**Examples:**

```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    btn = page.get_by_role("button", name="Submit")

    # Visibility
    expect(btn).to_be_visible()
    expect(btn).not_to_be_visible()

    # Enabled/Disabled
    expect(btn).to_be_enabled()
    expect(btn).to_be_disabled()

    # Text content
    expect(page.locator("h1")).to_have_text("Welcome")
    expect(page.locator(".price")).to_contain_text("$")

    # Attribute
    expect(page.locator("img.logo")).to_have_attribute("alt", "Company Logo")

    # Value (input)
    expect(page.get_by_label("Email")).to_have_value("user@example.com")

    # Count
    expect(page.locator(".item")).to_have_count(5)

    # CSS class
    expect(btn).to_have_class("btn-primary")

    # Checked state
    expect(page.get_by_role("checkbox", name="Agree")).to_be_checked()

    # Focused
    expect(page.get_by_label("Search")).to_be_focused()

    # URL
    expect(page).to_have_url("https://example.com/dashboard")

    # Title
    expect(page).to_have_title("Dashboard")

    # Custom timeout
    expect(page.locator(".spinner")).not_to_be_visible(timeout=10000)

    browser.close()
```

---

## 19. Custom Locator Strategies

Combine multiple locators for complex real-world scenarios.

**Examples:**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/admin")

    # Strategy 1: Locate by partial attribute
    page.locator("[data-action*='delete']").first.click()

    # Strategy 2: Locate by multiple classes
    page.locator(".btn.btn-danger.confirm").click()

    # Strategy 3: Adjacent sibling (CSS)
    page.locator("label:has-text('Country') + select").select_option("India")

    # Strategy 4: Combine role + filter
    page.get_by_role("listitem").filter(has_text="Premium Plan").get_by_role("button", name="Select").click()

    # Strategy 5: Locator + keyboard interaction
    search = page.get_by_role("searchbox")
    search.fill("playwright")
    search.press("Enter")

    # Strategy 6: Drag and drop
    source = page.locator("#drag-source")
    target = page.locator("#drop-target")
    source.drag_to(target)

    # Strategy 7: Hover then click submenu
    page.get_by_role("menuitem", name="Products").hover()
    page.get_by_role("menuitem", name="Laptops").click()

    browser.close()
```

---

## 20. Best Practices

| Priority | Strategy               | Why                                 |
| -------- | ---------------------- | ----------------------------------- |
| 1st      | `get_by_role()`        | Reflects accessibility semantics    |
| 2nd      | `get_by_label()`       | Mirrors user interaction with forms |
| 3rd      | `get_by_test_id()`     | Stable, immune to UI changes        |
| 4th      | `get_by_text()`        | Readable and user-centric           |
| 5th      | `get_by_placeholder()` | Good for unlabelled inputs          |
| 6th      | `locator("css")`       | Fragile if classes change           |
| Last     | `locator("xpath")`     | Verbose, brittle, hard to maintain  |

### Key Rules

```python
# DO: Use semantic, stable locators
page.get_by_role("button", name="Submit").click()
page.get_by_label("Email").fill("user@example.com")
page.get_by_test_id("checkout-btn").click()

# AVOID: Fragile positional or implementation-specific selectors
page.locator("div > div:nth-child(3) > span").click()  # breaks easily
page.locator(".xyz123").click()  # CSS-module generated class, unstable

# DO: Chain for scoping
page.locator(".order-card").filter(has_text="Order #100").get_by_role("button", name="Cancel").click()

# DO: Use assertions (they auto-wait)
from playwright.sync_api import expect
expect(page.get_by_text("Success")).to_be_visible()

# AVOID: Manual sleep
import time
time.sleep(3)  # Never use this in Playwright tests
```

### Auto-Waiting Summary

Playwright automatically waits for:

- Element to be **attached** to DOM
- Element to be **visible**
- Element to be **stable** (no animations)
- Element to be **enabled**
- Element to be **editable** (for fill actions)
- Element to **receive events** (not obscured)

You rarely need explicit waits — locators handle it all.

---

## Quick Reference Card

```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    page = p.chromium.launch().new_page()

    # All locator strategies at a glance:
    page.locator("css-selector")                          # CSS
    page.locator("xpath=//xpath")                         # XPath
    page.get_by_text("text")                              # Text
    page.get_by_role("button", name="name")               # ARIA Role
    page.get_by_label("Label")                            # Label
    page.get_by_placeholder("Placeholder")                # Placeholder
    page.get_by_alt_text("Alt text")                      # Alt text
    page.get_by_title("Title")                            # Title
    page.get_by_test_id("test-id")                        # Test ID
    page.locator(".item").filter(has_text="text")         # Filter
    page.locator(".parent").locator(".child")             # Chaining
    page.locator(".item").nth(2)                          # nth
    page.locator(".item").first                           # first
    page.locator(".item").last                            # last
    page.locator(".parent", has=page.locator(".child"))   # has
    page.frame_locator("iframe")                          # Frame
    page.locator(".item").all()                           # All elements
```

---

_Reference: Python Playwright Docs — https://playwright.dev/python/docs/locators_
