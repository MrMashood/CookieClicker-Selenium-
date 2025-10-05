"""
Cookie Clicker auto-clicker using Selenium + Brave (Chromium).
- Works with Selenium Manager (no webdriver-manager needed).
- Hardened against DOM refreshes (stale element references).
- Keeps window open if script exits unexpectedly (detach=True).
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
import time

# === Configuration ===
# If Brave is installed elsewhere, change this path or set BRAVE_PATH env var.
BRAVE_PATH = os.getenv(
    "BRAVE_PATH",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
)

if not os.path.exists(BRAVE_PATH):
    raise FileNotFoundError(
        f"Brave not found at: {BRAVE_PATH}\n"
        "Update BRAVE_PATH in main.py or set the BRAVE_PATH environment variable."
    )

# Selenium/Brave options
options = Options()
options.binary_location = BRAVE_PATH
# Keep the window open even if the Python process exits
options.add_experimental_option("detach", True)
# Optional: faster page load strategy
# options.page_load_strategy = "eager"

# Launch ChromeDriver via Selenium Manager (auto-downloads matching driver)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# === Target page ===
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Element IDs / prefixes
COOKIE_ID = "bigCookie"
COOKIES_ID = "cookies"
PRODUCT_PRICE_PREFIX = "productPrice"
PRODUCT_PREFIX = "product"

# 1) Pick language (this often causes a re-render)
wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'English')]"))).click()

# 2) Wait until the big cookie is actually clickable (not just present)
wait.until(EC.element_to_be_clickable((By.ID, COOKIE_ID)))


def safe_get_text(by, value, attempts=3, pause=0.1):
    """Read text while handling staleness and transient DOM states."""
    for _ in range(attempts):
        try:
            return driver.find_element(by, value).text
        except StaleElementReferenceException:
            time.sleep(pause)
    # final attempt with an explicit wait
    return wait.until(EC.presence_of_element_located((by, value))).text


def safe_click(by, value, attempts=3, pause=0.1):
    """Click element, retrying if it goes stale."""
    for _ in range(attempts):
        try:
            el = wait.until(EC.element_to_be_clickable((by, value)))
            el.click()
            return True
        except StaleElementReferenceException:
            time.sleep(pause)
    return False


# 3) Main loop: re-find elements each time & guard for staleness
try:
    while True:
        # Re-locate the cookie for each click cycle (prevents stale refs)
        try:
            cookie = wait.until(EC.element_to_be_clickable((By.ID, COOKIE_ID)))
            cookie.click()
        except (StaleElementReferenceException, TimeoutException):
            # if the DOM refreshed, just try again
            continue

        # Parse cookies count (guard for staleness and non-numeric transient text)
        try:
            cookies_text = safe_get_text(By.ID, COOKIES_ID).split(" ")[0]
            cookies_count = int(cookies_text.replace(",", ""))
        except Exception:
            # sometimes the counter briefly shows non-numeric text; skip this tick
            continue

        # Try buying first affordable product among first N slots
        for i in range(8):  # try more than 4 slots; adjust as you like
            try:
                price_text = safe_get_text(By.ID, f"{PRODUCT_PRICE_PREFIX}{i}").replace(",", "")
                if not price_text.isdigit():
                    continue
                if cookies_count >= int(price_text):
                    safe_click(By.ID, f"{PRODUCT_PREFIX}{i}")
                    break
            except Exception:
                # ignore transient issues and continue clicking
                continue

        # tiny sleep to avoid pegging CPU (tune as desired)
        time.sleep(0.01)

except KeyboardInterrupt:
    # let you Ctrl+C to stop without closing (because of detach=True)
    pass
