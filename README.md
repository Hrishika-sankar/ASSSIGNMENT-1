# Flipkart Search & Product Filter — Automated Test Suite

## Overview
Automated test cases for the **Search & Product Filter module** of Flipkart
(https://www.flipkart.com/) using **Python + Selenium WebDriver + pytest**.

Includes **15 test cases**: 10 Positive + 5 Negative, with automatic HTML
report generation and screenshot capture.

---

## Test Cases Summary

| ID      | Type     | Scenario                              |
|---------|----------|---------------------------------------|
| TC_001  | Positive | Valid keyword search                  |
| TC_002  | Positive | Filter by price range                 |
| TC_003  | Positive | Filter by brand name                  |
| TC_004  | Positive | Filter by customer ratings            |
| TC_005  | Positive | Sort by price (Low to High)           |
| TC_006  | Positive | Apply multiple filters simultaneously |
| TC_007  | Positive | Search with auto-suggestion           |
| TC_008  | Positive | Exclude out-of-stock products         |
| TC_009  | Positive | Filter by discount percentage         |
| TC_010  | Positive | Clear all applied filters             |
| TC_011  | Negative | Empty / blank search                  |
| TC_012  | Negative | Special characters only               |
| TC_013  | Negative | Invalid price range (Min > Max)       |
| TC_014  | Negative | Extremely long search string          |
| TC_015  | Negative | Gibberish / non-existent product      |

---

## Prerequisites

1. **Python 3.8+** installed
2. **Google Chrome** browser installed
3. **ChromeDriver** matching your Chrome version
   - Option A: Download manually from https://chromedriver.chromium.org/
   - Option B: Let `webdriver-manager` handle it automatically

---

## Setup Instructions

### Step 1: Clone / Download this project
Place all files in a folder (e.g., `flipkart_tests/`)

### Step 2: Install dependencies
```bash
cd flipkart_tests
pip install -r requirements.txt
```

### Step 3: Run all tests and generate HTML report
```bash
pytest test_flipkart_search_filter.py -v --html=report.html --self-contained-html
```

### Step 4: Run a specific test case
```bash
# Run only TC_001
pytest test_flipkart_search_filter.py::TestPositiveCases::test_TC_001_valid_keyword_search -v

# Run only negative cases
pytest test_flipkart_search_filter.py::TestNegativeCases -v
```

### Step 5: Run headless (no browser window)
Uncomment line 30 in `test_flipkart_search_filter.py`:
```python
options.add_argument("--headless=new")
```

---

## Output Files

| File/Folder      | Description                          |
|------------------|--------------------------------------|
| `report.html`    | HTML test report with Pass/Fail/Screenshots |
| `screenshots/`   | Individual PNG screenshots per test  |

---

## Project Structure
```
flipkart_tests/
├── test_flipkart_search_filter.py   # All 15 test cases
├── conftest.py                       # Report config + screenshot hooks
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── report.html                       # Generated after running tests
└── screenshots/                      # Auto-captured screenshots
```

---

## Notes
- Flipkart's UI class names may change over time. If a test fails due to
  element not found, inspect the page and update the XPath/CSS selectors.
- The login popup is automatically dismissed when detected.
- Each test function is independent and opens a fresh browser session.
- Screenshots are embedded directly into the HTML report.
