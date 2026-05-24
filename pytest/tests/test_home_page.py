from pages.home_page import HomePage
from utilities.logger import setup_logger

logger = setup_logger("TestHomePage")

def test_homepage_elements(driver):
    logger.info("Starting homepage validation test")
    home = HomePage(driver)

    logger.info("Verifying page title")
    assert driver.title is not None
    logger.info(f"Page title is: {driver.title}")

    logger.info("Verifying Projects tab is displayed")
    assert home.wait.until(
        lambda d: d.find_element(*home.projects_tab).is_displayed()
    ), "Projects tab is not displayed"

    logger.info("Verifying Search box is displayed")
    assert home.wait.until(
        lambda d: d.find_element(*home.search_box).is_displayed()
    ), "Search box is not displayed"

    logger.info("Verifying Search button is displayed")
    assert home.wait.until(
        lambda d: d.find_element(*home.search_button).is_displayed()
    ), "Search button is not displayed"

    logger.info("Homepage elements validated successfully")
