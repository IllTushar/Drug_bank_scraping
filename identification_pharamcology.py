import pandas as pd

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    WebDriverException

from selenium.common import StaleElementReferenceException

from assets.assets import Assets
from selenium.webdriver.common.by import By

from typing import List
import time

from Model.identification_pharamcology_model import Model

scrap_data_list: List[Model] = []
drug_data_rows = []
csv_value_list = []


def automation(assets, email, password):
    xpath = By.XPATH
    email_xpath = "//*[starts-with(@placeholder ,'name@example')]"
    assets.explict_wait(5, xpath, email_xpath)

    # Email
    user_email = assets.single_element_find(xpath, email_xpath)
    user_email.send_keys(email)

    # Password
    password_x_path = "//*[@type = 'password']"
    user_password = assets.single_element_find(xpath, password_x_path)
    user_password.send_keys(password)

    # Login
    login_x_path = '//*[@data-disable-with ="Log in"]'
    login = assets.single_element_find(xpath, login_x_path)
    login.click()

    read_csv_file_for_drug_name = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv")
    drug_list = read_csv_file_for_drug_name['Name']

    count = 0
    for drug in drug_list:
        count += 1
        print(f"drug name: {drug}, index is: {count}")
        time.sleep(5)
        value = search_drug(assets, xpath, scrap_data_list, drug)
        csv_value_list.append(value)

    # Check if csv_value is defined and not empty before using it
    for csv_value in csv_value_list:
        if csv_value is not None and not csv_value.empty:
            csv_value.to_csv(fr"C:\Users\gtush\Desktop\SayaCsv\FormalData.csv", index=False)
        else:
            print("Data not found")

    # Extract cookies from the browser
    cookies = assets.browser.get_cookies()
    print("Cookies:", cookies)


def search_drug(assets, xpath, drug_data_list, drug):
    # Search Bar
    search_bar_x_path = '//*[starts-with(@placeholder,"Type your search")]'
    search = assets.single_element_find(xpath, search_bar_x_path)
    search.clear()
    search.send_keys(drug)

    # Search Icon
    search_button_x_path = '//*[starts-with(@class,"search-query-button")]'
    search_button = assets.single_element_find(xpath, search_button_x_path)
    search_button.click()
    try:
        # Title
        title_x_path = '//*[@class ="align-self-center mr-4"]'
        assets.explict_wait(5, xpath, title_x_path)
        title = assets.single_element_find(xpath, title_x_path)
        drug_title = title.text

        # Generic Name
        generic_x_path = '//dt[@id="generic-name"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, generic_x_path)
        generic = assets.single_element_find(xpath, generic_x_path).text

        # Type
        type_x_path = '//*[@id="type"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, type_x_path)
        type_drug = assets.single_element_find(xpath, type_x_path).text

        # Background
        background_x_path = '//*[@id="background"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, background_x_path)
        background = assets.single_element_find(xpath, background_x_path).text

        # print(background.text)

        # Get URL End point
        end_point_x_path = "//dd[contains(@class, 'col-xl-4 col-md-9 col-sm-8') and starts-with(text(), 'DB')]"
        assets.explict_wait(5, xpath, background_x_path)
        end_point = assets.single_element_find(xpath, end_point_x_path)
        base_url = end_point.text

        # Pharmacology

        # Indication
        indication_x_path = '//*[@id = "indication"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, indication_x_path)
        indication = assets.single_element_find(xpath, indication_x_path).text

        # Pharmacodynamics
        pharmacodynamics_x_path = '//*[@id = "pharmacodynamics"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, pharmacodynamics_x_path)
        pharmacodynamics = assets.single_element_find(xpath, pharmacodynamics_x_path).text

        # Mechanism action
        mechanism_x_path = '//*[@id = "mechanism-of-action"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, mechanism_x_path)
        mechanism = assets.single_element_find(xpath, mechanism_x_path).text

        # Absorption
        absorption_x_path = '//*[@id = "absorption"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, absorption_x_path)
        absorption = assets.single_element_find(xpath, absorption_x_path).text

        # Half-life
        half_life_x_path = '//*[@id = "half-life"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, half_life_x_path)
        half_life = assets.single_element_find(xpath, half_life_x_path).text

        # Toxicity
        toxicity_x_path = '//*[@id = "toxicity"]/following-sibling::dd[1]'
        assets.explict_wait(5, xpath, toxicity_x_path)
        toxicity = assets.single_element_find(xpath, toxicity_x_path).text

        # Create Model Class Object
        model_class = Model(drug_title, generic, type_drug, background, f"https://go.drugbank.com/drugs/{base_url}",
                            indication,
                            pharmacodynamics, mechanism, absorption, half_life, toxicity)
        scrap_data_list.append(model_class)

        for data in drug_data_list:
            drug_data_rows.append(
                {"Title": data.drug_title, "Generic Name": data.generic, "Type": data.type_drug,
                 "Background": data.background,
                 "url": data.base_url, "Indication": data.indication, "Pharmacodynamics": data.pharamacodynamics,
                 "Mechanism": data.mechanism,
                 "Absorption": data.absorption, "Half-life": data.half_life, "Toxicity": data.toxicity})

        csv_data = pd.DataFrame(drug_data_rows)

        return csv_data

    except TimeoutException:
        print("Timeout occurred while waiting for the element to be clickable.")
        return None

    # Handle the timeout exception (e.g., retrying the operation, logging the error)
    except NoSuchElementException:
        print("Element not found.")
        return None
    except ElementClickInterceptedException:
        print("No Click able element")
        return None
    except StaleElementReferenceException:
        print("StateElementReference")
        return None
    except WebDriverException:
        print("Web driver not found")
        return None


if __name__ == '__main__':
    assets = Assets()
    assets.url()
    automation(assets, "dmg@saya.net.in", "Saya12!")
