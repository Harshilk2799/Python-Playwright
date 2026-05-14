# Python Playwright: Handling Input Boxes, Radio Buttons & Checkboxes

> A comprehensive, in-depth guide covering every method available in Playwright for interacting with form elements.

---

## Table of Contents

- [Python Playwright: Handling Input Boxes, Radio Buttons \& Checkboxes](#python-playwright-handling-input-boxes-radio-buttons--checkboxes)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup \& Installation](#setup--installation)
  - [Input Box Handling](#input-box-handling)
    - [HTML Reference](#html-reference)
    - [Method 1: `fill()`](#method-1-fill)
    - [Method 2: `type()`](#method-2-type)
    - [Method 3: `press_sequentially()`](#method-3-press_sequentially)
    - [Method 4: `press()`](#method-4-press)
    - [Method 5: `clear()`](#method-5-clear)
    - [Method 6: `input_value()`](#method-6-input_value)
    - [Method 7: `focus()` + Keyboard API](#method-7-focus--keyboard-api)
    - [Method 8: `evaluate()` (JavaScript Injection)](#method-8-evaluate-javascript-injection)
    - [Method 9: Clipboard Paste via `page.evaluate()`](#method-9-clipboard-paste-via-pageevaluate)
    - [Method 10: `dispatch_event()` for Dynamic Inputs](#method-10-dispatch_event-for-dynamic-inputs)
  - [Radio Button Handling](#radio-button-handling)
    - [HTML Reference](#html-reference-1)
    - [Method 1: `check()` (Radio)](#method-1-check-radio)
    - [Method 2: `click()` (Radio)](#method-2-click-radio)
    - [Method 3: `is_checked()` (Radio)](#method-3-is_checked-radio)
    - [Method 4: `evaluate()` (JavaScript Radio)](#method-4-evaluate-javascript-radio)
    - [Method 5: Selecting by Value with `locator()`](#method-5-selecting-by-value-with-locator)
    - [Method 6: `get_by_label()` + `check()`](#method-6-get_by_label--check)
    - [Method 7: `get_by_role()` (Radio)](#method-7-get_by_role-radio)
  - [Checkbox Handling](#checkbox-handling)
    - [HTML Reference](#html-reference-2)
    - [Method 1: `check()` (Checkbox)](#method-1-check-checkbox)
    - [Method 2: `uncheck()`](#method-2-uncheck)
    - [Method 3: `click()` (Checkbox)](#method-3-click-checkbox)
    - [Method 4: `set_checked()`](#method-4-set_checked)
    - [Method 5: `is_checked()` (Checkbox)](#method-5-is_checked-checkbox)
    - [Method 6: `evaluate()` (JavaScript Checkbox)](#method-6-evaluate-javascript-checkbox)
    - [Method 7: `get_by_label()` + `check()` (Checkbox)](#method-7-get_by_label--check-checkbox)
    - [Method 8: Checking Multiple Checkboxes in a Loop](#method-8-checking-multiple-checkboxes-in-a-loop)
  - [Combining All Elements — Full Form Example](#combining-all-elements--full-form-example)
  - [Locator Strategies Summary](#locator-strategies-summary)
  - [Best Practices](#best-practices)
    - [1. Prefer `locator()` over `page.fill()` (Modern API)](#1-prefer-locator-over-pagefill-modern-api)
    - [2. Use Accessibility Locators When Possible](#2-use-accessibility-locators-when-possible)
    - [3. Use `set_checked()` for Conditional State](#3-use-set_checked-for-conditional-state)
    - [4. Always Verify After Interaction](#4-always-verify-after-interaction)
    - [5. Add Waits for Dynamic Forms](#5-add-waits-for-dynamic-forms)
    - [6. Use `slow_mo` During Development](#6-use-slow_mo-during-development)
    - [7. Use `force=True` Sparingly](#7-use-forcetrue-sparingly)
  - [Common Errors \& Fixes](#common-errors--fixes)
    - [Error: `TimeoutError: Waiting for locator to be visible`](#error-timeouterror-waiting-for-locator-to-be-visible)
    - [Error: `Element is not an input[type=checkbox]`](#error-element-is-not-an-inputtypecheckbox)
    - [Error: `Checkbox is already checked`](#error-checkbox-is-already-checked)
    - [Error: React/Vue input not updating](#error-reactvue-input-not-updating)
    - [Error: `strict mode violation — multiple elements matched`](#error-strict-mode-violation--multiple-elements-matched)

---

## Introduction

[Playwright](https://playwright.dev/python/) is a powerful browser automation library by Microsoft. It supports Chromium, Firefox, and WebKit, and provides both synchronous and asynchronous APIs for Python.

This guide focuses on three core form interaction categories:

| Element          | Common Actions                                    |
| ---------------- | ------------------------------------------------- |
| **Input Box**    | fill, type, clear, read value, keyboard shortcuts |
| **Radio Button** | check, click, verify selection, select by value   |
| **Checkbox**     | check, uncheck, toggle, set state, verify state   |

---

## Setup & Installation

```bash
pip install playwright
playwright install
```

**Basic Boilerplate (Sync API):**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    # ... your interactions here
    browser.close()
```

**Basic Boilerplate (Async API):**

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")
        # ... your interactions here
        await browser.close()

asyncio.run(main())
```

> All examples below use the **synchronous API** for clarity. Prefix `await` before each Playwright call to convert to async.

---

## Input Box Handling

An input box (text field) is the most common form element. Playwright provides multiple ways to interact with it.

### HTML Reference

```html
<input type="text" id="username" name="username" placeholder="Enter username" />
<input type="password" id="password" name="password" />
<textarea id="bio" name="bio"></textarea>
```

---

### Method 1: `fill()`

**Best for:** Quickly setting a value in an input or textarea. It clears the existing content first, then types the new value atomically.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Fill by CSS selector
    page.fill("#username", "john_doe")

    # Fill by placeholder
    page.fill("[placeholder='Enter username']", "john_doe")

    # Fill using locator (recommended modern approach)
    page.locator("#username").fill("john_doe")

    # Fill a textarea
    page.locator("#bio").fill("This is my biography text.\nIt spans multiple lines.")

    # Fill password field
    page.locator("#password").fill("SecurePass@123")

    browser.close()
```

**Key Characteristics:**

- Clears existing content before filling
- Does NOT simulate keystroke-by-keystroke (fires `input` and `change` events)
- Fast — ideal for most use cases
- Waits for the element to be visible and enabled automatically

---

### Method 2: `type()`

**Best for:** Simulating real human typing character by character, triggering `keydown`, `keypress`, `keyup`, and `input` events for each character.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Type character by character (default delay: no delay)
    page.locator("#username").type("john_doe")

    # Type with a realistic delay between keystrokes (milliseconds)
    page.locator("#username").type("john_doe", delay=100)

    # Click to focus first, then type
    page.locator("#bio").click()
    page.locator("#bio").type("Hello, I am typing slowly!", delay=75)

    browser.close()
```

**Key Characteristics:**

- Simulates real human typing (keystroke by keystroke)
- Triggers all keyboard events per character
- Useful for apps with real-time search suggestions, autocomplete, or live validation
- Slower than `fill()` but more realistic

> ⚠️ **Note:** `type()` does NOT clear existing text. Use `fill()` or `triple_click()` + `type()` if you need to replace content.

---

### Method 3: `press_sequentially()`

**Best for:** Modern replacement for `type()` in newer Playwright versions. Sends keystrokes one by one with optional delay.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Press keys sequentially with delay
    page.locator("#username").press_sequentially("john_doe", delay=80)

    # No delay (fast sequential keypresses)
    page.locator("#search").press_sequentially("playwright python")

    browser.close()
```

**Key Characteristics:**

- Fires `keydown`, `input`, `keyup` for each character
- Preferred over `type()` in Playwright v1.30+
- Supports `delay` parameter for human-like behavior

---

### Method 4: `press()`

**Best for:** Pressing special keys like Enter, Tab, Escape, Arrow keys, or keyboard shortcuts.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    page.locator("#username").fill("john_doe")

    # Press Enter to submit the form
    page.locator("#username").press("Enter")

    # Press Tab to move to the next field
    page.locator("#username").press("Tab")

    # Press keyboard shortcut: Ctrl+A (select all)
    page.locator("#bio").press("Control+A")

    # Press Backspace
    page.locator("#username").press("Backspace")

    # Press Escape
    page.locator("#search").press("Escape")

    # Press Arrow keys (useful for dropdowns)
    page.locator("#dropdown").press("ArrowDown")
    page.locator("#dropdown").press("ArrowDown")
    page.locator("#dropdown").press("Enter")

    browser.close()
```

**Common Key Names:**

| Key        | Playwright Key String |
| ---------- | --------------------- |
| Enter      | `"Enter"`             |
| Tab        | `"Tab"`               |
| Escape     | `"Escape"`            |
| Backspace  | `"Backspace"`         |
| Delete     | `"Delete"`            |
| Arrow Up   | `"ArrowUp"`           |
| Arrow Down | `"ArrowDown"`         |
| Ctrl+A     | `"Control+A"`         |
| Ctrl+C     | `"Control+C"`         |
| Ctrl+V     | `"Control+V"`         |
| Shift+Tab  | `"Shift+Tab"`         |

---

### Method 5: `clear()`

**Best for:** Clearing the content of an input field without typing anything new.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # First fill the field
    page.locator("#username").fill("old_username")

    # Then clear it
    page.locator("#username").clear()

    # Verify it's empty
    value = page.locator("#username").input_value()
    assert value == "", f"Expected empty string but got: '{value}'"

    # Alternative: Use fill with empty string
    page.locator("#username").fill("")

    # Alternative: Triple-click to select all + Delete key
    page.locator("#bio").triple_click()
    page.locator("#bio").press("Delete")

    browser.close()
```

---

### Method 6: `input_value()`

**Best for:** Reading the current value from an input field for assertions or conditional logic.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Fill then read
    page.locator("#username").fill("john_doe")
    current_value = page.locator("#username").input_value()
    print(f"Current value: {current_value}")  # Output: john_doe

    # Use in conditional logic
    if page.locator("#email").input_value() == "":
        page.locator("#email").fill("default@example.com")

    # Read value from a textarea
    bio_text = page.locator("#bio").input_value()
    assert "biography" in bio_text.lower()

    browser.close()
```

---

### Method 7: `focus()` + Keyboard API

**Best for:** Situations where you need to focus a field and then use the global `page.keyboard` API for granular key control.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Focus the input
    page.locator("#username").focus()

    # Use the keyboard API directly
    page.keyboard.type("john", delay=50)
    page.keyboard.press("End")         # Move cursor to end
    page.keyboard.type("_doe", delay=50)

    # Select all text using keyboard shortcut and replace
    page.locator("#bio").focus()
    page.keyboard.press("Control+A")
    page.keyboard.type("Replaced entire content!")

    # Holding Shift to select range
    page.locator("#username").focus()
    page.keyboard.press("Home")        # Go to start
    page.keyboard.down("Shift")
    page.keyboard.press("End")         # Select to end while holding Shift
    page.keyboard.up("Shift")
    page.keyboard.press("Delete")      # Delete selected text

    browser.close()
```

---

### Method 8: `evaluate()` (JavaScript Injection)

**Best for:** When standard Playwright methods don't trigger the right events, or you need to bypass restrictions (e.g., read-only attributes set via JS, React-controlled inputs).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Set value directly via JavaScript
    page.evaluate("""
        document.querySelector('#username').value = 'john_doe';
    """)

    # Trigger change event after JS injection (important for React/Vue)
    page.evaluate("""
        const input = document.querySelector('#username');
        input.value = 'john_doe';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    # Read value via JavaScript
    value = page.evaluate("document.querySelector('#username').value")
    print(f"JS value: {value}")

    # Bypass readonly attribute
    page.evaluate("""
        const el = document.querySelector('#readonly-field');
        el.removeAttribute('readonly');
        el.value = 'now editable';
    """)

    browser.close()
```

---

### Method 9: Clipboard Paste via `page.evaluate()`

**Best for:** Pasting large amounts of text quickly, simulating clipboard paste behavior.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    large_text = "A" * 5000  # 5000 character string

    # Method 1: Use fill (most efficient for large text)
    page.locator("#bio").fill(large_text)

    # Method 2: Use clipboard API via JavaScript
    page.locator("#bio").focus()
    page.evaluate(f"""
        navigator.clipboard.writeText('{large_text[:100]}').then(() => {{
            document.querySelector('#bio').focus();
            document.execCommand('paste');
        }});
    """)

    # Method 3: Use keyboard shortcut after setting clipboard
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])

    browser.close()
```

---

### Method 10: `dispatch_event()` for Dynamic Inputs

**Best for:** Triggering custom events on inputs that use non-standard event listeners (Angular, custom web components).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Fill the field
    page.locator("#username").fill("john_doe")

    # Dispatch a custom event
    page.locator("#username").dispatch_event("input")
    page.locator("#username").dispatch_event("change")

    # Dispatch with custom event data
    page.locator("#username").dispatch_event("customEvent", {
        "bubbles": True,
        "detail": {"source": "playwright"}
    })

    # Dispatch blur event (simulates user leaving the field)
    page.locator("#username").dispatch_event("blur")

    browser.close()
```

---

## Radio Button Handling

Radio buttons are grouped inputs where only one can be selected at a time.

### HTML Reference

```html
<form>
  <label><input type="radio" name="gender" value="male" /> Male</label>
  <label><input type="radio" name="gender" value="female" /> Female</label>
  <label><input type="radio" name="gender" value="other" /> Other</label>

  <label
    ><input type="radio" name="plan" value="free" id="plan-free" /> Free</label
  >
  <label
    ><input type="radio" name="plan" value="pro" id="plan-pro" /> Pro</label
  >
  <label
    ><input type="radio" name="plan" value="enterprise" id="plan-enterprise" />
    Enterprise</label
  >
</form>
```

---

### Method 1: `check()` (Radio)

**Best for:** The most direct and reliable way to select a radio button.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Check by CSS selector (by value attribute)
    page.locator("input[name='gender'][value='male']").check()

    # Check by ID
    page.locator("#plan-pro").check()

    # Verify the selection
    assert page.locator("input[name='gender'][value='male']").is_checked()

    # Check with force (bypasses actionability checks)
    page.locator("input[name='gender'][value='female']").check(force=True)

    browser.close()
```

---

### Method 2: `click()` (Radio)

**Best for:** When `check()` doesn't work due to custom styling (the actual `<input>` might be hidden and a `<span>` or `<div>` acts as the visible selector).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Click the radio button directly
    page.locator("input[name='gender'][value='female']").click()

    # Click the label (useful when input is hidden)
    page.locator("label:has-text('Female')").click()

    # Click by text content of the label
    page.get_by_text("Male", exact=True).click()

    # Click with position offset (for custom UI radio buttons)
    page.locator(".custom-radio-female").click(position={"x": 10, "y": 10})

    browser.close()
```

---

### Method 3: `is_checked()` (Radio)

**Best for:** Asserting which radio button is currently selected.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    page.locator("input[name='gender'][value='male']").check()

    # Check state
    is_male_selected = page.locator("input[name='gender'][value='male']").is_checked()
    is_female_selected = page.locator("input[name='gender'][value='female']").is_checked()

    print(f"Male selected: {is_male_selected}")     # True
    print(f"Female selected: {is_female_selected}") # False

    # Assert in tests
    assert page.locator("input[name='gender'][value='male']").is_checked(), "Male should be selected"
    assert not page.locator("input[name='gender'][value='female']").is_checked()

    browser.close()
```

---

### Method 4: `evaluate()` (JavaScript Radio)

**Best for:** Programmatically selecting a radio button by its value when the element is hard to reach.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Select radio by value via JavaScript
    page.evaluate("""
        const radios = document.querySelectorAll('input[name="gender"]');
        radios.forEach(radio => {
            if (radio.value === 'female') {
                radio.checked = true;
                radio.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    """)

    # Verify via JS
    selected = page.evaluate("""
        document.querySelector('input[name="gender"]:checked').value
    """)
    print(f"Selected gender: {selected}")  # female

    browser.close()
```

---

### Method 5: Selecting by Value with `locator()`

**Best for:** Dynamically selecting a radio button based on a variable value.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Dynamic selection using a variable
    selected_plan = "pro"

    # Build the selector dynamically
    page.locator(f"input[name='plan'][value='{selected_plan}']").check()

    # Alternative: Using filter
    page.locator("input[name='plan']").filter(has=page.locator(f"[value='{selected_plan}']")).check()

    # Select from a list of options
    options = ["free", "pro", "enterprise"]
    for option in options:
        locator = page.locator(f"input[name='plan'][value='{option}']")
        print(f"Plan '{option}' is checked: {locator.is_checked()}")

    browser.close()
```

---

### Method 6: `get_by_label()` + `check()`

**Best for:** Accessibility-first approach, selecting radio by its associated label text.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Select by exact label text
    page.get_by_label("Male").check()

    # Select by partial label text
    page.get_by_label("Enter").check()

    # Verify using get_by_label
    assert page.get_by_label("Male").is_checked()

    browser.close()
```

---

### Method 7: `get_by_role()` (Radio)

**Best for:** ARIA role-based selection, very robust for accessibility-compliant forms.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Select radio by ARIA role and accessible name
    page.get_by_role("radio", name="Female").check()
    page.get_by_role("radio", name="Pro").check()

    # Verify
    assert page.get_by_role("radio", name="Female").is_checked()
    assert not page.get_by_role("radio", name="Male").is_checked()

    # Get all radio buttons in a group
    all_radios = page.get_by_role("radio").all()
    for radio in all_radios:
        print(f"Radio checked: {radio.is_checked()}")

    browser.close()
```

---

## Checkbox Handling

Checkboxes allow multiple selections simultaneously, unlike radio buttons.

### HTML Reference

```html
<form>
  <label
    ><input type="checkbox" id="terms" name="terms" /> I accept the Terms</label
  >
  <label
    ><input type="checkbox" id="newsletter" name="newsletter" checked />
    Subscribe to newsletter</label
  >

  <input type="checkbox" name="hobby" value="reading" id="hobby-reading" />
  <label for="hobby-reading">Reading</label>

  <input type="checkbox" name="hobby" value="coding" id="hobby-coding" />
  <label for="hobby-coding">Coding</label>

  <input type="checkbox" name="hobby" value="gaming" id="hobby-gaming" />
  <label for="hobby-gaming">Gaming</label>
</form>
```

---

### Method 1: `check()` (Checkbox)

**Best for:** Ensuring a checkbox is checked, regardless of its current state.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Check by ID
    page.locator("#terms").check()

    # Check by CSS attribute selector
    page.locator("input[name='hobby'][value='coding']").check()

    # Check multiple checkboxes
    hobbies = ["reading", "coding", "gaming"]
    for hobby in hobbies:
        page.locator(f"input[name='hobby'][value='{hobby}']").check()

    # check() is idempotent — if already checked, it does nothing
    page.locator("#newsletter").check()  # Already checked — no error

    # Verify
    assert page.locator("#terms").is_checked()

    browser.close()
```

---

### Method 2: `uncheck()`

**Best for:** Ensuring a checkbox is unchecked, regardless of its current state.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Uncheck a checkbox that is currently checked
    page.locator("#newsletter").uncheck()

    # Uncheck by name and value
    page.locator("input[name='hobby'][value='gaming']").uncheck()

    # uncheck() is idempotent — if already unchecked, no error
    page.locator("#terms").uncheck()  # Already unchecked — no error

    # Verify
    assert not page.locator("#newsletter").is_checked()

    # Uncheck with force (bypasses visibility checks)
    page.locator("#hidden-checkbox").uncheck(force=True)

    browser.close()
```

---

### Method 3: `click()` (Checkbox)

**Best for:** Toggling a checkbox (from checked to unchecked or vice versa), or clicking associated label elements.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Toggle checkbox
    page.locator("#terms").click()         # Unchecked → Checked
    page.locator("#terms").click()         # Checked → Unchecked

    # Click the label instead of the checkbox (useful for styled checkboxes)
    page.locator("label[for='terms']").click()

    # Click by label text
    page.get_by_text("I accept the Terms").click()

    # Click with custom position
    page.locator(".custom-checkbox").click(position={"x": 5, "y": 5})

    browser.close()
```

> ⚠️ **Warning:** `click()` **toggles** state. Prefer `check()` / `uncheck()` when you need a guaranteed final state.

---

### Method 4: `set_checked()`

**Best for:** Setting checkbox state conditionally using a boolean, combining `check()` and `uncheck()` into one method.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Set to checked
    page.locator("#terms").set_checked(True)

    # Set to unchecked
    page.locator("#newsletter").set_checked(False)

    # Use with dynamic boolean values
    user_wants_newsletter = True
    page.locator("#newsletter").set_checked(user_wants_newsletter)

    user_accepts_terms = False
    page.locator("#terms").set_checked(user_accepts_terms)

    # Practical use: configure checkboxes from a dictionary
    preferences = {
        "#terms": True,
        "#newsletter": False,
        "#hobby-reading": True,
        "#hobby-coding": True,
        "#hobby-gaming": False,
    }

    for selector, should_check in preferences.items():
        page.locator(selector).set_checked(should_check)

    browser.close()
```

---

### Method 5: `is_checked()` (Checkbox)

**Best for:** Reading the current checked state of a checkbox for assertions or logic.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Check and verify
    page.locator("#terms").check()
    is_terms_checked = page.locator("#terms").is_checked()
    print(f"Terms checked: {is_terms_checked}")  # True

    # Conditional logic based on state
    if not page.locator("#newsletter").is_checked():
        page.locator("#newsletter").check()
        print("Newsletter was unchecked — now checked!")

    # Collect all checked hobby values
    all_hobbies = ["reading", "coding", "gaming"]
    selected_hobbies = []

    for hobby in all_hobbies:
        if page.locator(f"input[name='hobby'][value='{hobby}']").is_checked():
            selected_hobbies.append(hobby)

    print(f"Selected hobbies: {selected_hobbies}")

    browser.close()
```

---

### Method 6: `evaluate()` (JavaScript Checkbox)

**Best for:** Programmatic state changes or reading checkbox states in bulk using JavaScript.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Check via JavaScript
    page.evaluate("""
        const checkbox = document.querySelector('#terms');
        checkbox.checked = true;
        checkbox.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    # Uncheck via JavaScript
    page.evaluate("""
        const checkbox = document.querySelector('#newsletter');
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    # Get all checked checkboxes' values
    checked_values = page.evaluate("""
        Array.from(document.querySelectorAll('input[name="hobby"]:checked'))
             .map(el => el.value)
    """)
    print(f"Checked hobbies: {checked_values}")

    # Check all checkboxes with a given name
    page.evaluate("""
        document.querySelectorAll('input[name="hobby"]').forEach(cb => {
            cb.checked = true;
            cb.dispatchEvent(new Event('change', { bubbles: true }));
        });
    """)

    browser.close()
```

---

### Method 7: `get_by_label()` + `check()` (Checkbox)

**Best for:** Accessible checkbox selection using label text.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # Check by label text (exact)
    page.get_by_label("I accept the Terms").check()

    # Check by partial label text
    page.get_by_label("newsletter").check()

    # Check by label — case insensitive using regex
    import re
    page.get_by_label(re.compile("reading", re.IGNORECASE)).check()

    # Verify
    assert page.get_by_label("I accept the Terms").is_checked()
    assert not page.get_by_label("Subscribe to newsletter").is_checked()

    browser.close()
```

---

### Method 8: Checking Multiple Checkboxes in a Loop

**Best for:** Handling dynamic lists of checkboxes, bulk operations.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com/form")

    # --- Method A: Loop by value ---
    hobbies_to_select = ["reading", "coding"]
    for hobby in hobbies_to_select:
        page.locator(f"input[name='hobby'][value='{hobby}']").check()

    # --- Method B: Using locator.all() to get all checkboxes ---
    all_checkboxes = page.locator("input[type='checkbox']").all()
    print(f"Total checkboxes on page: {len(all_checkboxes)}")

    for checkbox in all_checkboxes:
        print(f"  Checked: {checkbox.is_checked()}")

    # --- Method C: Check all checkboxes on the page ---
    page.locator("input[type='checkbox']").all()
    for cb in page.locator("input[type='checkbox']").all():
        cb.check()

    # --- Method D: Uncheck all ---
    for cb in page.locator("input[type='checkbox']").all():
        cb.uncheck()

    # --- Method E: Dictionary-driven configuration ---
    checkbox_config = {
        "input[name='hobby'][value='reading']": True,
        "input[name='hobby'][value='coding']":  True,
        "input[name='hobby'][value='gaming']":  False,
        "#terms":                               True,
        "#newsletter":                          False,
    }

    for selector, state in checkbox_config.items():
        page.locator(selector).set_checked(state)

    # --- Verify all ---
    for selector, expected_state in checkbox_config.items():
        actual = page.locator(selector).is_checked()
        assert actual == expected_state, f"Mismatch for {selector}"
        print(f"✓ {selector}: {actual}")

    browser.close()
```

---

## Combining All Elements — Full Form Example

Here is a complete, real-world example combining input boxes, radio buttons, and checkboxes in a single registration form workflow.

```python
from playwright.sync_api import sync_playwright
import re

def fill_registration_form(page):
    """
    Fill a complete user registration form with all element types.

    Assumed HTML form structure:
    - Text inputs: #first-name, #last-name, #email, #password
    - Textarea: #bio
    - Radio group: input[name='gender'] with values male/female/other
    - Radio group: input[name='plan'] with values free/pro/enterprise
    - Checkboxes: #terms, #newsletter, input[name='hobby'] with values reading/coding/gaming
    """

    print("Step 1: Filling text input fields...")

    # Fill basic text inputs
    page.locator("#first-name").fill("John")
    page.locator("#last-name").fill("Doe")
    page.locator("#email").fill("john.doe@example.com")

    # Type password with simulated keystrokes
    page.locator("#password").press_sequentially("SecurePass@123", delay=50)

    # Fill multi-line textarea
    page.locator("#bio").fill(
        "Hello! I am John Doe.\n"
        "I love Python, automation, and building web applications.\n"
        "Playwright is my go-to tool for browser automation."
    )

    print("Step 2: Selecting gender via radio button...")

    # Select gender using CSS selector
    page.locator("input[name='gender'][value='male']").check()
    assert page.locator("input[name='gender'][value='male']").is_checked(), \
        "Gender should be 'male'"

    print("Step 3: Selecting subscription plan via radio button...")

    # Select plan using get_by_role (accessibility-first)
    page.get_by_role("radio", name="Pro").check()
    assert page.get_by_role("radio", name="Pro").is_checked(), \
        "Plan should be 'Pro'"

    print("Step 4: Configuring checkboxes...")

    # Accept terms (required)
    page.get_by_label("I accept the Terms").check()

    # Opt out of newsletter
    if page.locator("#newsletter").is_checked():
        page.locator("#newsletter").uncheck()

    # Select hobbies using dictionary-driven approach
    hobby_config = {
        "reading": True,
        "coding":  True,
        "gaming":  False,
    }

    for hobby, should_check in hobby_config.items():
        page.locator(f"input[name='hobby'][value='{hobby}']").set_checked(should_check)

    print("Step 5: Verifying all form values before submission...")

    # Verify inputs
    assert page.locator("#first-name").input_value() == "John"
    assert page.locator("#last-name").input_value() == "Doe"
    assert page.locator("#email").input_value() == "john.doe@example.com"
    assert page.locator("#password").input_value() == "SecurePass@123"
    assert "John Doe" in page.locator("#bio").input_value()

    # Verify radio buttons
    assert page.locator("input[name='gender'][value='male']").is_checked()
    assert page.get_by_role("radio", name="Pro").is_checked()

    # Verify checkboxes
    assert page.locator("#terms").is_checked()
    assert not page.locator("#newsletter").is_checked()
    assert page.locator("input[name='hobby'][value='reading']").is_checked()
    assert page.locator("input[name='hobby'][value='coding']").is_checked()
    assert not page.locator("input[name='hobby'][value='gaming']").is_checked()

    print("Step 6: Submitting the form...")
    page.locator("button[type='submit']").click()

    # Wait for navigation or success message
    page.wait_for_url("**/success**", timeout=5000)
    print("✅ Form submitted successfully!")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://example.com/register")
        page.wait_for_load_state("networkidle")

        fill_registration_form(page)

        browser.close()


if __name__ == "__main__":
    main()
```

---

## Locator Strategies Summary

Playwright offers multiple ways to locate elements. Here's a quick reference:

| Strategy               | Example                                          | Best Used For            |
| ---------------------- | ------------------------------------------------ | ------------------------ |
| CSS Selector           | `page.locator("#id")`                            | IDs, classes, attributes |
| XPath                  | `page.locator("//input[@name='email']")`         | Complex DOM traversal    |
| `get_by_label()`       | `page.get_by_label("Email")`                     | Form fields with labels  |
| `get_by_role()`        | `page.get_by_role("checkbox", name="Terms")`     | ARIA-compliant forms     |
| `get_by_text()`        | `page.get_by_text("Submit")`                     | Buttons, labels by text  |
| `get_by_placeholder()` | `page.get_by_placeholder("Enter email")`         | Input fields             |
| `get_by_test_id()`     | `page.get_by_test_id("submit-btn")`              | `data-testid` attributes |
| Attribute Filter       | `page.locator("[name='gender'][value='male']")`  | Radio/checkbox by value  |
| `filter()`             | `page.locator("input").filter(has_text="Email")` | Scoped filtering         |

---

## Best Practices

### 1. Prefer `locator()` over `page.fill()` (Modern API)

```python
# ❌ Old way
page.fill("#username", "john")

# ✅ Modern way
page.locator("#username").fill("john")
```

### 2. Use Accessibility Locators When Possible

```python
# ✅ Role + name (most robust)
page.get_by_role("checkbox", name="Accept Terms").check()
page.get_by_label("Email address").fill("test@example.com")
```

### 3. Use `set_checked()` for Conditional State

```python
# ✅ Use set_checked with boolean
page.locator("#newsletter").set_checked(user_prefers_newsletter)
```

### 4. Always Verify After Interaction

```python
page.locator("#terms").check()
assert page.locator("#terms").is_checked(), "Terms checkbox must be checked"
```

### 5. Add Waits for Dynamic Forms

```python
# Wait for element to be visible before interacting
page.locator("#dynamic-input").wait_for(state="visible")
page.locator("#dynamic-input").fill("value")
```

### 6. Use `slow_mo` During Development

```python
browser = p.chromium.launch(headless=False, slow_mo=300)
```

### 7. Use `force=True` Sparingly

```python
# Only when element is covered or hidden intentionally
page.locator("#hidden-checkbox").check(force=True)
```

---

## Common Errors & Fixes

### Error: `TimeoutError: Waiting for locator to be visible`

**Cause:** Element not yet in DOM or is hidden.

```python
# Fix: Wait for the element first
page.locator("#username").wait_for(state="visible", timeout=10000)
page.locator("#username").fill("john")
```

---

### Error: `Element is not an input[type=checkbox]`

**Cause:** Trying to `check()` on a non-checkbox element.

```python
# Fix: Use click() on the label or wrapper div instead
page.locator("label.custom-checkbox").click()
```

---

### Error: `Checkbox is already checked`

**Cause:** Calling `check()` on something that isn't a checkbox/radio.

```python
# Fix: Use set_checked() which handles both states safely
page.locator("#my-toggle").set_checked(True)
```

---

### Error: React/Vue input not updating

**Cause:** `fill()` doesn't trigger framework-specific events in some cases.

```python
# Fix: Use evaluate() to trigger React's synthetic events
page.evaluate("""
    const input = document.querySelector('#react-input');
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value').set;
    nativeInputValueSetter.call(input, 'new value');
    input.dispatchEvent(new Event('input', { bubbles: true }));
""")
```

---

### Error: `strict mode violation — multiple elements matched`

**Cause:** Locator matches more than one element.

```python
# Fix: Use .first, .last, or .nth() to be specific
page.locator("input[type='text']").first.fill("john")
page.locator("input[type='checkbox']").nth(2).check()
```

---

_Generated with Python Playwright v1.40+ | Playwright Docs: https://playwright.dev/python/_
