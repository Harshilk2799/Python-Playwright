# Python Playwright — Handling Single & Multi-Select Dropdowns (In-Depth Guide)

---

## Table of Contents

- [Python Playwright — Handling Single \& Multi-Select Dropdowns (In-Depth Guide)](#python-playwright--handling-single--multi-select-dropdowns-in-depth-guide)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites \& Setup](#prerequisites--setup)
  - [Understanding HTML Select Elements](#understanding-html-select-elements)
  - [Single-Select Dropdowns](#single-select-dropdowns)
    - [Method 1: select_option() by Value](#method-1-select_option-by-value)
    - [Method 2: select_option() by Label (Visible Text)](#method-2-select_option-by-label-visible-text)
    - [Method 3: select_option() by Index](#method-3-select_option-by-index)
    - [Method 4: select_option() by SelectOption Object](#method-4-select_option-by-selectoption-object)
    - [Method 5: Clicking the Dropdown Then an Option](#method-5-clicking-the-dropdown-then-an-option)
    - [Method 6: Using keyboard() to Navigate](#method-6-using-keyboard-to-navigate)
    - [Method 7: Using evaluate() (JavaScript Injection)](#method-7-using-evaluate-javascript-injection)
    - [Method 8: Using fill() on a Native Select (Workaround)](#method-8-using-fill-on-a-native-select-workaround)
  - [Multi-Select Dropdowns](#multi-select-dropdowns)
    - [Method 1: select_option() with a List of Values](#method-1-select_option-with-a-list-of-values)
    - [Method 2: select_option() with a List of Labels](#method-2-select_option-with-a-list-of-labels)
    - [Method 3: select_option() with a List of Indices](#method-3-select_option-with-a-list-of-indices)
    - [Method 4: Mixed Selection (Value + Label + Index)](#method-4-mixed-selection-value--label--index)
    - [Method 5: Ctrl+Click for Multi-Select](#method-5-ctrlclick-for-multi-select)
    - [Method 6: Select All Options via JavaScript](#method-6-select-all-options-via-javascript)
    - [Method 7: Deselect Specific Options](#method-7-deselect-specific-options)
  - [Custom Dropdowns (Non-Native)](#custom-dropdowns-non-native)
    - [Pattern 1: Click-to-Open + Click Option](#pattern-1-click-to-open--click-option)
    - [Pattern 2: Autocomplete / Searchable Dropdown](#pattern-2-autocomplete--searchable-dropdown)
    - [Pattern 3: React/Vue/Angular Dropdowns](#pattern-3-reactvueangular-dropdowns)
  - [Reading Selected Values](#reading-selected-values)
  - [Validating Dropdown Options](#validating-dropdown-options)
  - [Waiting Strategies for Dynamic Dropdowns](#waiting-strategies-for-dynamic-dropdowns)
  - [Real-World Complete Examples](#real-world-complete-examples)
    - [Example 1: Full Form with Single \& Multi Dropdowns](#example-1-full-form-with-single--multi-dropdowns)
    - [Example 2: Data-Driven Dropdown Selection](#example-2-data-driven-dropdown-selection)
  - [Error Handling \& Best Practices](#error-handling--best-practices)
  - [Summary Table](#summary-table)
  - [Quick Reference](#quick-reference)

---

## Introduction

Playwright is a powerful end-to-end testing and browser automation framework by Microsoft. It provides first-class support for handling HTML `<select>` dropdowns (both single and multi-select) through its `select_option()` API, as well as flexible strategies for custom UI dropdowns built with `<div>`, `<ul>`, or JavaScript frameworks.

This guide covers **every available method** with detailed explanations and runnable examples.

---

## Prerequisites & Setup

```bash
# Install Playwright
pip install playwright

# Install browsers
playwright install

# Or install only Chromium
playwright install chromium
```

```python
# Basic sync setup
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    # ... your code ...
    browser.close()
```

```python
# Basic async setup
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")
        # ... your code ...
        await browser.close()

asyncio.run(main())
```

> **Note:** All examples below use the **synchronous API**. To convert to async, add `await` before every Playwright call and wrap in `async def`.

---

## Understanding HTML Select Elements

```html
<!-- Single-Select Dropdown -->
<select id="country" name="country">
  <option value="">-- Select Country --</option>
  <option value="in">India</option>
  <option value="us">United States</option>
  <option value="uk">United Kingdom</option>
  <option value="au">Australia</option>
</select>

<!-- Multi-Select Dropdown -->
<select id="skills" name="skills" multiple>
  <option value="py">Python</option>
  <option value="js">JavaScript</option>
  <option value="java">Java</option>
  <option value="go">Go</option>
  <option value="rust">Rust</option>
</select>
```

**Key attributes:**
| Attribute | Meaning |
|---|---|
| `value` | The programmatic value sent on form submit |
| Text content | The visible label the user sees |
| `index` | Zero-based position of the option in the list |
| `multiple` | Allows multiple selections simultaneously |
| `selected` | Marks the option as selected by default |
| `disabled` | Makes an option unselectable |

---

## Single-Select Dropdowns

### Method 1: select_option() by Value

Selects by the `value` attribute of the `<option>` tag.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to a page with a dropdown
    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
        </select>
    """)

    # Select by value attribute
    page.select_option("#country", value="us")

    # Verify selection
    selected = page.locator("#country").input_value()
    print(f"Selected value: {selected}")  # Output: us

    browser.close()
```

**When to use:** When you know the backend `value` attribute (most reliable — values rarely change even if labels do).

---

### Method 2: select_option() by Label (Visible Text)

Selects by the visible text displayed in the dropdown.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
        </select>
    """)

    # Select by visible label text
    page.select_option("#country", label="India")

    selected_label = page.locator("#country option:checked").inner_text()
    print(f"Selected label: {selected_label}")  # Output: India

    browser.close()
```

**When to use:** When matching what the user visually sees. Be careful with leading/trailing whitespace in labels.

---

### Method 3: select_option() by Index

Selects by the zero-based position of the option in the list.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>   <!-- index 0 -->
            <option value="in">India</option>         <!-- index 1 -->
            <option value="us">United States</option> <!-- index 2 -->
            <option value="uk">United Kingdom</option><!-- index 3 -->
        </select>
    """)

    # Select the 3rd option (index 2 = "United States")
    page.select_option("#country", index=2)

    selected = page.locator("#country").input_value()
    print(f"Selected value: {selected}")  # Output: us

    browser.close()
```

**When to use:** When you want to pick by position (e.g., "always pick the second option"). Use with caution if the list order might change.

---

### Method 4: select_option() by SelectOption Object

Uses a dictionary to specify selection criteria explicitly.

```python
from playwright.sync_api import sync_playwright, SelectOption

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
        </select>
    """)

    # Using SelectOption object (explicit and readable)
    page.select_option("#country", SelectOption(value="uk"))
    print("Selected by SelectOption value:", page.locator("#country").input_value())

    page.select_option("#country", SelectOption(label="India"))
    print("Selected by SelectOption label:", page.locator("#country").input_value())

    page.select_option("#country", SelectOption(index=2))
    print("Selected by SelectOption index:", page.locator("#country").input_value())

    browser.close()
```

**When to use:** When you want explicit, self-documenting code that makes the selection strategy obvious.

---

### Method 5: Clicking the Dropdown Then an Option

Simulates a real user interaction — open the dropdown, then click the desired option.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
        </select>
    """)

    # Click to open the dropdown
    page.click("#country")

    # Click the specific option
    page.click("#country option[value='in']")

    print("Selected:", page.locator("#country").input_value())  # Output: in

    browser.close()
```

**When to use:** When triggering JavaScript event listeners that fire on click events (some frameworks need this).

---

### Method 6: Using keyboard() to Navigate

Simulates keyboard interaction — Tab to focus, then use arrow keys or type to select.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
        </select>
    """)

    # Focus the select element
    page.focus("#country")

    # Press ArrowDown to navigate options
    page.keyboard.press("ArrowDown")  # Moves to "India"
    page.keyboard.press("ArrowDown")  # Moves to "United States"

    print("Selected:", page.locator("#country").input_value())  # Output: us

    # Alternative: Type first letter to jump
    page.focus("#country")
    page.keyboard.press("u")  # Jumps to "United Kingdom" (or first option starting with U)

    browser.close()
```

**When to use:** Testing keyboard accessibility or when simulating real user keyboard navigation.

---

### Method 7: Using evaluate() (JavaScript Injection)

Directly manipulates the DOM using JavaScript — the most powerful but least "realistic" method.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
        </select>
    """)

    # Method A: Set value directly via JS
    page.evaluate("""
        document.querySelector('#country').value = 'uk';
        document.querySelector('#country').dispatchEvent(new Event('change'));
    """)
    print("JS set value:", page.locator("#country").input_value())  # uk

    # Method B: Select by index via JS
    page.evaluate("""
        const sel = document.querySelector('#country');
        sel.selectedIndex = 1;
        sel.dispatchEvent(new Event('change', { bubbles: true }));
    """)
    print("JS set by index:", page.locator("#country").input_value())  # in

    # Method C: Select by label text via JS
    page.evaluate("""
        const sel = document.querySelector('#country');
        const options = Array.from(sel.options);
        const target = options.find(o => o.text === 'United States');
        if (target) {
            target.selected = true;
            sel.dispatchEvent(new Event('change', { bubbles: true }));
        }
    """)
    print("JS set by label:", page.locator("#country").input_value())  # us

    browser.close()
```

**When to use:** When the element is obscured, disabled, or when you need to bypass UI restrictions for test setup. Always fire `change` events to trigger listeners.

---

### Method 8: Using fill() on a Native Select (Workaround)

`fill()` doesn't natively work on `<select>`, but you can combine it with `select_option()` in a helper.

```python
from playwright.sync_api import sync_playwright

def smart_select(page, selector, text):
    """Select by label, falling back gracefully."""
    try:
        page.select_option(selector, label=text)
    except Exception:
        # Fallback: try value
        page.select_option(selector, value=text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="in">India</option>
            <option value="us">United States</option>
        </select>
    """)

    smart_select(page, "#country", "India")
    print("Smart selected:", page.locator("#country").input_value())  # in

    browser.close()
```

---

## Multi-Select Dropdowns

Multi-select `<select multiple>` elements allow selecting several options simultaneously.

### Method 1: select_option() with a List of Values

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>
            <option value="js">JavaScript</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    # Select multiple options by value
    page.select_option("#skills", value=["py", "js", "go"])

    # Get all selected values
    selected_values = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions)
             .map(o => o.value)
    """)
    print("Selected values:", selected_values)  # ['py', 'js', 'go']

    browser.close()
```

---

### Method 2: select_option() with a List of Labels

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>
            <option value="js">JavaScript</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    # Select multiple options by visible label
    page.select_option("#skills", label=["Python", "Rust", "Java"])

    selected_labels = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions)
             .map(o => o.text)
    """)
    print("Selected labels:", selected_labels)  # ['Python', 'Java', 'Rust']

    browser.close()
```

---

### Method 3: select_option() with a List of Indices

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>    <!-- 0 -->
            <option value="js">JavaScript</option> <!-- 1 -->
            <option value="java">Java</option>     <!-- 2 -->
            <option value="go">Go</option>         <!-- 3 -->
            <option value="rust">Rust</option>     <!-- 4 -->
        </select>
    """)

    # Select options at index 0, 2, and 4 (Python, Java, Rust)
    page.select_option("#skills", index=[0, 2, 4])

    selected_labels = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions)
             .map(o => o.text)
    """)
    print("Selected by index:", selected_labels)  # ['Python', 'Java', 'Rust']

    browser.close()
```

---

### Method 4: Mixed Selection (Value + Label + Index)

You can combine different selection types in one call using a list of `SelectOption` objects.

```python
from playwright.sync_api import sync_playwright, SelectOption

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>
            <option value="js">JavaScript</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    # Mixed: one by value, one by label, one by index
    page.select_option("#skills", [
        SelectOption(value="py"),       # Python — by value
        SelectOption(label="Go"),        # Go     — by label
        SelectOption(index=4),           # Rust   — by index
    ])

    selected_labels = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions)
             .map(o => o.text)
    """)
    print("Mixed selected:", selected_labels)  # ['Python', 'Go', 'Rust']

    browser.close()
```

---

### Method 5: Ctrl+Click for Multi-Select

Simulates how a real user selects multiple options — hold Ctrl and click each option.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>
            <option value="js">JavaScript</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    options_to_select = ["py", "java", "rust"]

    # Click first option normally
    page.click(f"#skills option[value='{options_to_select[0]}']")

    # Ctrl+Click remaining options
    for val in options_to_select[1:]:
        page.click(
            f"#skills option[value='{val}']",
            modifiers=["Control"]  # Use "Meta" on macOS
        )

    selected_values = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions)
             .map(o => o.value)
    """)
    print("Ctrl+Click selected:", selected_values)  # ['py', 'java', 'rust']

    browser.close()
```

**When to use:** Testing multi-select UX behavior and event handling triggered by mouse clicks.

---

### Method 6: Select All Options via JavaScript

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py">Python</option>
            <option value="js">JavaScript</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    # Select ALL options via JavaScript
    page.evaluate("""
        const sel = document.querySelector('#skills');
        Array.from(sel.options).forEach(opt => opt.selected = true);
        sel.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    count = page.evaluate("""
        document.querySelector('#skills').selectedOptions.length
    """)
    print(f"Total selected: {count}")  # 5

    browser.close()
```

---

### Method 7: Deselect Specific Options

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="skills" multiple size="5">
            <option value="py" selected>Python</option>
            <option value="js" selected>JavaScript</option>
            <option value="java" selected>Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
        </select>
    """)

    # First, check what's currently selected
    initial = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions).map(o => o.value)
    """)
    print("Initially selected:", initial)  # ['py', 'js', 'java']

    # Deselect 'js' via JavaScript
    page.evaluate("""
        const sel = document.querySelector('#skills');
        const opt = Array.from(sel.options).find(o => o.value === 'js');
        if (opt) opt.selected = false;
        sel.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    after = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions).map(o => o.value)
    """)
    print("After deselect:", after)  # ['py', 'java']

    # Re-select only specific items (replaces all current selections)
    page.select_option("#skills", value=["go", "rust"])
    final = page.evaluate("""
        Array.from(document.querySelector('#skills').selectedOptions).map(o => o.value)
    """)
    print("Final selection:", final)  # ['go', 'rust']

    browser.close()
```

> **Important:** Calling `select_option()` **replaces** the entire selection. It does not append to it.

---

## Custom Dropdowns (Non-Native)

Many modern websites use custom dropdown components built with `<div>`, `<ul>`, or JavaScript frameworks instead of native `<select>` elements. These require different strategies.

### Pattern 1: Click-to-Open + Click Option

```html
<!-- Example custom dropdown HTML structure -->
<div class="dropdown">
  <button class="dropdown-toggle">Select Country</button>
  <ul class="dropdown-menu" hidden>
    <li data-value="in">India</li>
    <li data-value="us">United States</li>
    <li data-value="uk">United Kingdom</li>
  </ul>
</div>
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <div class="dropdown">
            <button id="toggle">Select Country ▼</button>
            <ul id="menu" style="display:none; list-style:none; padding:0; border:1px solid #ccc;">
                <li data-value="in" onclick="this.parentElement.style.display='none';
                    document.getElementById('toggle').textContent=this.textContent;">India</li>
                <li data-value="us" onclick="this.parentElement.style.display='none';
                    document.getElementById('toggle').textContent=this.textContent;">United States</li>
                <li data-value="uk" onclick="this.parentElement.style.display='none';
                    document.getElementById('toggle').textContent=this.textContent;">United Kingdom</li>
            </ul>
        </div>
        <script>
            document.getElementById('toggle').onclick = function() {
                var m = document.getElementById('menu');
                m.style.display = m.style.display === 'none' ? 'block' : 'none';
            }
        </script>
    """)

    # Step 1: Click to open the dropdown
    page.click("#toggle")

    # Step 2: Wait for menu to appear
    page.wait_for_selector("#menu", state="visible")

    # Step 3: Click the desired option
    page.click("li[data-value='us']")

    # Verify
    button_text = page.locator("#toggle").inner_text()
    print("Selected:", button_text)  # United States

    browser.close()
```

---

### Pattern 2: Autocomplete / Searchable Dropdown

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Example: Select2 or similar autocomplete
    # Real usage on a site like https://select2.org/
    page.goto("https://select2.org/getting-started/basic-usage")

    # Open the dropdown by clicking the Select2 container
    page.click(".select2-selection")

    # Type to search/filter
    page.keyboard.type("Alabam")

    # Wait for filtered results
    page.wait_for_selector(".select2-results__option", state="visible")

    # Click the matching result
    page.click(".select2-results__option", strict=False)  # Clicks first match

    browser.close()
```

---

### Pattern 3: React/Vue/Angular Dropdowns

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Generic pattern for most component-library dropdowns
    page.set_content("""
        <div id="app">
            <div class="select-container" role="combobox" aria-haspopup="listbox"
                 aria-expanded="false" tabindex="0">
                <span class="selected-value">Choose...</span>
                <div class="options" role="listbox" style="display:none;">
                    <div role="option" data-value="a">Option A</div>
                    <div role="option" data-value="b">Option B</div>
                    <div role="option" data-value="c">Option C</div>
                </div>
            </div>
        </div>
        <script>
            const container = document.querySelector('.select-container');
            container.addEventListener('click', function() {
                const opts = this.querySelector('.options');
                const expanded = this.getAttribute('aria-expanded') === 'true';
                opts.style.display = expanded ? 'none' : 'block';
                this.setAttribute('aria-expanded', !expanded);
            });
            document.querySelectorAll('[role=option]').forEach(opt => {
                opt.addEventListener('click', function(e) {
                    e.stopPropagation();
                    document.querySelector('.selected-value').textContent = this.textContent;
                    document.querySelector('.options').style.display = 'none';
                    container.setAttribute('aria-expanded', 'false');
                });
            });
        </script>
    """)

    # Use ARIA roles for robust selection
    page.click("[role='combobox']")
    page.wait_for_selector("[role='listbox']", state="visible")
    page.click("[role='option']:has-text('Option B')")

    result = page.locator(".selected-value").inner_text()
    print("Selected:", result)  # Option B

    browser.close()
```

---

## Reading Selected Values

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="single">
            <option value="a">Alpha</option>
            <option value="b" selected>Beta</option>
            <option value="c">Gamma</option>
        </select>
        <select id="multi" multiple>
            <option value="x" selected>X</option>
            <option value="y">Y</option>
            <option value="z" selected>Z</option>
        </select>
    """)

    # --- Single select ---
    # Get the selected VALUE
    single_value = page.locator("#single").input_value()
    print("Single value:", single_value)  # b

    # Get the selected LABEL (visible text)
    single_label = page.locator("#single option:checked").inner_text()
    print("Single label:", single_label)  # Beta

    # --- Multi select ---
    # Get all selected VALUES
    multi_values = page.evaluate("""
        Array.from(document.querySelector('#multi').selectedOptions)
             .map(o => o.value)
    """)
    print("Multi values:", multi_values)  # ['x', 'z']

    # Get all selected LABELS
    multi_labels = page.evaluate("""
        Array.from(document.querySelector('#multi').selectedOptions)
             .map(o => o.text)
    """)
    print("Multi labels:", multi_labels)  # ['X', 'Z']

    # Get count of selected options
    count = page.evaluate("""
        document.querySelector('#multi').selectedOptions.length
    """)
    print("Count:", count)  # 2

    browser.close()
```

---

## Validating Dropdown Options

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="fruits">
            <option value="">-- Pick a fruit --</option>
            <option value="apple">Apple</option>
            <option value="banana">Banana</option>
            <option value="cherry">Cherry</option>
            <option value="date" disabled>Date (Out of Stock)</option>
        </select>
    """)

    # Get ALL option labels
    all_labels = page.locator("#fruits option").all_inner_texts()
    print("All options:", all_labels)

    # Get ALL option values
    all_values = page.evaluate("""
        Array.from(document.querySelector('#fruits').options).map(o => o.value)
    """)
    print("All values:", all_values)

    # Check if a specific option exists
    has_banana = "Banana" in all_labels
    print("Has Banana:", has_banana)  # True

    # Check option count
    option_count = page.locator("#fruits option").count()
    print("Option count:", option_count)  # 5

    # Get only ENABLED options
    enabled_options = page.evaluate("""
        Array.from(document.querySelector('#fruits').options)
             .filter(o => !o.disabled)
             .map(o => o.text)
    """)
    print("Enabled options:", enabled_options)

    # Assert using Playwright's expect (for tests)
    from playwright.sync_api import expect
    expect(page.locator("#fruits")).to_have_values([
        "", "apple", "banana", "cherry", "date"
    ])

    browser.close()
```

---

## Waiting Strategies for Dynamic Dropdowns

Dynamic dropdowns load options asynchronously (e.g., country → state → city cascades).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.set_content("""
        <select id="country">
            <option value="">-- Select Country --</option>
            <option value="in">India</option>
            <option value="us">United States</option>
        </select>
        <select id="state" disabled>
            <option value="">-- Select State --</option>
        </select>
        <script>
            document.getElementById('country').addEventListener('change', function() {
                const stateSelect = document.getElementById('state');
                stateSelect.innerHTML = '<option value="">Loading...</option>';
                stateSelect.disabled = true;
                // Simulate async data fetch
                setTimeout(() => {
                    const states = {
                        in: [['mh','Maharashtra'],['gj','Gujarat'],['dl','Delhi']],
                        us: [['ca','California'],['ny','New York'],['tx','Texas']]
                    };
                    const options = states[this.value] || [];
                    stateSelect.innerHTML = '<option value="">-- Select State --</option>' +
                        options.map(([v,l]) => `<option value="${v}">${l}</option>`).join('');
                    stateSelect.disabled = false;
                }, 500);
            });
        </script>
    """)

    # Select country — this triggers async state loading
    page.select_option("#country", value="in")

    # Strategy 1: Wait for the state dropdown to be enabled
    page.wait_for_selector("#state:not([disabled])")

    # Strategy 2: Wait for specific option to appear
    page.wait_for_selector("#state option[value='mh']")

    # Strategy 3: Wait for option count to increase
    page.wait_for_function("""
        document.querySelector('#state').options.length > 1
    """)

    # Now select the state
    page.select_option("#state", value="gj")

    state_label = page.locator("#state option:checked").inner_text()
    print("Selected state:", state_label)  # Gujarat

    browser.close()
```

---

## Real-World Complete Examples

### Example 1: Full Form with Single & Multi Dropdowns

```python
from playwright.sync_api import sync_playwright

def fill_registration_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        page.set_content("""
            <form id="registration">
                <label>Country:
                    <select id="country" name="country">
                        <option value="">-- Select --</option>
                        <option value="in">India</option>
                        <option value="us">United States</option>
                        <option value="uk">United Kingdom</option>
                    </select>
                </label>
                <br><br>
                <label>Experience Level:
                    <select id="level" name="level">
                        <option value="junior">Junior (0-2 yrs)</option>
                        <option value="mid">Mid (2-5 yrs)</option>
                        <option value="senior">Senior (5+ yrs)</option>
                    </select>
                </label>
                <br><br>
                <label>Tech Stack (multi):
                    <select id="stack" name="stack" multiple size="4">
                        <option value="frontend">Frontend</option>
                        <option value="backend">Backend</option>
                        <option value="devops">DevOps</option>
                        <option value="data">Data Science</option>
                    </select>
                </label>
                <br><br>
                <button type="submit">Submit</button>
            </form>
        """)

        # Fill single dropdowns
        page.select_option("#country", label="India")
        page.select_option("#level", value="senior")

        # Fill multi-select
        page.select_option("#stack", value=["backend", "devops", "data"])

        # Validate selections
        assert page.locator("#country").input_value() == "in"
        assert page.locator("#level").input_value() == "senior"

        selected_stack = page.evaluate("""
            Array.from(document.querySelector('#stack').selectedOptions)
                 .map(o => o.value)
        """)
        assert set(selected_stack) == {"backend", "devops", "data"}

        print("Form filled and validated successfully!")
        print(f"  Country: {page.locator('#country option:checked').inner_text()}")
        print(f"  Level:   {page.locator('#level option:checked').inner_text()}")
        print(f"  Stack:   {selected_stack}")

        browser.close()

fill_registration_form()
```

### Example 2: Data-Driven Dropdown Selection

```python
from playwright.sync_api import sync_playwright
import json

# Test data
TEST_CASES = [
    {"country": "in", "skills": ["py", "go"]},
    {"country": "us", "skills": ["js", "rust"]},
    {"country": "uk", "skills": ["java", "py", "go"]},
]

def run_dropdown_tests(test_cases):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, tc in enumerate(test_cases):
            page.set_content("""
                <select id="country">
                    <option value="in">India</option>
                    <option value="us">United States</option>
                    <option value="uk">United Kingdom</option>
                </select>
                <select id="skills" multiple size="5">
                    <option value="py">Python</option>
                    <option value="js">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                </select>
            """)

            page.select_option("#country", value=tc["country"])
            page.select_option("#skills", value=tc["skills"])

            actual_country = page.locator("#country").input_value()
            actual_skills = page.evaluate("""
                Array.from(document.querySelector('#skills').selectedOptions)
                     .map(o => o.value)
            """)

            assert actual_country == tc["country"], f"Test {i+1}: Country mismatch"
            assert set(actual_skills) == set(tc["skills"]), f"Test {i+1}: Skills mismatch"
            print(f"✅ Test {i+1} passed: country={actual_country}, skills={actual_skills}")

        browser.close()

run_dropdown_tests(TEST_CASES)
```

---

## Error Handling & Best Practices

```python
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

def safe_select(page, selector, **kwargs):
    """Robust dropdown selection with retries and error handling."""
    try:
        page.wait_for_selector(selector, state="visible", timeout=5000)
        result = page.select_option(selector, timeout=5000, **kwargs)
        return result
    except PWTimeout:
        print(f"Timeout: Element {selector} not visible within 5s")
        return None
    except Exception as e:
        print(f"Error selecting from {selector}: {e}")
        return None

# Best Practices Summary:
best_practices = {
    "1_prefer_value": "Use value= over label= when possible — values are stable, labels may change",
    "2_wait_dynamic": "Always wait for dynamic dropdowns to finish loading before selecting",
    "3_assert_after": "Validate the selected value after selection in critical test flows",
    "4_dispatchEvent": "When using JS evaluate(), always fire the 'change' event with bubbles:true",
    "5_slow_mo": "Use slow_mo=200-500 in launch() for debugging flaky dropdown interactions",
    "6_aria_roles":  "For custom dropdowns, prefer ARIA role selectors (role='option') for robustness",
    "7_no_fill": "Never use fill() on native <select> elements — use select_option() instead",
    "8_replace_all": "select_option() REPLACES all selections — it doesn't append",
}

for key, tip in best_practices.items():
    print(f"[{key}] {tip}")
```

---

## Summary Table

| Method               | API                                | Single | Multi | Native `<select>` | Custom Dropdown |
| -------------------- | ---------------------------------- | :----: | :---: | :---------------: | :-------------: |
| By value             | `select_option(value="x")`         |   ✅   |  ✅   |        ✅         |       ❌        |
| By label             | `select_option(label="X")`         |   ✅   |  ✅   |        ✅         |       ❌        |
| By index             | `select_option(index=0)`           |   ✅   |  ✅   |        ✅         |       ❌        |
| SelectOption object  | `select_option(SelectOption(...))` |   ✅   |  ✅   |        ✅         |       ❌        |
| Click + Click option | `click()` → `click()`              |   ✅   |  ✅   |        ✅         |       ✅        |
| Keyboard navigation  | `focus()` + `keyboard.press()`     |   ✅   |  ❌   |        ✅         |     Partial     |
| JavaScript evaluate  | `evaluate(js_code)`                |   ✅   |  ✅   |        ✅         |       ✅        |
| Ctrl+Click           | `click(modifiers=["Control"])`     |   ❌   |  ✅   |        ✅         |       ✅        |
| List of values       | `select_option(value=[...])`       |   ❌   |  ✅   |        ✅         |       ❌        |
| List of labels       | `select_option(label=[...])`       |   ❌   |  ✅   |        ✅         |       ❌        |
| List of indices      | `select_option(index=[...])`       |   ❌   |  ✅   |        ✅         |       ❌        |

---

## Quick Reference

```python
# ─── Single Select ──────────────────────────────────────────────
page.select_option("#id", value="val")       # by value attribute
page.select_option("#id", label="Text")      # by visible text
page.select_option("#id", index=2)           # by zero-based index

# ─── Multi Select ───────────────────────────────────────────────
page.select_option("#id", value=["a","b"])   # multiple values
page.select_option("#id", label=["X","Y"])   # multiple labels
page.select_option("#id", index=[0,1,2])     # multiple indices

# ─── Read Selected ──────────────────────────────────────────────
page.locator("#id").input_value()            # single: selected value
page.locator("#id option:checked").inner_text()  # single: selected label

# ─── Custom Dropdown ────────────────────────────────────────────
page.click(".toggle")                        # open
page.wait_for_selector(".menu", state="visible")
page.click(".menu li:has-text('Option')")    # pick item

# ─── Wait for Dynamic ───────────────────────────────────────────
page.wait_for_selector("#state:not([disabled])")
page.wait_for_selector("#state option[value='ca']")
page.wait_for_function("document.querySelector('#state').options.length > 1")
```

---

_Guide authored for Python Playwright (sync & async API) — covers all major dropdown handling patterns as of 2025._
