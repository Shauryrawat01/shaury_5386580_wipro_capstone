from behave import when, then
from pages.search_results_page import SearchResultsPage
from utilities.logger import setup_logger
import os
import time
import allure

logger = setup_logger("PropertyDetailsSteps")

@when('I click on the third property result')
def step_impl(context):
    if not hasattr(context, 'results_page'):
        context.results_page = SearchResultsPage(context.driver)
    context.results_page.click_third_property()
    logger.info("Clicked on the third property result")

@when('I switch to the new tab')
def step_impl(context):
    context.results_page.switch_to_new_tab()
    logger.info("Switched to the new tab")

@when('I click \'OK GOT IT\' if present')
def step_impl(context):
    context.results_page.click_ok_got_it()
    logger.info("Clicked 'OK GOT IT' button")

@when('I click the \'View Number\' button')
def step_impl(context):
    context.results_page.click_view_number()
    logger.info("Clicked 'View Number' button")

@then('the contact details popup should be displayed')
def step_impl(context):
    assert context.results_page.verify_contact_popup(), "Contact details popup not displayed"
    logger.info("Contact details popup displayed")

@then('I take a screenshot of the view number result')
def step_impl(context):
    screenshot_dir = "screenshots/result_screenshots/view_number"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"view_number_result_{timestamp}.png")
    
    context.driver.save_screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name="Contact Details Popup", attachment_type=allure.attachment_type.PNG)
    logger.info(f"Screenshot saved at: {screenshot_path}")
    assert os.path.exists(screenshot_path), "Failed to save screenshot"
