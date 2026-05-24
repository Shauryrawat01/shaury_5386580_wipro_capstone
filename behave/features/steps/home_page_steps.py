from behave import given, then
from pages.home_page import HomePage
from utilities.logger import setup_logger

logger = setup_logger("HomePageSteps")

@given('I am on the 99acres home page')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    context.driver.get(context.base_url)
    logger.info("Navigated to 99acres home page")

@then('the page title should be visible')
def step_impl(context):
    assert context.driver.title is not None
    logger.info(f"Page title is: {context.driver.title}")

@then('the Projects tab should be displayed')
def step_impl(context):
    assert context.home_page.wait.until(
        lambda d: d.find_element(*context.home_page.projects_tab).is_displayed()
    ), "Projects tab is not displayed"

@then('the Search box should be displayed')
def step_impl(context):
    assert context.home_page.wait.until(
        lambda d: d.find_element(*context.home_page.search_box).is_displayed()
    ), "Search box is not displayed"

@then('the Search button should be displayed')
def step_impl(context):
    assert context.home_page.wait.until(
        lambda d: d.find_element(*context.home_page.search_button).is_displayed()
    ), "Search button is not displayed"
