from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service


class Assets:
    def __init__(self):
        option = Options()
        option.add_experimental_option("detach", True)
        self.browser = wd.Chrome(options=option)
        self.action = wd.ActionChains(self.browser, duration=2000)

    def url(self):
        self.browser.get("https://go.drugbank.com/public_users/log_in")

    def explict_wait(self, time_out, xpath, attribute_x_path):
        WebDriverWait(self.browser, time_out).until(EC.visibility_of_element_located((xpath, attribute_x_path)))

    def single_element_find(self, xpath, attribute_x_path):
        element = self.browser.find_element(xpath, attribute_x_path)
        return element

    def multiple_element_find(self, xpath, attribute_x_path):
        multiple_elements = self.browser.find_elements(xpath, attribute_x_path)
        return multiple_elements

    def action_chain(self, xpath, attribute_x_path):
        self.action.move_to_element(
            self.browser.find_element(xpath, attribute_x_path)).click().perform()

    def wait_until_element_not_click_able(self, xpath, attribute_x_path):
        try:
            medicine_add = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((xpath, attribute_x_path))
            )
            return medicine_add
        except Exception as e:
            print(f"Error while clicking on add medicine button: {e}")

    def mouse_hover(self, xpath, attribute_x_path):
        action = wd.ActionChains(self.browser, duration=2000)
        action.move_to_element(
            self.browser.find_element(xpath, attribute_x_path)).click().perform()
