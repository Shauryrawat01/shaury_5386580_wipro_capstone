from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utilities.logger import setup_logger


class SearchResultsPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 20)
        self.logger = setup_logger(self.__class__.__name__)

    # Robust locators for property cards
    property_results = (
        By.XPATH,
        "//*[contains(@class,'tuple') or contains(@class,'Card')]"
    )

    bhk_3_filter = (
        By.XPATH,
        "//span[@title='3 BHK']"
    )

    bhk_2_filter = (
        By.XPATH,
        "//span[@title='2 BHK']"
    )

    bhk_2036_filter = (
        By.XPATH,
        "//span[@title='2036']"
    )

    third_property = (
        By.XPATH,
        "//td[@colspan='3']"
    )

    # Very flexible locator to find any element containing 'View Number'
    view_number_button = (
        By.XPATH,
        "//*[contains(text(),'View Number')]"
    )

    no_identity_option = (
        By.XPATH,
        "//label[@for='identityRadioI']"
    )

    name_input = (By.NAME, "name")
    phone_input = (By.NAME, "phone")

    ok_got_it_button = (
        By.XPATH,
        "//*[contains(text(),'OK, Got it') or contains(text(),'Got it')]"
    )
    
    # Updated locator based on screenshot text
    lead_form_popup = (
        By.XPATH,
        "//*[contains(text(),'Please share your details') or contains(@class, 'leadForm')]"
    )
    
    no_results_msg = (
        By.XPATH,
        "//*[contains(text(),'0 results') or contains(text(),'No results') or contains(text(),'Zero Results')]"
    )

    def verify_search_results(self):
        self.logger.info("Verifying search results visibility")
        try:
            # Short wait for any listing to appear
            self.wait.until(
                EC.presence_of_element_located(self.property_results)
            )
            self.logger.info("Search results are visible")
            return True
        except Exception as e:
            self.logger.error(f"Search results not visible: {str(e)}")
            return False

    def verify_no_results(self):
        self.logger.info("Verifying that no search results are found")
        try:
            # 99acres shows '0 results' text or similar when nothing is found.
            # If property cards are shown, it's a fail for negative test.
            
            # Check if property cards appear within 5 seconds
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.property_results)
                )
                self.logger.warning("Property cards WERE found. Search did not return zero results.")
                
                # Double check if it's the 'Featured' or 'Similar' results which 99acres sometimes shows
                # But for a basic negative test, any cards mean the search "found" something (even if fallback)
                return False
            except:
                self.logger.info("No property cards found. This matches expected negative behavior.")
                return True

        except Exception as e:
            self.logger.error(f"Error in verify_no_results: {str(e)}")
            return True # Assume no results if error occurred during card search
            
    def verify_property_card_visible(self):
        return self.verify_search_results()

    def apply_3bhk_filter(self):
        self.logger.info("Applying 3 BHK filter")
        filter_element = self.wait.until(
            EC.element_to_be_clickable(
                self.bhk_3_filter
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", filter_element)
        self.driver.execute_script("arguments[0].click();", filter_element)
        time.sleep(2) # Wait for results to refresh

    def apply_2036_filter(self):
        self.logger.info("Applying 2036 filter")
        filter_element = self.wait.until(
            EC.element_to_be_clickable(
                self.bhk_2036_filter
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", filter_element)
        self.driver.execute_script("arguments[0].click();", filter_element)
        time.sleep(2) # Wait for results to refresh

    def click_third_property(self):
        self.logger.info("Clicking on the third property result")
        # Give page some time to stabilize after filters
        time.sleep(3)
        
        try:
            # Try user-suggested locator for td[@colspan='3']
            element = self.wait.until(
                EC.element_to_be_clickable(self.third_property)
            )
        except:
            # Fallback to the third card div
            self.logger.info("Falling back to generic locator for third property")
            element = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//*[contains(@class,'tuple') or contains(@class,'Card')])[3]")
                )
            )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)

    def switch_to_new_tab(self):
        self.logger.info("Switching to the newly opened tab")
        # Wait for new window handle to appear
        self.wait.until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def click_view_number(self):
        self.logger.info("Clicking on 'View Number' button")
        # Try multiple strategies to find the button
        try:
            element = self.wait.until(
                EC.presence_of_element_located(self.view_number_button)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self.logger.warning(f"Standard click failed, attempting JS click: {str(e)}")
            # Absolute fallback using JavaScript to find element by text
            self.driver.execute_script("""
                var elements = document.querySelectorAll('*');
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].innerText === 'View Number' || elements[i].textContent === 'View Number') {
                        elements[i].click();
                        break;
                    }
                }
            """)

    def verify_contact_popup(self):
        self.logger.info("Verifying if contact details popup is visible")
        try:
            # Use presence instead of visibility in case it's partially obscured
            self.wait.until(
                EC.presence_of_element_located(self.lead_form_popup)
            )
            self.logger.info("Contact details popup is visible")
            return True
        except Exception as e:
            self.logger.error(f"Contact details popup not visible: {str(e)}")
            return False

    def click_no_on_identity(self):
        self.logger.info("Clicking 'No' on identity option")
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(
                    self.no_identity_option
                )
            )
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self.logger.warning(f"Could not click 'No' on identity: {str(e)}")

    def enter_lead_name(self, name):
        self.logger.info(f"Entering lead name: {name}")
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    self.name_input
                )
            )
            element.clear()
            element.send_keys(name)
        except Exception as e:
            self.logger.error(f"Could not enter lead name: {str(e)}")

    def enter_lead_phone(self, phone):
        self.logger.info(f"Entering lead phone: {phone}")
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    self.phone_input
                )
            )
            element.clear()
            element.send_keys(phone)
        except Exception as e:
            self.logger.error(f"Could not enter lead phone: {str(e)}")

    def click_ok_got_it(self):
        self.logger.info("Clicking 'OK, Got it' button")
        # Increased wait for pop-up on new tab
        time.sleep(5) 
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(
                    self.ok_got_it_button
                )
            )
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("Successfully clicked 'OK, Got it'")
        except Exception as e:
            # If pop-up doesn't appear, just log and continue
            self.logger.info(f"OK, Got it pop-up not found or already closed: {str(e)}")
