from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


username = "performance_glitch_user"
password = "secret_sauce"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    return driver

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def test_cart(driver, username, password):
    results = {"tests": {}}
    try:
        try:
            wait_for_element(driver, By.ID, "user-name").send_keys(username)
            wait_for_element(driver, By.ID, "password").send_keys(password)
            wait_for_element(driver, By.ID, "login-button").click()
            time.sleep(2)
            if "inventory.html" not in driver.current_url:
                raise Exception("Login failed. Redirected to incorrect page.")
            results["tests"]["Login"] = "PASS"
        except Exception as e:
            results["tests"]["Login"] = f"FAIL: {e}"
            driver.quit()
            return results

        try:
            add_to_cart_button = wait_for_element(driver, By.CSS_SELECTOR, ".btn_inventory")
            add_to_cart_button.click()
            results["tests"]["Add to Cart button present"] = "PASS"
        except Exception as e:
            results["tests"]["Add to Cart button present"] = f"FAIL: {e}"

        try:
            wait_for_element(driver, By.CSS_SELECTOR, ".shopping_cart_link").click()
            time.sleep(2) 
            results["tests"]["Navigate to cart page"] = "PASS"
        except Exception as e:
            results["tests"]["Navigate to cart page"] = f"FAIL: {e}"

        try:
            quantity = wait_for_element(driver, By.CSS_SELECTOR, ".cart_quantity").text
            if quantity == "1":
                results["tests"]["Product quantity shown"] = "PASS"
            else:
                results["tests"]["Product quantity shown"] = f"FAIL: Incorrect quantity"
        except Exception as e:
            results["tests"]["Product quantity shown"] = f"FAIL: {e}"

        try:
            price = wait_for_element(driver, By.CSS_SELECTOR, ".inventory_item_price").text
            if price:
                results["tests"]["Product price shown"] = f"PASS: {price}"
            else:
                results["tests"]["Product price shown"] = "FAIL: Price not visible"
        except Exception as e:
            results["tests"]["Product price shown"] = f"FAIL: {e}"
        try:
            total_price_element = wait_for_element(driver, By.CSS_SELECTOR, ".summary_total_label")
            total_price = total_price_element.text
            if total_price:
                results["tests"]["Total price shown"] = f"PASS: {total_price}"
            else:
                results["tests"]["Total price shown"] = "FAIL: Missing"
        except Exception as e:
            results["tests"]["Total price shown"] = f"FAIL: {e}"

    except Exception as e:
        results["tests"]["General Failure"] = f"FAIL: {e}"
    finally:
        driver.quit()

    return results
if __name__ == "__main__":
    driver = setup_driver()
    test_results = test_cart(driver, username, password)
    print("Results for performance_user:")
    for test, status in test_results["tests"].items():
        print(f"  {test}: {status}")
