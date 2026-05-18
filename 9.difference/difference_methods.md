# 🎭 Python Playwright: Text Extraction Methods — Complete Guide

> A deep dive into `inner_text` vs `text_content`, `all_inner_texts` vs `all_text_contents`, and the `all()` method with practical examples.

---

## Table of Contents

1. [inner_text() vs text_content()](#1-inner_text-vs-text_content)
2. [all_inner_texts() vs all_text_contents()](#2-all_inner_texts-vs-all_text_contents)
3. [The all() Method](#3-the-all-method)
4. [Complete Comparison at a Glance](#4-complete-comparison-at-a-glance)
5. [When to Use What](#5-when-to-use-what)

---

## 1. `inner_text()` vs `text_content()`

These two methods both retrieve text from a **single element**, but they behave very differently under the hood.

---

### `text_content()`

- Returns the **raw text content** of the element and **all its descendants**
- Mirrors the DOM property `Node.textContent`
- **Does NOT care about CSS visibility** — returns text even if `display: none` or `visibility: hidden`
- Includes text from `<script>` and `<style>` tags if they're inside the element
- Returns text **exactly as it is in the DOM**, with no style-based formatting

### `inner_text()`

- Returns the **human-visible text** of the element
- Mirrors the DOM property `HTMLElement.innerText`
- **Respects CSS styling** — hidden elements are excluded
- Applies **line breaks** based on rendered layout (`<br>`, block elements, etc.)
- Triggers **layout/reflow** in the browser (slightly slower)
- More aligned with what a real user **sees on screen**

---

### Example

```python
from playwright.sync_api import sync_playwright

HTML = """
<html>
<body>
  <div id="demo">
    Hello <span style="display:none">Hidden</span> World
    <style>.cls { color: red; }</style>
    <script>var x = 1;</script>
  </div>
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    locator = page.locator("#demo")

    print("text_content():", repr(locator.text_content()))
    # Output: '\n    Hello Hidden World\n    .cls { color: red; }\n    var x = 1;\n  '
    # Includes hidden text, style content, and script content

    print("inner_text():", repr(locator.inner_text()))
    # Output: 'Hello World'
    # Only visible text — hidden span, style, and script are excluded

    browser.close()
```

---

### Comparison Table

| Feature                     | `text_content()` | `inner_text()`               |
| --------------------------- | ---------------- | ---------------------------- |
| Hidden elements             | ✅ Included      | ❌ Excluded                  |
| `<style>` / `<script>` tags | ✅ Included      | ❌ Excluded                  |
| CSS-aware                   | ❌ No            | ✅ Yes                       |
| Respects layout/line breaks | ❌ No            | ✅ Yes                       |
| Speed                       | ⚡ Faster        | 🐢 Slightly slower           |
| Best for                    | Raw DOM scraping | User-visible text assertions |

---

## 2. `all_inner_texts()` vs `all_text_contents()`

These are the **multi-element versions** — they return a **list of strings**, one per matched element.

---

### `all_text_contents()`

- Returns a list of `text_content` values for **every element** matched by the locator
- Does **not** wait for elements to be visible or stable
- Fast but includes hidden/raw content

### `all_inner_texts()`

- Returns a list of `inner_text` values for **every element** matched by the locator
- Respects CSS visibility per element
- More reliable for asserting what users actually see

---

### Example

```python
from playwright.sync_api import sync_playwright

HTML = """
<html>
<body>
  <ul>
    <li>Apple</li>
    <li style="display:none">Hidden Mango</li>
    <li>  Banana  </li>
    <li>Cherry</li>
  </ul>
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    locator = page.locator("li")

    print("all_text_contents():", locator.all_text_contents())
    # Output: ['Apple', 'Hidden Mango', '  Banana  ', 'Cherry']
    # Returns ALL 4 items including the hidden one, with raw whitespace

    print("all_inner_texts():", locator.all_inner_texts())
    # Output: ['Apple', '', 'Banana', 'Cherry']
    # Hidden element returns '', whitespace is trimmed

    browser.close()
```

---

### Comparison Table

| Feature             | `all_text_contents()`    | `all_inner_texts()`        |
| ------------------- | ------------------------ | -------------------------- |
| Returns             | `List[str]` — raw text   | `List[str]` — visible text |
| Hidden elements     | ✅ Included (as text)    | ❌ Returns `''`            |
| Whitespace trimming | ❌ No                    | ✅ Yes                     |
| CSS-aware           | ❌ No                    | ✅ Yes                     |
| Best for            | Raw bulk text extraction | Visible text validation    |

---

## 3. The `all()` Method

The `all()` method is fundamentally different — it doesn't return text. Instead, it returns a **list of `Locator` objects**, one for each matched element.

- Resolves the locator into **individual locators** at call time
- Lets you **iterate** over each element and call any locator method on it
- Does **not** auto-wait — captures elements present at the moment of the call
- Ideal when you need to perform **different actions or assertions per element**

---

### Example

```python
from playwright.sync_api import sync_playwright

HTML = """
<html>
<body>
  <ul>
    <li class="fruit">Apple - $1.00</li>
    <li class="fruit">Banana - $0.50</li>
    <li class="fruit" style="display:none">Mango - $2.00</li>
    <li class="fruit">Cherry - $3.00</li>
  </ul>
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    items = page.locator("li.fruit").all()
    # Returns: [Locator, Locator, Locator, Locator] — 4 individual Locator objects

    print(f"Total elements found: {len(items)}")  # 4

    for i, item in enumerate(items):
        raw      = item.text_content()    # raw DOM text
        visible  = item.inner_text()      # CSS-aware visible text
        is_vis   = item.is_visible()
        print(f"[{i}] is_visible={is_vis} | text_content={repr(raw)} | inner_text={repr(visible)}")

    # Output:
    # [0] is_visible=True  | text_content='Apple - $1.00'  | inner_text='Apple - $1.00'
    # [1] is_visible=True  | text_content='Banana - $0.50' | inner_text='Banana - $0.50'
    # [2] is_visible=False | text_content='Mango - $2.00'  | inner_text=''
    # [3] is_visible=True  | text_content='Cherry - $3.00' | inner_text='Cherry - $3.00'

    browser.close()
```

---

### Why Use `all()` Instead of `all_text_contents()` or `all_inner_texts()`?

Because `all()` gives you full **Locator power** per element:

```python
items = page.locator("li.fruit").all()

for item in items:
    if item.is_visible():
        item.click()                         # click each visible item
        item.screenshot(path="item.png")     # screenshot each one
        print(item.get_attribute("class"))   # read attributes
        item.highlight()                     # highlight for debugging
```

You cannot do any of this with `all_text_contents()` or `all_inner_texts()` — those only return plain strings.

---

## 4. Complete Comparison at a Glance

```python
locator = page.locator("li")

# ── Single Element ─────────────────────────────────────────────────────────
locator.first.text_content()       # str  — raw DOM text of first match
locator.first.inner_text()         # str  — visible text of first match

# ── Multiple Elements → List[str] ──────────────────────────────────────────
locator.all_text_contents()        # List[str] — raw DOM text per element
locator.all_inner_texts()          # List[str] — visible text per element

# ── Multiple Elements → List[Locator] ──────────────────────────────────────
locator.all()                      # List[Locator] — interact per element
```

---

## 5. When to Use What

| Scenario                                           | Best Method           |
| -------------------------------------------------- | --------------------- |
| Assert exact visible text of one element           | `inner_text()`        |
| Scrape raw DOM content of one element              | `text_content()`      |
| Collect all visible labels in a list/dropdown      | `all_inner_texts()`   |
| Extract all raw text from multiple elements        | `all_text_contents()` |
| Click, screenshot, or interact with each element   | `all()`               |
| Check visibility + text conditionally per element  | `all()`               |
| Count elements and get their individual attributes | `all()`               |

---

## Key Takeaways

- **`text_content()`** — Raw DOM text, CSS-blind, fast. Use for scraping.
- **`inner_text()`** — Visible text only, CSS-aware, layout-aware. Use for assertions.
- **`all_text_contents()`** — Bulk raw text list. Includes hidden elements.
- **`all_inner_texts()`** — Bulk visible text list. Excludes hidden elements.
- **`all()`** — Returns Locator list for per-element interactions. Most powerful and flexible.

> **Rule of thumb:** If you're asserting what a user sees, use `inner_text` variants.  
> If you need to interact with elements individually, use `all()`.  
> If you just need raw data from the DOM, use `text_content` variants.
