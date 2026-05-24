import os
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utilities.config_reader import (
    get_base_url,
    get_browser,
    get_implicit_wait
)

from utilities.excel_reader import get_test_data

def before_all(context):
    """
    Setup before all tests.
    """
    context.test_data = get_test_data()
    browser = get_browser()
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        context.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        context.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
    elif browser == "edge":
        context.driver = webdriver.Edge()
    else:
        raise Exception(f"Browser '{browser}' not supported")

    context.driver.maximize_window()
    context.driver.implicitly_wait(get_implicit_wait())
    context.base_url = get_base_url()

def before_scenario(context, scenario):
    """
    Actions before each scenario.
    """
    context.driver.get(context.base_url)

def after_scenario(context, scenario):
    """
    Cleanup after each scenario.
    """
    if scenario.status == "failed":
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{scenario.name.replace(' ', '_')}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)
        
        try:
            context.driver.save_screenshot(file_path)
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=f"screenshot_{scenario.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to save screenshot or attach to allure: {e}")

def after_all(context):
    """
    Teardown after all tests.
    """
    if hasattr(context, 'driver'):
        context.driver.quit()
