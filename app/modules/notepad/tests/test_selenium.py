from selenium.common.exceptions import NoSuchElementException
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_notepad_index():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        driver.get("http://127.0.0.1:5000/notepad")
        driver.set_window_size(1011, 833)
        driver.find_element(By.LINK_TEXT, "Edit").click()
        driver.find_element(By.ID, "title").click()
        driver.find_element(By.ID, "title").send_keys("Practica EGC Selenium")
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").click()
        element = driver.find_element(By.ID, "body")
        actions = ActionChains(driver)
        actions.double_click(element).perform()
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").send_keys("Prueba selenium")
        driver.find_element(By.ID, "submit").click()

    except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


# Call the test function
test_notepad_index()
