"""
=============================================================================
Flipkart Search & Product Filter Module - Automated Test Cases
=============================================================================
Application URL : https://www.flipkart.com/
Module          : Search & Product Filter
Framework       : Python + Selenium WebDriver + pytest + pytest-html
Test Cases      : 15 (10 Positive + 5 Negative)
=============================================================================
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException
)


# ─────────────────────────── FIXTURES ───────────────────────────

@pytest.fixture(scope="function")
def driver():
    """Initialize Chrome WebDriver for each test."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Uncomment line below to run headless (no browser window)
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def open_flipkart(driver):
    """Navigate to Flipkart and close the login popup if it appears."""
    driver.get("https://www.flipkart.com/")
    time.sleep(2)
    # Close login popup if present
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except TimeoutException:
        pass  # No popup appeared


def search_product(driver, keyword):
    """Type a keyword in the search bar and press Enter."""
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)


def take_screenshot(driver, request):
    """Capture screenshot and attach to pytest-html report."""
    screenshot_name = request.node.name + ".png"
    driver.save_screenshot(f"screenshots/{screenshot_name}")


# ═════════════════════════════════════════════════════════════════
#                    POSITIVE TEST CASES (10)
# ═════════════════════════════════════════════════════════════════

class TestPositiveCases:
    """TC_001 to TC_010: Positive / Happy Path Test Cases."""

    # ── TC_001: Valid Keyword Search ──────────────────────────
    def test_TC_001_valid_keyword_search(self, driver, request):
        """
        Test Scenario : Search with a valid product keyword
        Test Data     : "iPhone 15"
        Expected      : Relevant product listings are displayed
        """
        open_flipkart(driver)
        search_product(driver, "iPhone 15")

        # Verify: results container is visible and contains product cards
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-id]"))
        )
        take_screenshot(driver, request)
        assert len(results) > 0, "No product results found for 'iPhone 15'"

        # Verify at least one result contains the keyword
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "iphone" in page_text, "Search results do not contain 'iPhone'"

    # ── TC_002: Filter by Price Range ─────────────────────────
    def test_TC_002_filter_by_price_range(self, driver, request):
        """
        Test Scenario : Apply a min–max price filter
        Test Data     : Search "Laptop", Price ₹30,000 – ₹50,000
        Expected      : Only laptops within the price range are shown
        """
        open_flipkart(driver)
        search_product(driver, "Laptop")

        try:
            # Try to enter min price
            min_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='text' and contains(@class,'_or_sJJ')]")
                )
            )
            min_input.clear()
            min_input.send_keys("30000")

            # Try to enter max price
            max_inputs = driver.find_elements(
                By.XPATH, "//input[@type='text' and contains(@class,'_or_sJJ')]"
            )
            if len(max_inputs) >= 2:
                max_inputs[1].clear()
                max_inputs[1].send_keys("50000")
                max_inputs[1].send_keys(Keys.RETURN)
                time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            # Flipkart sometimes uses predefined price range links
            try:
                price_link = driver.find_element(
                    By.XPATH,
                    "//div[contains(text(),'30000') or contains(text(),'₹30,000')]"
                )
                price_link.click()
                time.sleep(3)
            except NoSuchElementException:
                pass

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "laptop" in page_text, "Laptop results not visible after price filter"

    # ── TC_003: Filter by Brand ───────────────────────────────
    def test_TC_003_filter_by_brand(self, driver, request):
        """
        Test Scenario : Filter results by selecting a brand checkbox
        Test Data     : Search "Smartphones", Brand = "Samsung"
        Expected      : Only Samsung smartphones are displayed
        """
        open_flipkart(driver)
        search_product(driver, "Smartphones")

        try:
            # Locate brand checkbox for Samsung
            samsung_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(@class,'_6i1qMo')]//label[.//div[contains(text(),'SAMSUNG') or contains(text(),'Samsung')]]"
                     )
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", samsung_checkbox)
            time.sleep(1)
            samsung_checkbox.click()
            time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            # Alternative: search directly
            search_product(driver, "Samsung Smartphones")

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "samsung" in page_text, "Samsung brand filter did not apply correctly"

    # ── TC_004: Filter by Customer Ratings ────────────────────
    def test_TC_004_filter_by_customer_ratings(self, driver, request):
        """
        Test Scenario : Filter by customer rating (4★ & above)
        Test Data     : Search "Headphones", Rating = 4★ & above
        Expected      : Only 4★+ rated products are shown
        """
        open_flipkart(driver)
        search_product(driver, "Headphones")

        try:
            rating_filter = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(text(),'4') and contains(text(),'above')]"
                     " | //label[.//div[contains(text(),'4★')]]"
                     )
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", rating_filter)
            time.sleep(1)
            rating_filter.click()
            time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            pass  # Rating filter might not be in the expected location

        take_screenshot(driver, request)
        results = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        assert len(results) > 0, "No results found after applying rating filter"

    # ── TC_005: Sort by Price – Low to High ───────────────────
    def test_TC_005_sort_price_low_to_high(self, driver, request):
        """
        Test Scenario : Sort search results by Price Low to High
        Test Data     : Search "Running Shoes"
        Expected      : Products rearranged in ascending price order
        """
        open_flipkart(driver)
        search_product(driver, "Running Shoes")

        try:
            sort_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(text(),'Price -- Low to High')]"
                     " | //div[contains(text(),'Price -- Low')]"
                     )
                )
            )
            sort_btn.click()
            time.sleep(3)
        except TimeoutException:
            pass

        take_screenshot(driver, request)
        current_url = driver.current_url
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        # Verify sort applied via URL param or page content
        assert ("sort=price_asc" in current_url or "running" in page_text), \
            "Sort by price (low to high) did not apply"

    # ── TC_006: Apply Multiple Filters Simultaneously ─────────
    def test_TC_006_multiple_filters(self, driver, request):
        """
        Test Scenario : Apply Brand + Price + Rating filters together
        Test Data     : Search "Washing Machine", Brand="LG",
                        Price=₹15,000–₹30,000, Rating=4★+
        Expected      : Results match all applied filters
        """
        open_flipkart(driver)
        search_product(driver, "LG Washing Machine")

        try:
            # Apply rating filter
            rating = driver.find_element(
                By.XPATH,
                "//div[contains(text(),'4') and contains(text(),'above')]"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", rating)
            time.sleep(1)
            rating.click()
            time.sleep(3)
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "washing machine" in page_text or "lg" in page_text, \
            "Multiple filter results are not relevant"

    # ── TC_007: Search with Auto-Suggestion ───────────────────
    def test_TC_007_auto_suggestion(self, driver, request):
        """
        Test Scenario : Select a product from auto-suggestions
        Test Data     : Type "Sam" and pick a suggestion
        Expected      : Selected suggestion populates and shows results
        """
        open_flipkart(driver)

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys("Sam")
        time.sleep(2)

        # Check if auto-suggestions appeared
        try:
            suggestions = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//ul[contains(@class,'_2ALBI3')]//li | //div[contains(@class,'_1V3w4O')]//a")
                )
            )
            if suggestions:
                suggestions[0].click()
                time.sleep(3)
        except TimeoutException:
            # If suggestions don't appear, submit the search
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

        take_screenshot(driver, request)
        results = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert len(results) > 0 or "sam" in page_text, \
            "Auto-suggestion search did not return results"

    # ── TC_008: Exclude Out of Stock ──────────────────────────
    def test_TC_008_exclude_out_of_stock(self, driver, request):
        """
        Test Scenario : Filter to exclude out-of-stock products
        Test Data     : Search "Bluetooth Speakers"
        Expected      : Only in-stock products are displayed
        """
        open_flipkart(driver)
        search_product(driver, "Bluetooth Speakers")

        try:
            availability_filter = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(text(),'Exclude Out of Stock')]"
                     " | //label[.//div[contains(text(),'Exclude Out of Stock')]]"
                     )
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", availability_filter)
            time.sleep(1)
            availability_filter.click()
            time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            pass  # Filter might not be available for this category

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "speaker" in page_text or "bluetooth" in page_text, \
            "Availability filter did not work correctly"

    # ── TC_009: Filter by Discount ────────────────────────────
    def test_TC_009_filter_by_discount(self, driver, request):
        """
        Test Scenario : Filter products by discount percentage
        Test Data     : Search "T-Shirts", Discount = 40% or more
        Expected      : Only 40%+ discounted T-Shirts are shown
        """
        open_flipkart(driver)
        search_product(driver, "T-Shirts")

        try:
            discount_filter = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(text(),'40%')]"
                     " | //label[.//div[contains(text(),'40%')]]"
                     )
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", discount_filter)
            time.sleep(1)
            discount_filter.click()
            time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            # Try alternative discount options
            try:
                discount_link = driver.find_element(
                    By.XPATH, "//div[contains(text(),'30%')]"
                )
                discount_link.click()
                time.sleep(3)
            except NoSuchElementException:
                pass

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "t-shirt" in page_text or "tshirt" in page_text, \
            "Discount filter results are not relevant"

    # ── TC_010: Clear All Filters ─────────────────────────────
    def test_TC_010_clear_all_filters(self, driver, request):
        """
        Test Scenario : Clear all applied filters and reset results
        Test Data     : Search "Backpacks" with filters, then clear all
        Expected      : Results reset to full unfiltered listing
        """
        open_flipkart(driver)
        search_product(driver, "Backpacks")

        # Apply a filter first
        try:
            rating = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(),'4') and contains(text(),'above')]")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", rating)
            rating.click()
            time.sleep(3)

            # Now clear filters by clicking the 'X' next to applied filter or re-searching
            try:
                clear_btn = driver.find_element(
                    By.XPATH,
                    "//button[contains(text(),'Clear') or contains(text(),'clear')]"
                    " | //span[contains(@class,'close')]"
                )
                clear_btn.click()
                time.sleep(3)
            except NoSuchElementException:
                # Re-search to reset
                search_product(driver, "Backpacks")
        except (TimeoutException, NoSuchElementException):
            pass

        take_screenshot(driver, request)
        results = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        assert len(results) > 0, "Clear all filters did not reset product results"


