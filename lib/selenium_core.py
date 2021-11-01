import os
from logger import Logger
from selenium import webdriver
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as ec


class SeleniumCore(object):
    def __init__(self):
        self.logger = Logger.__call__().get_logger()
        try:
            # let's fetch headless value directly from the cfg file, assume it False if not found
            headless = BuiltIn().get_variable_value("${environment.headless_mode}")
        except RobotNotRunningError:
            headless = False

        try:
            current_path = os.getcwd()
            home_dir = os.path.join(current_path[:current_path.find('uiautomate')], 'uiautomate')
            if headless and headless.upper() == "YES":
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.headless = True
                self.driver = webdriver.Chrome(f'{home_dir}/chromedriver', options=chrome_options)
            else:
                self.driver = webdriver.Chrome(f'{home_dir}/chromedriver')
        except Exception as e:
            self.logger.error(f"Unable to instantiate selenium class.\nException: {e}")

    def open_url(self, url):
        self.logger.debug(f"Opening the URL: {url}")
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            self.logger.debug(f"Successfully opened the URL: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Unable to open the specified URL: {url}\nException: {e}")
        return False

    def get_title(self):
        try:
            title = self.driver.title
            self.logger.debug(f"Found web page title: {title}")
            return title
        except NoSuchElementException as e:
            self.logger.error(f"Unable to fetch current webpage title\nException: {e}")
        return False

    def close_browser(self):
        try:
            self.logger.debug(f"Closing the browser..")
            self.driver.close()
        except Exception as e:
            self.logger.error(f"Error while closing the browser\nException: {e}")

    def quit_browser(self):
        try:
            self.logger.debug(f"Quitting the browser..")
            self.driver.quit()
        except Exception as e:
            self.logger.error(f"Error while quitting the browser\nException: {e}")

    def element_displayed(self, locator, locator_type=By.XPATH, explicit_timeout=20):
        self.logger.debug(f"Checking is element is displayed, locator: {locator}")
        try:
            element = WebDriverWait(self.driver, explicit_timeout).until(
                ec.presence_of_element_located((locator_type, locator)))
            return element.is_displayed()
        except TimeoutException as e:
            self.logger.error(f"Failed to verify element load, Element locator: {locator}\nException: {e}")
        return False

    def element_load_wait(self, locator, locator_type=By.XPATH, explicit_timeout=20):
        self.logger.info(f"Waiting for element load.. locator: {locator}")
        try:
            WebDriverWait(self.driver, explicit_timeout).until(
                ec.presence_of_element_located((locator_type, locator)))
            return True
        except TimeoutException as e:
            self.logger.error(f"Failed to verify element load, Element locator: {locator}\nException: {e}")
        return False

    def click(self, locator, locator_type=By.XPATH, explicit_timeout=20):
        self.logger.debug(f"Clicking the element, locator: {locator}")
        try:
            element = WebDriverWait(self.driver, explicit_timeout).until(
                ec.element_to_be_clickable((locator_type, locator)))
            element.click()
            self.logger.debug(f"Successfully clicked on web element, locator: {locator}")
            return True
        except ElementNotInteractableException:
            element = WebDriverWait(self.driver, explicit_timeout).until(
                ec.element_to_be_clickable((locator_type, locator)))
            element.click()
            self.logger.debug(f"Successfully clicked on web element, locator: {locator}")
            return True
        except TimeoutException as e:
            self.logger.error(f"Unable to click on element, Element locator: {locator}\nException: {e}")
        return False

    def input_text(self, locator, text_value, locator_type=By.XPATH, explicit_timeout=10):
        self.logger.debug(f"Inputting the text on web element, locator: {locator}, text to enter: {text_value}")
        try:
            element = WebDriverWait(self.driver, explicit_timeout).until(
                ec.presence_of_element_located((locator_type, locator)))
            element.send_keys(text_value)
            self.logger.debug(f"Successfully entered text on web element, "
                              f"locator: {locator}, text entered: {text_value}")
            return True
        except TimeoutException as e:
            self.logger.error(f"Unable to input text for element locator: {locator}\nException: {e}")
        return False
