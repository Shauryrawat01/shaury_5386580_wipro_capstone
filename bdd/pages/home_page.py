from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from utilities.logger import setup_logger


class HomePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 20)
        self.logger = setup_logger("HomePage")

    # Locators

    buy_tab = (
        By.ID,
        "inPageSearchForm_0"
    )

    rent_tab = (
        By.ID,
        "inPageSearchForm_1"
    )

    projects_tab = (
        By.ID,
        "inPageSearchForm_5"
    )

    search_box = (
        By.ID,
        "keyword2"
    )

    search_button = (
        By.ID,
        "searchform_search_btn"
    )
    
    suggestions_list = (
        By.CSS_SELECTOR,
        "div[class*='suggester'] li, div[class*='component__suggestItem'], .suggester-container li"
    )

    # Actions
    def click_buy_tab(self):
        self.logger.info("Clicking on Buy tab")
        self.wait.until(
            EC.element_to_be_clickable(self.buy_tab)
        ).click()

    def click_rent_tab(self):
        self.logger.info("Clicking on Rent tab")
        self.wait.until(
            EC.element_to_be_clickable(self.rent_tab)
        ).click()

    def click_projects_tab(self):
        self.logger.info("Clicking on Projects tab")
        try:
            tab = self.wait.until(EC.element_to_be_clickable(self.projects_tab))
            self.driver.execute_script("arguments[0].click();", tab)
        except Exception as e:
            self.logger.error(f"Failed to click Projects tab: {e}")

    def enter_location(self, location):
        self.logger.info(f"Entering location: {location}")
        search = self.wait.until(
            EC.visibility_of_element_located(self.search_box)
        )
        search.click()
        search.clear()
        for char in location:
            search.send_keys(char)
            time.sleep(0.1)
        time.sleep(3) 

    def select_location(self):
        self.logger.info("Selecting location from suggestions")
        try:
            suggestions = self.driver.find_elements(*self.suggestions_list)
            if suggestions:
                self.logger.info(f"Found {len(suggestions)} suggestions, clicking the first one")
                self.driver.execute_script("arguments[0].click();", suggestions[0])
            else:
                self.logger.info("No suggestions found via locator, trying Arrow Down and Enter")
                search = self.driver.find_element(*self.search_box)
                search.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                search.send_keys(Keys.ENTER)
        except Exception as e:
            self.logger.error(f"Error during location selection: {str(e)}")

    def click_search(self):
        self.logger.info("Clicking Search button")
        # Try to close any overlay first
        try:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
        except:
            pass

        try:
            # Use JS click as it is more reliable for buttons that might be obscured
            btn = self.wait.until(EC.presence_of_element_located(self.search_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn)
            self.logger.info("Search button clicked via JS")
        except Exception as e:
            self.logger.error(f"Search button not found or clickable: {e}")
            # Final attempt: click by coordinates if we can, or just try Enter on the search box
            try:
                self.driver.find_element(*self.search_box).send_keys(Keys.ENTER)
                self.logger.info("Pressed Enter on search box as fallback")
            except:
                raise e
