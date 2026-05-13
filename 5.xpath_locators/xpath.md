# Python Playwright — XPath Locators: Complete In-Depth Guide

> A comprehensive reference for every XPath locator strategy available in Python Playwright, with real-world examples, best practices, and pitfalls.

---

## Table of Contents

- [Python Playwright — XPath Locators: Complete In-Depth Guide](#python-playwright--xpath-locators-complete-in-depth-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What is XPath?](#1-what-is-xpath)
    - [XPath Anatomy](#xpath-anatomy)
  - [2. XPath in Playwright](#2-xpath-in-playwright)
  - [3. XPath Locator Types \& Strategies](#3-xpath-locator-types--strategies)
    - [3.1 Absolute XPath](#31-absolute-xpath)
    - [3.2 Relative XPath](#32-relative-xpath)
    - [3.3 By Attribute](#33-by-attribute)
    - [3.4 By Text Content](#34-by-text-content)
    - [3.5 By Partial Text — `contains()` on Text](#35-by-partial-text--contains-on-text)
    - [3.6 By Partial Attribute — `contains()` on Attribute](#36-by-partial-attribute--contains-on-attribute)
    - [3.7 By `starts-with()`](#37-by-starts-with)
    - [3.8 By `normalize-space()`](#38-by-normalize-space)
    - [3.9 By Multiple Attributes — `and` / `or`](#39-by-multiple-attributes--and--or)
    - [3.10 By Index / Position](#310-by-index--position)
    - [3.11 By `last()`](#311-by-last)
    - [3.12 By Parent Navigation](#312-by-parent-navigation)
    - [3.13 By Sibling Navigation — `following-sibling` / `preceding-sibling`](#313-by-sibling-navigation--following-sibling--preceding-sibling)
    - [3.14 By Ancestor Axis](#314-by-ancestor-axis)
    - [3.15 By Descendant Axis](#315-by-descendant-axis)
    - [3.16 By `following` / `preceding` Axes](#316-by-following--preceding-axes)
    - [3.17 By Child Axis](#317-by-child-axis)
    - [3.18 By Self Axis](#318-by-self-axis)
    - [3.19 Wildcard XPath — `*`](#319-wildcard-xpath--)
    - [3.20 XPath with Multiple Conditions](#320-xpath-with-multiple-conditions)
    - [3.21 XPath with `not()`](#321-xpath-with-not)
    - [3.22 XPath with `count()`](#322-xpath-with-count)
    - [3.23 XPath with `string-length()`](#323-xpath-with-string-length)
    - [3.24 Dynamic XPath](#324-dynamic-xpath)
    - [3.25 XPath inside Frames / iFrames](#325-xpath-inside-frames--iframes)
  - [4. Using XPath with Playwright APIs](#4-using-xpath-with-playwright-apis)
  - [5. Chaining XPath with Playwright Locators](#5-chaining-xpath-with-playwright-locators)
  - [6. XPath vs Other Locators](#6-xpath-vs-other-locators)
  - [7. Best Practices](#7-best-practices)
  - [8. Common Mistakes \& Fixes](#8-common-mistakes--fixes)
    - [Mistake 1: Forgetting parentheses for indexing](#mistake-1-forgetting-parentheses-for-indexing)
    - [Mistake 2: Exact text match fails due to whitespace](#mistake-2-exact-text-match-fails-due-to-whitespace)
    - [Mistake 3: Class attribute partial match](#mistake-3-class-attribute-partial-match)
    - [Mistake 4: Forgetting frame context for iframes](#mistake-4-forgetting-frame-context-for-iframes)
    - [Mistake 5: Using `//` when you mean direct child](#mistake-5-using--when-you-mean-direct-child)
  - [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## 1. What is XPath?

**XPath** (XML Path Language) is a query language used to navigate and select nodes in an XML/HTML document. It describes the location of elements in a tree structure.

### XPath Anatomy

```
//tagName[@attribute='value']
^  ^        ^         ^
|  |        |         └── Attribute value
|  |        └──────────── Attribute name
|  └───────────────────── Tag name (element)
└──────────────────────── // = anywhere in document
```

---

## 2. XPath in Playwright

Playwright uses XPath locators via the `page.locator()` method with an `xpath=` prefix or the shorthand `//` or `(//`.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")

    # Method 1: xpath= prefix
    element = page.locator("xpath=//button[@id='submit']")

    # Method 2: shorthand (// at start is auto-detected as XPath)
    element = page.locator("//button[@id='submit']")

    element.click()
    browser.close()
```

> **Note:** Both `xpath=//...` and `//...` work. The `xpath=` prefix is explicit and recommended for clarity.

---

## 3. XPath Locator Types & Strategies

---

### 3.1 Absolute XPath

Starts from the **root** of the HTML document. Fragile — breaks on any structural change.

**Syntax:** `/html/body/div/form/input`

```python
# HTML:
# <html><body><div><form><input type="text" /></form></div></body></html>

element = page.locator("/html/body/div/form/input")
element.fill("Hello World")
```

> ❌ **Avoid in production** — any DOM restructuring breaks it.

---

### 3.2 Relative XPath

Starts from **anywhere** in the document using `//`. This is the most common strategy.

**Syntax:** `//tagName`

```python
# HTML:
# <button class="btn-primary">Login</button>

# Select any <button> anywhere in the page
element = page.locator("//button")

# More specific
element = page.locator("//form//input")  # <input> inside any <form>
element.fill("test@example.com")
```

---

### 3.3 By Attribute

Locate elements using their HTML attributes (`id`, `class`, `name`, `type`, `href`, etc.).

**Syntax:** `//tag[@attribute='value']`

```python
# HTML:
# <input type="email" id="email" name="user_email" placeholder="Enter email" />

# By id
page.locator("//input[@id='email']").fill("user@example.com")

# By name
page.locator("//input[@name='user_email']").fill("user@example.com")

# By type
page.locator("//input[@type='email']").fill("user@example.com")

# By placeholder
page.locator("//input[@placeholder='Enter email']").fill("user@example.com")

# By href
page.locator("//a[@href='/login']").click()

# By class
page.locator("//button[@class='btn btn-primary']").click()
```

---

### 3.4 By Text Content

Select elements by their **exact visible text**.

**Syntax:** `//tag[text()='Exact Text']`

```python
# HTML:
# <button>Submit Form</button>
# <h1>Welcome to Dashboard</h1>
# <a>Click Here</a>

# Click button with exact text
page.locator("//button[text()='Submit Form']").click()

# Find heading by exact text
page.locator("//h1[text()='Welcome to Dashboard']").is_visible()

# Find any element with exact text
page.locator("//*[text()='Click Here']").click()
```

---

### 3.5 By Partial Text — `contains()` on Text

Locate elements containing **part** of a text string.

**Syntax:** `//tag[contains(text(), 'partial text')]`

```python
# HTML:
# <button>Submit & Save</button>
# <p>Your order #12345 has been placed successfully.</p>

# Button with partial text
page.locator("//button[contains(text(), 'Submit')]").click()

# Paragraph with partial text
msg = page.locator("//p[contains(text(), 'placed successfully')]")
assert msg.is_visible()

# Any element containing partial text
page.locator("//*[contains(text(), 'Dashboard')]").click()
```

---

### 3.6 By Partial Attribute — `contains()` on Attribute

Locate elements where an attribute **contains** a substring.

**Syntax:** `//tag[contains(@attribute, 'partial-value')]`

```python
# HTML:
# <button class="btn btn-primary btn-lg">Save</button>
# <input id="username_field_01" />
# <a href="https://example.com/products/shoes">Shoes</a>

# Class contains partial value
page.locator("//button[contains(@class, 'btn-primary')]").click()

# ID contains partial value
page.locator("//input[contains(@id, 'username')]").fill("john_doe")

# href contains partial URL
page.locator("//a[contains(@href, 'products')]").click()
```

---

### 3.7 By `starts-with()`

Match attribute values that **start with** a specific string. Useful for auto-generated IDs.

**Syntax:** `//tag[starts-with(@attribute, 'prefix')]`

```python
# HTML:
# <input id="user_name_abc123" />
# <button id="btn_save_001">Save</button>
# <div class="panel-header-main">...</div>

# ID starts with 'user_name'
page.locator("//input[starts-with(@id, 'user_name')]").fill("Alice")

# Button ID starts with 'btn_save'
page.locator("//button[starts-with(@id, 'btn_save')]").click()

# Class starts with 'panel'
page.locator("//div[starts-with(@class, 'panel')]").is_visible()
```

---

### 3.8 By `normalize-space()`

Handles elements where text has **leading/trailing spaces or extra whitespace**.

**Syntax:** `//tag[normalize-space(text())='Expected Text']`

```python
# HTML:
# <button>   Submit   </button>
# <p>   Welcome   User   </p>

# Without normalize-space, text() won't match due to extra spaces
# This FAILS: page.locator("//button[text()='Submit']")

# This WORKS:
page.locator("//button[normalize-space(text())='Submit']").click()

# Also works for attributes with unintended spaces
page.locator("//p[normalize-space()='Welcome   User']").is_visible()
```

---

### 3.9 By Multiple Attributes — `and` / `or`

Combine multiple conditions for precise targeting.

**Syntax:**

- `//tag[@attr1='val1' and @attr2='val2']`
- `//tag[@attr1='val1' or @attr2='val2']`

```python
# HTML:
# <input type="text" name="username" class="form-control" />
# <input type="password" name="password" />
# <button type="submit" class="btn-primary">Login</button>

# AND — must match both conditions
page.locator("//input[@type='text' and @name='username']").fill("admin")
page.locator("//button[@type='submit' and @class='btn-primary']").click()

# AND with three conditions
page.locator("//input[@type='text' and @name='username' and @class='form-control']").fill("admin")

# OR — matches either condition
page.locator("//input[@type='text' or @type='email']").fill("user@mail.com")

# Combining AND and OR
page.locator("//input[(@type='text' or @type='email') and @class='form-control']").fill("hello")
```

---

### 3.10 By Index / Position

Select a **specific occurrence** of an element when multiple match.

**Syntax:** `(//tag)[index]` — index starts at **1**

```python
# HTML:
# <ul>
#   <li>Item One</li>
#   <li>Item Two</li>
#   <li>Item Three</li>
# </ul>

# Select 1st <li>
page.locator("(//li)[1]").click()

# Select 2nd <li>
page.locator("(//li)[2]").click()

# Select 3rd <li>
page.locator("(//li)[3]").click()

# Select 2nd input on the page
page.locator("(//input[@type='text'])[2]").fill("Second input")

# Get all matching elements count
items = page.locator("//li")
print(items.count())  # → 3
```

---

### 3.11 By `last()`

Select the **last matching** element in a node set.

**Syntax:** `(//tag)[last()]`

```python
# HTML:
# <tr><td>Row 1</td></tr>
# <tr><td>Row 2</td></tr>
# <tr><td>Row 3</td></tr>

# Select last <tr>
page.locator("(//tr)[last()]").click()

# Select second-to-last
page.locator("(//tr)[last()-1]").click()

# Last input field on the page
page.locator("(//input)[last()]").fill("Last field")
```

---

### 3.12 By Parent Navigation

Move **up to the parent** element from a child.

**Syntax:** `//child-tag[@attr='val']/..` or `//child-tag/parent::parent-tag`

```python
# HTML:
# <div class="form-group">
#   <label>Username</label>
#   <input id="username" type="text" />
# </div>

# Select parent <div> of the input with id='username'
page.locator("//input[@id='username']/..").get_attribute("class")
# Returns: "form-group"

# Using parent:: axis explicitly
page.locator("//input[@id='username']/parent::div").is_visible()

# Go up multiple levels
page.locator("//input[@id='username']/../..").get_attribute("id")

# Find the label inside the same parent as the input
page.locator("//input[@id='username']/../label").inner_text()
# Returns: "Username"
```

---

### 3.13 By Sibling Navigation — `following-sibling` / `preceding-sibling`

Navigate to **adjacent siblings** at the same DOM level.

**Syntax:**

- `//tag/following-sibling::sibling-tag`
- `//tag/preceding-sibling::sibling-tag`

```python
# HTML:
# <div>
#   <label>Email</label>
#   <input id="email" type="email" />
#   <span class="error-msg">Invalid email</span>
# </div>

# Get the error span AFTER the email input (following-sibling)
error = page.locator("//input[@id='email']/following-sibling::span")
print(error.inner_text())  # → "Invalid email"

# Get the label BEFORE the email input (preceding-sibling)
label = page.locator("//input[@id='email']/preceding-sibling::label")
print(label.inner_text())  # → "Email"

# Click the button that follows a specific heading
page.locator("//h2[text()='Confirm Order']/following-sibling::button").click()

# First following sibling
page.locator("//label/following-sibling::input[1]").fill("value")
```

---

### 3.14 By Ancestor Axis

Navigate **upward** through the DOM tree — more powerful than `..`

**Syntax:** `//tag/ancestor::ancestor-tag`

```python
# HTML:
# <form id="login-form">
#   <div class="wrapper">
#     <div class="field-group">
#       <input id="password" type="password" />
#     </div>
#   </div>
# </form>

# Get the closest ancestor <div>
page.locator("//input[@id='password']/ancestor::div[1]").get_attribute("class")
# Returns: "field-group"

# Get the ancestor <form>
page.locator("//input[@id='password']/ancestor::form").get_attribute("id")
# Returns: "login-form"

# Get ancestor with specific class
page.locator("//input[@id='password']/ancestor::div[@class='wrapper']").is_visible()
```

---

### 3.15 By Descendant Axis

Select **all descendant** elements (children, grandchildren, etc.).

**Syntax:** `//tag/descendant::descendant-tag`

```python
# HTML:
# <div id="container">
#   <section>
#     <article>
#       <p>Deep paragraph</p>
#     </article>
#   </section>
# </div>

# All <p> descendants of container
page.locator("//div[@id='container']/descendant::p").inner_text()
# Returns: "Deep paragraph"

# All <button> descendants in the main nav
buttons = page.locator("//nav[@id='main-nav']/descendant::button")
print(buttons.count())

# All inputs inside a specific form (descendant vs //)
page.locator("//form[@id='signup']/descendant::input").nth(0).fill("Alice")
```

---

### 3.16 By `following` / `preceding` Axes

Select **all** elements that appear after or before in the document (not just siblings).

**Syntax:**

- `//tag/following::other-tag`
- `//tag/preceding::other-tag`

```python
# HTML:
# <h2 id="section-a">Section A</h2>
# <p>Paragraph in A</p>
# <h2 id="section-b">Section B</h2>
# <button>Click Me</button>

# ALL elements after Section A heading
page.locator("//h2[@id='section-a']/following::p").inner_text()
# Returns: "Paragraph in A"

# First button that follows Section A
page.locator("//h2[@id='section-a']/following::button[1]").click()

# All elements before Section B
count = page.locator("//h2[@id='section-b']/preceding::p").count()
```

---

### 3.17 By Child Axis

Select **direct children** only (not grandchildren).

**Syntax:** `//tag/child::child-tag` or simply `//tag/child-tag`

```python
# HTML:
# <ul id="menu">
#   <li>Home</li>
#   <li>About</li>
#   <li><a><span>Contact</span></a></li>  ← span is grandchild
# </ul>

# Direct child <li> elements only
items = page.locator("//ul[@id='menu']/child::li")
print(items.count())  # → 3

# Equivalent shorthand
items = page.locator("//ul[@id='menu']/li")

# Direct child with text
page.locator("//ul[@id='menu']/li[text()='About']").click()
```

---

### 3.18 By Self Axis

Refers to the **current node itself**. Mostly used in complex predicates.

**Syntax:** `//tag/self::tag`

```python
# HTML:
# <input class="input-field active" type="text" />

# self:: used in compound expressions
page.locator("//input[self::input[@class='input-field active']]").fill("Hello")

# More practical: chained with other axes
page.locator("//div/child::input/self::input[@type='text']").fill("Direct input")
```

---

### 3.19 Wildcard XPath — `*`

The `*` wildcard matches **any element** regardless of tag name.

**Syntax:** `//*`, `//tag/*`, `//*/child`

```python
# HTML:
# <div id="box"><span>Hello</span></div>
# <section id="hero"><h1>Title</h1></section>

# Any element with id='box'
page.locator("//*[@id='box']").is_visible()

# Any direct child of a div
page.locator("//div[@id='box']/*").inner_text()  # → "Hello"

# Any element with class containing 'btn'
page.locator("//*[contains(@class, 'btn')]").first.click()

# Any element with text 'Submit'
page.locator("//*[text()='Submit']").click()

# Count all elements on page (rarely useful, but possible)
count = page.locator("//*").count()
```

---

### 3.20 XPath with Multiple Conditions

Combine attributes, text, axes, and functions.

```python
# HTML:
# <table>
#   <tr>
#     <td class="name">Alice</td>
#     <td class="role">Admin</td>
#     <td><button data-action="edit">Edit</button></td>
#   </tr>
# </table>

# Click "Edit" button in the row where name is "Alice"
page.locator(
    "//td[text()='Alice']/..//button[@data-action='edit']"
).click()

# Find a row containing BOTH text values
page.locator(
    "//tr[td[text()='Alice'] and td[text()='Admin']]"
).is_visible()

# Multi-condition with contains
page.locator(
    "//input[contains(@class,'form-control') and @type='email' and not(@disabled)]"
).fill("test@example.com")
```

---

### 3.21 XPath with `not()`

Exclude elements that match a certain condition.

**Syntax:** `//tag[not(@attribute)]` or `//tag[not(condition)]`

```python
# HTML:
# <input type="text" class="active" />
# <input type="text" class="active" disabled="true" />
# <input type="text" />

# Inputs that do NOT have disabled attribute
page.locator("//input[not(@disabled)]").first.fill("Enabled only")

# Inputs without a class attribute
page.locator("//input[@type='text' and not(@class)]").fill("No class input")

# Buttons that are NOT of type submit
page.locator("//button[not(@type='submit')]").first.click()

# Elements that do NOT contain certain text
page.locator("//li[not(contains(text(), 'Disabled'))]").first.click()
```

---

### 3.22 XPath with `count()`

Count child or descendant nodes as part of a condition.

**Syntax:** `//tag[count(child::*)=N]`

```python
# HTML:
# <ul>
#   <li>One</li>
#   <li>Two</li>
# </ul>
# <ul>
#   <li>A</li><li>B</li><li>C</li>
# </ul>

# Select the <ul> that has exactly 3 <li> children
page.locator("//ul[count(li)=3]").is_visible()

# Select <tr> rows that have exactly 4 <td> cells
rows = page.locator("//tr[count(td)=4]")
print(rows.count())

# Assert a form has exactly 3 inputs
assert page.locator("//form[count(.//input)=3]").count() == 1
```

---

### 3.23 XPath with `string-length()`

Match elements based on the **length** of their text or attribute value.

**Syntax:** `//tag[string-length(text())>N]`

```python
# HTML:
# <p>Hi</p>
# <p>This is a longer paragraph with more content.</p>
# <input value="ok" />
# <input value="verylongvalue" />

# Elements with text longer than 10 characters
page.locator("//p[string-length(text())>10]").inner_text()
# Returns: "This is a longer paragraph with more content."

# Inputs with value attribute shorter than 5 characters
page.locator("//input[string-length(@value)<5]").get_attribute("value")
# Returns: "ok"

# Paragraphs with non-empty text
page.locator("//p[string-length(normalize-space(text()))>0]").count()
```

---

### 3.24 Dynamic XPath

Build XPath expressions **dynamically** at runtime using Python f-strings.

```python
def get_table_cell(page, row_name: str, col_index: int):
    """Click a specific cell in a table by row label and column index."""
    xpath = f"//tr[td[text()='{row_name}']]/td[{col_index}]"
    return page.locator(xpath)

def click_menu_item(page, menu_text: str):
    """Click a navigation item by its text."""
    xpath = f"//nav//a[contains(text(), '{menu_text}')]"
    page.locator(xpath).click()

def get_row_action_button(page, row_identifier: str, action: str):
    """Click an action button in a specific data table row."""
    xpath = f"//tr[contains(., '{row_identifier}')]//button[@data-action='{action}']"
    page.locator(xpath).click()


# Usage examples:
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/dashboard")

    # Dynamic usage
    click_menu_item(page, "Reports")
    get_row_action_button(page, "Invoice #001", "view")

    cell = get_table_cell(page, "Alice", 3)
    print(cell.inner_text())

    browser.close()
```

---

### 3.25 XPath inside Frames / iFrames

When elements live inside `<iframe>`, you must **scope to the frame first**, then use XPath.

```python
# HTML:
# <iframe id="payment-frame" src="/payment">
#   <!-- Inside iframe: -->
#   <input id="card-number" type="text" />
#   <button>Pay Now</button>
# </iframe>

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://shop.example.com/checkout")

    # Locate the frame first
    frame = page.frame_locator("//iframe[@id='payment-frame']")

    # Now use XPath INSIDE the frame
    frame.locator("//input[@id='card-number']").fill("4111111111111111")
    frame.locator("//button[text()='Pay Now']").click()

    # Nested iframes
    outer_frame = page.frame_locator("//iframe[@name='outer']")
    inner_frame = outer_frame.frame_locator("//iframe[@name='inner']")
    inner_frame.locator("//input[@type='text']").fill("nested value")

    browser.close()
```

---

## 4. Using XPath with Playwright APIs

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")

    locator = page.locator("//button[@id='submit']")

    # ── Actions ──────────────────────────────────────────
    locator.click()                          # Click
    locator.dblclick()                       # Double-click
    locator.right_click()                    # Right-click
    locator.hover()                          # Hover
    locator.fill("text")                     # Fill input
    locator.type("text", delay=50)           # Type with delay
    locator.clear()                          # Clear input
    locator.press("Enter")                   # Press key
    locator.select_option("value")           # Select dropdown
    locator.check()                          # Check checkbox
    locator.uncheck()                        # Uncheck checkbox
    locator.tap()                            # Tap (mobile)
    locator.focus()                          # Focus element
    locator.scroll_into_view_if_needed()     # Scroll to element

    # ── Queries ──────────────────────────────────────────
    locator.inner_text()                     # Visible text
    locator.text_content()                   # Full text (incl. hidden)
    locator.inner_html()                     # Inner HTML
    locator.input_value()                    # Input value
    locator.get_attribute("href")            # Get attribute
    locator.count()                          # Count matches

    # ── State Checks ─────────────────────────────────────
    locator.is_visible()                     # Is visible?
    locator.is_hidden()                      # Is hidden?
    locator.is_enabled()                     # Is enabled?
    locator.is_disabled()                    # Is disabled?
    locator.is_checked()                     # Is checked?

    # ── Assertions ───────────────────────────────────────
    from playwright.sync_api import expect
    expect(locator).to_be_visible()
    expect(locator).to_have_text("Submit")
    expect(locator).to_have_attribute("type", "submit")
    expect(locator).to_be_enabled()
    expect(locator).to_have_count(1)

    # ── Multiple Elements ────────────────────────────────
    items = page.locator("//li")
    print(items.count())                     # Count
    items.nth(0).click()                     # Access by index (0-based)
    items.first.click()                      # First item
    items.last.click()                       # Last item
    for i in range(items.count()):
        print(items.nth(i).inner_text())     # Iterate

    browser.close()
```

---

## 5. Chaining XPath with Playwright Locators

Playwright allows chaining locators for more precise targeting.

```python
# HTML:
# <section id="products">
#   <div class="product-card">
#     <h3>Laptop Pro</h3>
#     <button class="add-to-cart">Add to Cart</button>
#   </div>
#   <div class="product-card">
#     <h3>Phone X</h3>
#     <button class="add-to-cart">Add to Cart</button>
#   </div>
# </section>

# Chain: first find the section, then find inside it
section = page.locator("//section[@id='products']")
laptop_card = section.locator("//div[.//h3[text()='Laptop Pro']]")
laptop_card.locator("//button[contains(@class,'add-to-cart')]").click()

# Chain XPath with filter()
page.locator("//div[@class='product-card']").filter(
    has=page.locator("//h3[text()='Phone X']")
).locator("//button").click()

# Combine XPath with CSS
page.locator("//section[@id='products']").locator(".product-card").nth(1).click()
```

---

## 6. XPath vs Other Locators

| Strategy         | Syntax Example                              | Speed   | Reliability | Best Use Case                    |
| ---------------- | ------------------------------------------- | ------- | ----------- | -------------------------------- |
| **XPath**        | `//input[@id='email']`                      | Medium  | High        | Complex DOM, relationships       |
| **CSS Selector** | `input#email`                               | Fast    | High        | Simple attribute/class selection |
| **ID**           | `page.locator("#email")`                    | Fastest | High        | Unique elements with stable IDs  |
| **Text**         | `page.get_by_text("Submit")`                | Fast    | Medium      | Static text labels               |
| **Role**         | `page.get_by_role("button", name="Submit")` | Fast    | Highest     | Accessibility-first testing      |
| **Label**        | `page.get_by_label("Email")`                | Fast    | High        | Form inputs with labels          |
| **Placeholder**  | `page.get_by_placeholder("Enter email")`    | Fast    | Medium      | Inputs with placeholders         |
| **Test ID**      | `page.get_by_test_id("submit-btn")`         | Fastest | Highest     | `data-testid` attribute          |

> ✅ **When to choose XPath:** Use XPath when you need to navigate DOM relationships (parent, sibling, ancestor), use string functions, or handle dynamic attributes that CSS selectors can't express.

---

## 7. Best Practices

```python
# ✅ DO: Use relative XPath
page.locator("//input[@id='username']")

# ✅ DO: Use data-testid when available
page.locator("//*[@data-testid='login-button']")

# ✅ DO: Use contains() for dynamic classes
page.locator("//button[contains(@class, 'submit')]")

# ✅ DO: Combine axes for table interactions
page.locator("//tr[td[text()='Alice']]/td[3]")

# ✅ DO: Use normalize-space() for whitespace-heavy text
page.locator("//button[normalize-space()='Save Changes']")

# ✅ DO: Store locators in variables/page objects
login_btn = page.locator("//button[@id='login']")
login_btn.click()

# ✅ DO: Use expect() for assertions instead of is_visible()
expect(page.locator("//div[@class='success-msg']")).to_be_visible()

# ❌ DON'T: Use absolute XPath
page.locator("/html/body/div[2]/form/input[1]")

# ❌ DON'T: Use fragile index-based XPath as primary strategy
page.locator("(//button)[4]")  # breaks when UI changes

# ❌ DON'T: Use overly complex XPath when simpler alternatives exist
page.locator("//div[contains(@class,'nav')]/ul/li[1]/a/span[2]")  # fragile
```

---

## 8. Common Mistakes & Fixes

### Mistake 1: Forgetting parentheses for indexing

```python
# ❌ WRONG — indexes the child, not the matched set
page.locator("//button[1]")  # 1st button child of parent

# ✅ CORRECT — indexes the entire matched result set
page.locator("(//button)[1]")  # 1st button anywhere on page
```

### Mistake 2: Exact text match fails due to whitespace

```python
# ❌ Fails if button has extra spaces
page.locator("//button[text()='Submit']")

# ✅ Use normalize-space()
page.locator("//button[normalize-space()='Submit']")
```

### Mistake 3: Class attribute partial match

```python
# ❌ Fails if class is "btn btn-primary btn-lg"
page.locator("//button[@class='btn-primary']")

# ✅ Use contains()
page.locator("//button[contains(@class,'btn-primary')]")
```

### Mistake 4: Forgetting frame context for iframes

```python
# ❌ Won't find element inside an iframe
page.locator("//input[@id='card']").fill("1234")

# ✅ Scope to the frame first
page.frame_locator("//iframe").locator("//input[@id='card']").fill("1234")
```

### Mistake 5: Using `//` when you mean direct child

```python
# Selects ALL descendant inputs (unintended)
page.locator("//form//input")

# ✅ Direct children only
page.locator("//form/input")
```

---

## Quick Reference Cheat Sheet

| XPath Pattern                        | Description               |
| ------------------------------------ | ------------------------- |
| `//tag`                              | Any element with tag      |
| `//tag[@attr='val']`                 | By attribute              |
| `//tag[text()='text']`               | By exact text             |
| `//tag[contains(text(),'part')]`     | By partial text           |
| `//tag[contains(@attr,'part')]`      | By partial attribute      |
| `//tag[starts-with(@attr,'prefix')]` | Attribute starts with     |
| `//tag[normalize-space()='text']`    | Trimmed text match        |
| `//tag[@a='v1' and @b='v2']`         | Multiple attributes (AND) |
| `//tag[@a='v1' or @b='v2']`          | Multiple attributes (OR)  |
| `(//tag)[n]`                         | nth occurrence (1-based)  |
| `(//tag)[last()]`                    | Last occurrence           |
| `//tag/..`                           | Parent element            |
| `//tag/following-sibling::sibling`   | Next sibling              |
| `//tag/preceding-sibling::sibling`   | Previous sibling          |
| `//tag/ancestor::ancestor`           | Any ancestor              |
| `//tag/descendant::desc`             | Any descendant            |
| `//*`                                | Any element               |
| `//tag[not(@attr)]`                  | Element without attribute |
| `//tag[count(child)=n]`              | Element with n children   |
| `//tag[string-length(text())>n]`     | Text length condition     |

---

_Generated with Python Playwright XPath Locators Guide — covering 25 strategies with production-ready examples._
