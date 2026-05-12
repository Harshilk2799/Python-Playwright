# Python Playwright — CSS Locators: Complete In-Depth Guide

> **Everything you need to know about CSS Locators in Playwright for Python — all methods, selectors, and real-world examples.**

---

## Table of Contents

- [Python Playwright — CSS Locators: Complete In-Depth Guide](#python-playwright--css-locators-complete-in-depth-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What Are CSS Locators?](#1-what-are-css-locators)
  - [2. Basic Tag / Element Selector](#2-basic-tag--element-selector)
    - [Syntax](#syntax)
    - [Examples](#examples)
  - [3. ID Selector](#3-id-selector)
    - [Syntax](#syntax-1)
    - [Examples](#examples-1)
  - [4. Class Selector](#4-class-selector)
    - [Syntax](#syntax-2)
    - [Examples](#examples-2)
  - [5. Attribute Selector](#5-attribute-selector)
    - [Syntax](#syntax-3)
    - [Examples](#examples-3)
  - [6. Attribute Value Variants](#6-attribute-value-variants)
    - [Syntax Table](#syntax-table)
    - [Examples](#examples-4)
  - [7. Descendant Combinator (space)](#7-descendant-combinator-space)
    - [Syntax](#syntax-4)
    - [Examples](#examples-5)
  - [8. Child Combinator (`>`)](#8-child-combinator-)
    - [Syntax](#syntax-5)
    - [Examples](#examples-6)
  - [9. Adjacent Sibling Combinator (`+`)](#9-adjacent-sibling-combinator-)
    - [Syntax](#syntax-6)
    - [Examples](#examples-7)
  - [10. General Sibling Combinator (`~`)](#10-general-sibling-combinator-)
    - [Syntax](#syntax-7)
    - [Examples](#examples-8)
  - [11. Grouping Selectors (`,`)](#11-grouping-selectors-)
    - [Syntax](#syntax-8)
    - [Examples](#examples-9)
  - [12. Pseudo-class Selectors](#12-pseudo-class-selectors)
    - [Common State Pseudo-classes](#common-state-pseudo-classes)
  - [13. Structural Pseudo-classes](#13-structural-pseudo-classes)
  - [14. Playwright-specific `:has()` Pseudo-class](#14-playwright-specific-has-pseudo-class)
    - [Syntax](#syntax-9)
    - [Examples](#examples-10)
  - [15. Playwright-specific `:has-text()` Pseudo-class](#15-playwright-specific-has-text-pseudo-class)
    - [Syntax](#syntax-10)
    - [Examples](#examples-11)
  - [16. Playwright-specific `:is()` Pseudo-class](#16-playwright-specific-is-pseudo-class)
    - [Syntax](#syntax-11)
    - [Examples](#examples-12)
  - [17. `:not()` Pseudo-class](#17-not-pseudo-class)
    - [Syntax](#syntax-12)
    - [Examples](#examples-13)
  - [18. Chaining Multiple CSS Selectors](#18-chaining-multiple-css-selectors)
    - [Examples](#examples-14)
  - [19. `nth-child` \& `nth-of-type`](#19-nth-child--nth-of-type)
    - [Syntax](#syntax-13)
    - [`n` can be:](#n-can-be)
    - [Examples](#examples-15)
  - [20. Universal Selector (`*`)](#20-universal-selector-)
    - [Examples](#examples-16)
  - [21. CSS Inside Frames / iFrames](#21-css-inside-frames--iframes)
    - [Examples](#examples-17)
  - [22. CSS with Shadow DOM](#22-css-with-shadow-dom)
    - [Examples](#examples-18)
  - [23. CSS Locator with `filter()`](#23-css-locator-with-filter)
    - [Examples](#examples-19)
  - [24. CSS Locator with `nth()`](#24-css-locator-with-nth)
    - [Examples](#examples-20)
  - [25. Real-World Cheat Sheet](#25-real-world-cheat-sheet)
  - [26. Best Practices](#26-best-practices)
  - [Summary of All CSS Selector Types](#summary-of-all-css-selector-types)

---

## 1. What Are CSS Locators?

CSS Locators use **CSS selector syntax** to find elements on a web page. In Playwright (Python), you pass CSS selectors to `page.locator()`, `page.query_selector()`, or any locator chaining method.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")

    # Generic CSS locator usage
    element = page.locator("css=button")   # explicit prefix (optional)
    element = page.locator("button")       # implicit CSS (Playwright default)
```

> **Note:** Playwright treats any selector that is not prefixed as a **CSS selector by default**. You can also prefix with `css=` explicitly.

---

## 2. Basic Tag / Element Selector

Select elements by their **HTML tag name**.

### Syntax

```
tagname
```

### Examples

```python
# Click the first <button> on the page
page.locator("button").first.click()

# Get all <a> (anchor/link) elements
links = page.locator("a").all()
for link in links:
    print(link.inner_text())

# Fill the first <input> field
page.locator("input").first.fill("Hello")

# Get text of all <h1> headings
headings = page.locator("h1").all()
for h in headings:
    print(h.inner_text())

# Click a <submit> type via tag
page.locator("form").locator("button").click()
```

---

## 3. ID Selector

Select an element by its **unique `id` attribute**. IDs should be unique per page.

### Syntax

```
#id-value
```

### Examples

```python
# Click a button with id="submit-btn"
page.locator("#submit-btn").click()

# Fill an input with id="username"
page.locator("#username").fill("john_doe")

# Fill password field
page.locator("#password").fill("secret123")

# Check a checkbox with id="agree"
page.locator("#agree").check()

# Get text of element with id="welcome-msg"
text = page.locator("#welcome-msg").inner_text()
print(text)

# Select a dropdown by id
page.locator("#country").select_option("India")
```

---

## 4. Class Selector

Select elements by their **CSS class name**. Multiple elements can share the same class.

### Syntax

```
.class-name
```

### Examples

```python
# Click a button with class="btn-primary"
page.locator(".btn-primary").click()

# Count all error messages
error_count = page.locator(".error-message").count()
print(f"Errors found: {error_count}")

# Get all items in a list
items = page.locator(".list-item").all()
for item in items:
    print(item.inner_text())

# Multiple classes — element must have BOTH classes
page.locator(".btn.btn-danger").click()

# Nested class selector
page.locator(".modal .close-btn").click()

# Hover over a nav item
page.locator(".nav-item").hover()
```

---

## 5. Attribute Selector

Select elements by **any HTML attribute** and its value.

### Syntax

```
[attribute]              → has the attribute (any value)
[attribute="value"]      → exact match
```

### Examples

```python
# Select any element that has a 'placeholder' attribute
page.locator("[placeholder]").first.fill("test")

# Select input with exact placeholder text
page.locator("[placeholder='Enter your email']").fill("user@example.com")

# Select by name attribute
page.locator("[name='username']").fill("admin")

# Select by type attribute
page.locator("[type='submit']").click()
page.locator("[type='checkbox']").first.check()
page.locator("[type='radio']").first.check()

# Select by data-* attribute
page.locator("[data-testid='login-button']").click()
page.locator("[data-cy='search-input']").fill("playwright")

# Select by aria attributes
page.locator("[aria-label='Close dialog']").click()
page.locator("[aria-expanded='true']").click()

# Select by href attribute
page.locator("[href='/home']").click()

# Select by disabled attribute
disabled_btn = page.locator("[disabled]")
print(disabled_btn.is_disabled())
```

---

## 6. Attribute Value Variants

CSS provides **partial matching** for attribute values — very powerful for dynamic content.

### Syntax Table

| Selector         | Description                        |
| ---------------- | ---------------------------------- |
| `[attr^="val"]`  | Starts with `val`                  |
| `[attr$="val"]`  | Ends with `val`                    |
| `[attr*="val"]`  | Contains `val` anywhere            |
| `[attr~="val"]`  | Contains `val` as a whole word     |
| `[attr\|="val"]` | Equals `val` or starts with `val-` |

### Examples

```python
# Starts with — href starts with "/product"
page.locator("[href^='/product']").first.click()

# Ends with — src ends with ".png"
images = page.locator("[src$='.png']").all()
print(f"PNG images: {len(images)}")

# Contains — class contains "active"
page.locator("[class*='active']").click()

# Contains word — class contains standalone word "btn"
page.locator("[class~='btn']").click()

# Starts with or equals with dash
page.locator("[lang|='en']").inner_text()

# Combine: input whose name contains "email"
page.locator("input[name*='email']").fill("test@test.com")

# Link whose href starts with "https"
secure_links = page.locator("a[href^='https']").all()
```

---

## 7. Descendant Combinator (space)

Select elements that are **anywhere inside** a parent element (any depth).

### Syntax

```
parent descendant
```

### Examples

```python
# Any <a> tag inside a <nav>
page.locator("nav a").first.click()

# Any <input> inside a <form>
page.locator("form input").first.fill("data")

# Any <li> inside a <ul> with class "menu"
items = page.locator("ul.menu li").all()
for item in items:
    print(item.inner_text())

# Button inside a div with id "actions"
page.locator("#actions button").click()

# Deep descendant — span inside p inside article
page.locator("article p span").inner_text()

# Label inside a form group
page.locator(".form-group label").inner_text()
```

---

## 8. Child Combinator (`>`)

Select elements that are **direct children** only (not deeper descendants).

### Syntax

```
parent > direct-child
```

### Examples

```python
# Direct <li> children of <ul id="main-menu">
page.locator("ul#main-menu > li").first.click()

# Direct <input> children of a <form>
page.locator("form > input").first.fill("direct only")

# Direct <div> children of a container
direct_divs = page.locator(".container > div").all()
print(f"Direct divs: {len(direct_divs)}")

# Direct <button> in a card footer
page.locator(".card > .card-footer > button").click()

# Only top-level <p> inside article (not nested)
top_paragraphs = page.locator("article > p").all()
for p in top_paragraphs:
    print(p.inner_text())
```

---

## 9. Adjacent Sibling Combinator (`+`)

Select an element that is the **immediately next sibling** of a specified element.

### Syntax

```
element + adjacent-sibling
```

### Examples

```python
# <p> that immediately follows an <h2>
page.locator("h2 + p").inner_text()

# <input> that immediately follows a <label>
page.locator("label + input").fill("value")

# Error message <span> after an <input>
page.locator("input + .error-msg").inner_text()

# Button immediately after a form group
page.locator(".form-group + button").click()

# <li> immediately after the first <li>
page.locator("li + li").first.inner_text()
```

---

## 10. General Sibling Combinator (`~`)

Select **all siblings** that follow a specified element (not just the immediate next one).

### Syntax

```
element ~ all-following-siblings
```

### Examples

```python
# All <p> elements that follow an <h2>
paras = page.locator("h2 ~ p").all()
for p in paras:
    print(p.inner_text())

# All <li> after the first <li> with class "active"
page.locator("li.active ~ li").first.click()

# All inputs after a label
inputs = page.locator("label ~ input").all()
print(f"Inputs after labels: {len(inputs)}")

# All divs after a separator
page.locator(".separator ~ div").first.inner_text()
```

---

## 11. Grouping Selectors (`,`)

Apply the **same action to multiple selectors** at once.

### Syntax

```
selector1, selector2, selector3
```

### Examples

```python
# Count all headings (h1, h2, h3)
all_headings = page.locator("h1, h2, h3").all()
print(f"Total headings: {len(all_headings)}")

# Select all button types
all_buttons = page.locator("button, input[type='submit'], input[type='button']").all()

# Check visibility of success or error banners
banner = page.locator(".success-banner, .error-banner")
print(banner.is_visible())

# Click whichever of these exists first
page.locator("#ok-btn, #confirm-btn, .accept").first.click()
```

---

## 12. Pseudo-class Selectors

Pseudo-classes select elements based on their **state or position**.

### Common State Pseudo-classes

```python
# :hover — elements under cursor (mainly for triggering)
page.locator("button:hover")  # Use .hover() method instead for actions

# :focus — currently focused element
page.locator("input:focus").fill("typing here")

# :checked — checked checkboxes/radio buttons
checked_boxes = page.locator("input[type='checkbox']:checked").all()
print(f"Checked: {len(checked_boxes)}")

# :disabled — disabled form elements
disabled_inputs = page.locator("input:disabled").all()

# :enabled — enabled form elements
enabled_inputs = page.locator("input:enabled").all()

# :required — required form fields
required_fields = page.locator("input:required").all()

# :optional — optional form fields
optional_fields = page.locator("input:optional").all()

# :valid — valid form fields (after user input)
page.locator("input:valid").all()

# :invalid — invalid form fields
page.locator("input:invalid").all()

# :read-only — read-only inputs
page.locator("input:read-only").inner_text()

# :placeholder-shown — input showing placeholder (empty)
empty_inputs = page.locator("input:placeholder-shown").all()
```

---

## 13. Structural Pseudo-classes

Select elements based on their **position within the DOM tree**.

```python
# :first-child — first child of its parent
page.locator("li:first-child").inner_text()

# :last-child — last child of its parent
page.locator("li:last-child").click()

# :first-of-type — first element of its type
page.locator("p:first-of-type").inner_text()

# :last-of-type — last element of its type
page.locator("p:last-of-type").inner_text()

# :only-child — only child of its parent
page.locator("div:only-child").inner_text()

# :only-of-type — only element of that type in parent
page.locator("img:only-of-type").get_attribute("alt")

# :empty — elements with no children or text
empty_divs = page.locator("div:empty").all()

# :root — the root <html> element
page.locator(":root").get_attribute("lang")
```

---

## 14. Playwright-specific `:has()` Pseudo-class

Select a **parent element** that **contains** a specific child. This is a Playwright/CSS4 extension.

### Syntax

```
parent:has(child-selector)
```

### Examples

```python
# Select a <tr> that contains a <td> with class "active"
page.locator("tr:has(td.active)").click()

# Select a <div> that contains an <input>
page.locator("div:has(input)").first.inner_text()

# Select a card that has an "Out of Stock" badge
page.locator(".product-card:has(.badge-out-of-stock)").all()

# Select a form group that has an error span
error_groups = page.locator(".form-group:has(.error)").all()
for group in error_groups:
    print(group.inner_text())

# Select a list item that contains a link to /dashboard
page.locator("li:has(a[href='/dashboard'])").inner_text()

# Select a row that has a delete button
rows_with_delete = page.locator("tr:has(button.delete-btn)").all()
print(f"Deletable rows: {len(rows_with_delete)}")

# Select nav item that contains active link
page.locator(".nav-item:has(a.active)").inner_text()
```

---

## 15. Playwright-specific `:has-text()` Pseudo-class

Select elements that **contain specific visible text**. This is a Playwright extension.

### Syntax

```
element:has-text("text")
```

### Examples

```python
# Click a button that says "Submit"
page.locator("button:has-text('Submit')").click()

# Click any element containing "Sign In"
page.locator(":has-text('Sign In')").first.click()

# Select a specific menu item by text
page.locator(".nav-item:has-text('Products')").click()

# Select a table row containing "John Doe"
page.locator("tr:has-text('John Doe')").click()

# Assert a success message is visible
page.locator(".toast:has-text('Success')").wait_for()

# Select the card that contains "Premium Plan"
page.locator(".pricing-card:has-text('Premium Plan')").click()

# Click the tab labeled "Settings"
page.locator(".tab:has-text('Settings')").click()

# Partial text match works too
page.locator("p:has-text('Welcome')").inner_text()
```

---

## 16. Playwright-specific `:is()` Pseudo-class

Match any element that matches **one of a list of selectors**. Useful to avoid repetition.

### Syntax

```
:is(selector1, selector2, ...)
```

### Examples

```python
# Select any heading level
headings = page.locator(":is(h1, h2, h3, h4, h5, h6)").all()
for h in headings:
    print(h.inner_text())

# Select any type of button
page.locator(":is(button, input[type='submit'], a.btn)").first.click()

# Select active or selected items
active_items = page.locator("li:is(.active, .selected)").all()

# Inside a form — any interactive field
fields = page.locator("form :is(input, select, textarea)").all()
print(f"Form fields: {len(fields)}")

# Any error or warning element
alerts = page.locator(":is(.error, .warning, .alert-danger)").all()
```

---

## 17. `:not()` Pseudo-class

Select elements that **do NOT match** a given selector.

### Syntax

```
element:not(selector)
```

### Examples

```python
# All buttons except disabled ones
active_buttons = page.locator("button:not([disabled])").all()

# All inputs except hidden
visible_inputs = page.locator("input:not([type='hidden'])").all()

# All list items except the active one
other_items = page.locator("li:not(.active)").all()

# All links except external
internal_links = page.locator("a:not([href^='http'])").all()

# All rows except the header row
data_rows = page.locator("tr:not(.header-row)").all()

# All divs that are not modals
page.locator("div:not(.modal)").first.inner_text()

# Input not of type submit or reset
page.locator("input:not([type='submit']):not([type='reset'])").first.fill("data")
```

---

## 18. Chaining Multiple CSS Selectors

Combine **tag + id + class + attribute** in a single selector for precision.

### Examples

```python
# Tag + class
page.locator("button.primary").click()

# Tag + id
page.locator("input#email").fill("user@email.com")

# Tag + class + attribute
page.locator("input.form-control[type='email']").fill("user@email.com")

# Tag + multiple classes
page.locator("div.card.card-shadow").first.inner_text()

# Class + attribute
page.locator(".btn[data-action='delete']").click()

# Tag + class + pseudo-class
page.locator("input.form-control:not([disabled])").first.fill("active input")

# Full chain: tag + id + class + attribute + pseudo
page.locator("form#login-form input.form-control[type='password']:enabled").fill("pass123")

# Parent > child with class
page.locator("table.data-table > tbody > tr").first.click()
```

---

## 19. `nth-child` & `nth-of-type`

Select elements by their **numeric position** in the DOM.

### Syntax

```
:nth-child(n)
:nth-of-type(n)
:nth-last-child(n)
:nth-last-of-type(n)
```

### `n` can be:

- A number: `2` → 2nd element
- `odd` → 1st, 3rd, 5th...
- `even` → 2nd, 4th, 6th...
- A formula: `3n` → every 3rd, `2n+1` → odd

### Examples

```python
# 2nd list item
page.locator("li:nth-child(2)").inner_text()

# 3rd row in a table body
page.locator("tbody tr:nth-child(3)").click()

# Every even row (zebra striping check)
even_rows = page.locator("tr:nth-child(even)").all()

# Every odd row
odd_rows = page.locator("tr:nth-child(odd)").all()

# Every 3rd item
page.locator("li:nth-child(3n)").all()

# 2nd <p> among all p elements (not just siblings of same type)
page.locator("p:nth-of-type(2)").inner_text()

# Last list item
page.locator("li:last-child").click()

# Second-to-last table row
page.locator("tr:nth-last-child(2)").inner_text()

# First 3 items using formula
page.locator("li:nth-child(-n+3)").all()  # 1st, 2nd, 3rd
```

---

## 20. Universal Selector (`*`)

The `*` selector matches **every element**. Use carefully — very broad.

### Examples

```python
# All elements inside a container
all_elements = page.locator(".container *").all()
print(f"Elements in container: {len(all_elements)}")

# First element of any type inside a form
page.locator("form > *").first.inner_text()

# Any direct child of the body
page.locator("body > *").first.inner_text()

# All elements with data-testid (any tag)
page.locator("*[data-testid]").all()

# Combine: any element that is not a script or style
# (usually handled differently, but shows * usage)
page.locator("main *").count()
```

---

## 21. CSS Inside Frames / iFrames

Playwright handles iframes via `.frame_locator()`, and CSS selectors work inside them.

### Examples

```python
# Locate an element inside an iframe by its CSS selector
frame = page.frame_locator("iframe#payment-frame")
frame.locator("input[name='card-number']").fill("4111111111111111")

# Using CSS to locate the iframe itself, then elements inside
frame = page.frame_locator("iframe.checkout-iframe")
frame.locator("#cvv").fill("123")
frame.locator("button[type='submit']").click()

# Nested iframes
outer = page.frame_locator("iframe#outer")
inner = outer.frame_locator("iframe#inner")
inner.locator(".target-element").click()

# Multiple iframes — select by index
frame = page.frame_locator("iframe").nth(0)
frame.locator("input.username").fill("admin")
```

---

## 22. CSS with Shadow DOM

Playwright can pierce Shadow DOM with `>>` (legacy) or by using `locator()` with `pierce` option. For open shadow roots, `page.locator()` can pierce automatically.

### Examples

```python
# Playwright auto-pierces open shadow DOM in modern versions
page.locator("my-custom-element input").fill("pierced shadow DOM")

# Using shadow piercing explicitly (Playwright CSS extension)
page.locator("css=my-component >> css=.internal-button").click()

# Shadow host → shadow content
page.locator("user-card").locator("button.edit").click()

# Deep shadow pierce
page.locator("app-root shop-cart cart-item button.remove").click()
```

---

## 23. CSS Locator with `filter()`

Use Playwright's `.filter()` method **on top of CSS locators** for powerful narrowing.

### Examples

```python
# Filter buttons by text after CSS selection
page.locator("button").filter(has_text="Delete").click()

# Filter rows that contain a specific cell value
page.locator("tr").filter(has_text="John").click()

# Filter items that have a child with class "badge"
page.locator(".list-item").filter(has=page.locator(".badge")).all()

# Filter input fields that are visible
page.locator("input").filter(has=page.locator(":visible")).first.fill("data")

# Combined: CSS + filter for precision
page.locator(".product-card") \
    .filter(has_text="In Stock") \
    .locator("button.add-to-cart") \
    .click()

# Filter rows that contain a "Pending" status
pending_rows = page.locator("tbody tr").filter(has_text="Pending").all()
print(f"Pending orders: {len(pending_rows)}")
```

---

## 24. CSS Locator with `nth()`

Playwright's `.nth()` method selects the **nth match** from a CSS locator result (0-indexed).

### Examples

```python
# Select the 1st match (index 0)
page.locator("button.btn").nth(0).click()

# Select the 2nd match (index 1)
page.locator("tr").nth(1).inner_text()

# Select the last match
page.locator("li").last.click()

# Select the first match
page.locator("a").first.click()

# Iterate with nth
count = page.locator(".product").count()
for i in range(count):
    name = page.locator(".product").nth(i).locator(".product-name").inner_text()
    print(name)

# Combined with filter
page.locator(".tab").filter(has_text="Active").nth(0).click()
```

---

## 25. Real-World Cheat Sheet

```python
# ━━━ Login Form ━━━
page.locator("#username").fill("admin")
page.locator("#password").fill("password123")
page.locator("button[type='submit']").click()

# ━━━ Navigation ━━━
page.locator("nav > ul > li:nth-child(3) > a").click()
page.locator(".navbar .nav-link:has-text('Products')").click()

# ━━━ Table Operations ━━━
# Get 3rd row, 2nd cell
cell = page.locator("table tbody tr:nth-child(3) td:nth-child(2)").inner_text()

# Click Edit in the row containing "Alice"
page.locator("tr:has-text('Alice') button:has-text('Edit')").click()

# Count total rows
row_count = page.locator("table tbody tr").count()

# ━━━ Form Validation ━━━
# Check which fields are invalid
invalid = page.locator("input:invalid").all()

# Get all error messages
errors = page.locator(".error-message, .field-error, [role='alert']").all()
for e in errors:
    print(e.inner_text())

# ━━━ Dynamic Content ━━━
# Wait for a success toast
page.locator(".toast:has-text('Success')").wait_for()

# Wait for a loader to disappear
page.locator(".loading-spinner").wait_for(state="hidden")

# ━━━ Dropdowns ━━━
page.locator("select#country").select_option("IN")
page.locator(".custom-select:has-text('Choose')").click()
page.locator(".dropdown-menu > li:has-text('India')").click()

# ━━━ Checkboxes & Radios ━━━
page.locator("input[type='checkbox']#terms").check()
page.locator("input[type='radio'][value='male']").check()

# ━━━ File Upload ━━━
page.locator("input[type='file']").set_input_files("path/to/file.pdf")

# ━━━ Pagination ━━━
page.locator(".pagination > li:last-child > a").click()
page.locator(".page-item:has-text('Next')").click()
```

---

## 26. Best Practices

| Tip                                               | Why                                                   |
| ------------------------------------------------- | ----------------------------------------------------- |
| Prefer `[data-testid]` attributes                 | Stable, not affected by style changes                 |
| Avoid over-specificity (`div > div > div > span`) | Brittle — breaks on layout changes                    |
| Use `:has-text()` for dynamic buttons             | More readable and intent-clear than brittle nth-child |
| Combine CSS with `.filter()`                      | Cleaner than huge CSS chains                          |
| Avoid universal `*` in large pages                | Performance cost and fragility                        |
| Use `[aria-label]` for accessibility elements     | More robust and semantic                              |
| Prefer `.first` / `.last` over `:nth-child(1)`    | Playwright-native, cleaner syntax                     |
| Use `page.locator()` over `page.query_selector()` | Locators are lazy and auto-retrying                   |

---

## Summary of All CSS Selector Types

| Selector Type   | Syntax Example                   | Description            |
| --------------- | -------------------------------- | ---------------------- |
| Tag             | `button`                         | By HTML tag            |
| ID              | `#login-btn`                     | By unique ID           |
| Class           | `.primary`                       | By class name          |
| Attribute       | `[type='email']`                 | By attribute           |
| Starts with     | `[href^='/']`                    | Attr starts with       |
| Ends with       | `[src$='.png']`                  | Attr ends with         |
| Contains        | `[class*='active']`              | Attr contains          |
| Descendant      | `form input`                     | Inside parent          |
| Child           | `ul > li`                        | Direct child           |
| Adjacent        | `label + input`                  | Next sibling           |
| General sibling | `h2 ~ p`                         | All following siblings |
| Grouping        | `h1, h2, h3`                     | Multiple selectors     |
| Pseudo-state    | `:checked`, `:disabled`          | State-based            |
| Structural      | `:nth-child(2)`                  | Position-based         |
| `:has()`        | `tr:has(td.error)`               | Parent with child      |
| `:has-text()`   | `button:has-text('OK')`          | Contains text          |
| `:is()`         | `:is(h1,h2,h3)`                  | Matches any of         |
| `:not()`        | `button:not(:disabled)`          | Excludes match         |
| Universal       | `*`                              | All elements           |
| Chain           | `input.cls[type]:not(:disabled)` | Combined               |

---

_Generated for Python Playwright — CSS Locators Complete Reference_
