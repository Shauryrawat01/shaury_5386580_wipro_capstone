from behave import given, when, then
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.logger import setup_logger
import time

logger = setup_logger("SearchSteps")

@when('I click on the Projects tab')
def step_impl(context):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(context.driver)
    context.home_page.click_projects_tab()
    logger.info("Clicked Projects tab")

@when('I enter the location from test data')
def step_impl(context):
    location = context.test_data['location']
    context.home_page.enter_location(location)
    logger.info(f"Entered location: {location}")

@when('I select the location from suggestions')
def step_impl(context):
    context.home_page.select_location()
    logger.info("Selected location from suggestions")

@when('I click the Search button')
def step_impl(context):
    context.home_page.click_search()
    logger.info("Clicked Search button")

@then('the search results page should be displayed')
def step_impl(context):
    context.results_page = SearchResultsPage(context.driver)
    assert context.results_page.verify_search_results(), "Search results page not displayed"
    logger.info("Search results page displayed")

@given('I have searched for a location')
def step_impl(context):
    context.execute_steps(u"""
        Given I am on the 99acres home page
        When I click on the Projects tab
        And I enter the location from test data
        And I select the location from suggestions
        And I click the Search button
        Then the search results page should be displayed
    """)

@when('I apply the {bhk} filter')
def step_impl(context, bhk):
    if not hasattr(context, 'results_page'):
        context.results_page = SearchResultsPage(context.driver)
    if bhk == "3 BHK":
        context.results_page.apply_3bhk_filter()
    elif bhk == "2036": # This is a bit hacky based on existing code
        context.results_page.apply_2036_filter()
    time.sleep(3)
    logger.info(f"Applied {bhk} filter")

@then('the required property card should be visible')
def step_impl(context):
    assert context.results_page.verify_property_card_visible(), "Property card not visible"
    logger.info("Property card visible")

@when('I enter an invalid location "{location}"')
def step_impl(context, location):
    context.home_page.enter_location(location)
    logger.info(f"Entered invalid location: {location}")

@when('I enter an empty location')
def step_impl(context):
    context.home_page.enter_location("")
    logger.info("Entered empty location")

@then('I should see a message indicating no results were found')
def step_impl(context):
    if not hasattr(context, 'results_page'):
        context.results_page = SearchResultsPage(context.driver)
    context.results_page.verify_no_results()
    logger.info("Verified no results found")