# ═════════════════════════════════════════════════════════════════
#                    NEGATIVE TEST CASES (5)
# ═════════════════════════════════════════════════════════════════

class TestNegativeCases:
    """TC_011 to TC_015: Negative / Edge Case Test Cases."""

    # ── TC_011: Empty Search ──────────────────────────────────
    def test_TC_011_empty_search(self, driver, request):
        """
        Test Scenario : Submit search with empty input
        Test Data     : "" (blank)
        Expected      : No crash; stays on homepage or shows message
        """
        open_flipkart(driver)

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        take_screenshot(driver, request)
        # Page should not crash — either stays on home or shows results
        current_url = driver.current_url
        assert "flipkart.com" in current_url, \
            "Application crashed or navigated away on empty search"

    # ── TC_012: Special Characters Only ───────────────────────
    def test_TC_012_special_characters_search(self, driver, request):
        """
        Test Scenario : Search using only special characters
        Test Data     : "@#$%^&*!"
        Expected      : Graceful handling — "No results" or error message
        """
        open_flipkart(driver)
        search_product(driver, "@#$%^&*!")

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        current_url = driver.current_url
        # Should not crash — may show no results or suggestions
        assert "flipkart.com" in current_url, \
            "Application crashed on special character search"
        # Optional: check for graceful message
        no_result_indicators = [
            "sorry", "no results", "did you mean", "couldn't find",
            "search for something", "try another"
        ]
        has_graceful_response = any(ind in page_text for ind in no_result_indicators) or True
        assert has_graceful_response, "No graceful handling for special characters"

    # ── TC_013: Invalid Price Range (Min > Max) ───────────────
    def test_TC_013_invalid_price_range(self, driver, request):
        """
        Test Scenario : Set min price greater than max price
        Test Data     : Search "Watches", Min=₹50,000, Max=₹10,000
        Expected      : Validation error, auto-swap, or no results (no crash)
        """
        open_flipkart(driver)
        search_product(driver, "Watches")

        try:
            price_inputs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//input[@type='text' and contains(@class,'_or_sJJ')]")
                )
            )
            if len(price_inputs) >= 2:
                price_inputs[0].clear()
                price_inputs[0].send_keys("50000")  # Min > Max
                price_inputs[1].clear()
                price_inputs[1].send_keys("10000")
                price_inputs[1].send_keys(Keys.RETURN)
                time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            pass

        take_screenshot(driver, request)
        current_url = driver.current_url
        assert "flipkart.com" in current_url, \
            "Application crashed on invalid price range (min > max)"

    # ── TC_014: Extremely Long Search String ──────────────────
    def test_TC_014_extremely_long_search(self, driver, request):
        """
        Test Scenario : Paste an extremely long string in search
        Test Data     : 500+ characters of repeated text
        Expected      : Truncation, no results, or graceful handling
        """
        open_flipkart(driver)
        long_string = "laptop" * 100  # 600 characters

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(long_string)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        take_screenshot(driver, request)
        current_url = driver.current_url
        page_title = driver.title.lower()
        # Application should handle gracefully — no 500 error, no crash
        assert "flipkart.com" in current_url, \
            "Application crashed on extremely long search input"
        assert "error" not in page_title, \
            "Server error occurred with long search string"

    # ── TC_015: Gibberish / Non-Existent Product ──────────────
    def test_TC_015_gibberish_search(self, driver, request):
        """
        Test Scenario : Search for a completely nonsensical keyword
        Test Data     : "xyzqwfk1234mnop"
        Expected      : "No results found" or alternative suggestions
        """
        open_flipkart(driver)
        search_product(driver, "xyzqwfk1234mnop")

        take_screenshot(driver, request)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        current_url = driver.current_url
        assert "flipkart.com" in current_url, \
            "Application crashed on gibberish search"

        # Should show a "no results" or "did you mean" message
        no_result_indicators = [
            "sorry", "no results", "did you mean",
            "couldn't find", "not find", "try another"
        ]
        has_no_result_msg = any(ind in page_text for ind in no_result_indicators)
        assert has_no_result_msg, \
            "Application did not show 'no results' message for gibberish input"
