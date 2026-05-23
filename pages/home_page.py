from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utilities.logger import setup_logger


class HomePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 20)
        self.logger = setup_logger(self.__class__.__name__)

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
    
    first_suggestion = (
        By.XPATH,
        "//div[contains(@class,'suggester')]//li[1]"
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
        self.wait.until(
            EC.element_to_be_clickable(self.projects_tab)
        ).click()

    def enter_location(self, location):
        self.logger.info(f"Entering location: {location}")
        search = self.wait.until(
            EC.visibility_of_element_located(self.search_box)
        )

        search.clear()

        search.send_keys(location)
        time.sleep(2) # Wait for suggestions to appear

    def select_location(self):
        self.logger.info("Selecting location from suggestions")
        try:
            suggestion = self.wait.until(
                EC.element_to_be_clickable(self.first_suggestion)
            )
            suggestion.click()
        except Exception as e:
            self.logger.error(f"No suggestion found or already selected: {str(e)}")

    def click_search(self):
        self.logger.info("Clicking Search button")
        self.wait.until(
            EC.element_to_be_clickable(self.search_button)
        ).click()
