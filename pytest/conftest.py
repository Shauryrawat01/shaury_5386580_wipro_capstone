import os
from datetime import datetime

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from utilities.config_reader import (
    get_base_url,
    get_browser,
    get_implicit_wait
)


@pytest.fixture(scope="module")
def driver():

    browser = get_browser()

    if browser == "chrome":

        chrome_options = Options()

        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        chrome_options.add_experimental_option(
            "useAutomationExtension",
            False
        )
        driver = webdriver.Chrome(
            service=Service(),options=chrome_options
        )

        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )


    elif browser == "edge":

        driver = webdriver.Edge()

    else:
        raise Exception("Browser not supported")

    driver.maximize_window()

    driver.implicitly_wait(get_implicit_wait())

    driver.get(get_base_url())

    yield driver

    driver.quit()


# Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            screenshots_dir = "screenshots"

            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            file_name = f"{item.name}_{timestamp}.png"

            file_path = os.path.join(
                screenshots_dir,
                file_name
            )

            try:
                driver.save_screenshot(file_path)
                print(f"Screenshot saved: {file_path}")
                
                # Attach to Allure Report
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to save screenshot or attach to allure: {e}")
