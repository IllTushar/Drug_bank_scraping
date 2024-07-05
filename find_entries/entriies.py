import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    WebDriverException
from selenium.common import StaleElementReferenceException
from assets.assets import Assets
from selenium.webdriver.common.by import By
import time
from typing import List
from Model.data_model import ModelClass
import math
from selenium.webdriver.support.ui import Select
import re

drug_data_list2: List[ModelClass] = []
csv_value_list = []


def search_bar(assets, xpath, base_drug):
    search_bar_x_path = '//*[starts-with(@placeholder,"Type your search")]'
    search = assets.single_element_find(xpath, search_bar_x_path)
    search.clear()
    search.send_keys(base_drug)

    # Search Icon
    search_button_x_path = '//*[starts-with(@class,"search-query-button")]'
    search_button = assets.single_element_find(xpath, search_button_x_path)
    search_button.click()

    # Get URL End point
    end_point_x_path = "//dd[contains(@class, 'col-xl-4 col-md-9 col-sm-8') and starts-with(text(), 'DB')]"
    end_point = assets.single_element_find(xpath, end_point_x_path)
    BaseUrl = end_point.text
    # Interaction
    click_x_path = '//*[@id = "interactions-sidebar-header"]'
    click_button = assets.single_element_find(xpath, click_x_path)
    click_button.click()


def automation(assets, email, password):
    global csv_value

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

    read_csv_file_for_drug_name = pd.read_csv(r"C:\Users\gtush\Desktop\DrugBankScraping\DataSetPresent_N_2.csv")

    for index, base_drug in read_csv_file_for_drug_name.iterrows():
        drug_data_list: List[ModelClass] = []
        if 459 <= index <= 606:
            print(f"drug name: {base_drug['Name']}, index is: {index}")
            time.sleep(5)
            value = search_drug(assets, xpath, drug_data_list, base_drug, index, read_csv_file_for_drug_name)
            if value is not None:
                read_csv_file_for_drug_name.at[index, 'Entries'] = value
                read_csv_file_for_drug_name.to_csv(r'C:\Users\gtush\Desktop\DrugBankScraping\DataSetPresent_N_2.csv',
                                                   index=False)


def search_drug(assets, xpath, drug_data_list, base_drug, index, read_csv_file_for_drug_name):
    status = None
    file_path = r'C:\Users\gtush\Desktop\DrugBankScraping\DataSetPresent_N_2.csv'
    # Search Bar
    name_of_base_drug = base_drug['Name']
    base_drug_url = base_drug['Drug URL']
    search_bar(assets, xpath, name_of_base_drug)

    # Row Spinner
    spinner_x_path = '//*[starts-with(@aria-controls,"drug-interactions-table")]'
    try:
        assets.mouse_hover(xpath, spinner_x_path)
        # Wait for the dropdown to be visible and interactable
        select_x_path = '//*[@id="drug-interactions-table_length"]/label/select'
        assets.explict_wait(3, xpath, select_x_path)
        select_element = assets.single_element_find(xpath, select_x_path)
        # Use the Select class to interact with the dropdown
        select = Select(select_element)
        select.select_by_index(4)  # Selecting the fifth option (index starts from 0)

        # Entity
        entity_x_path = '//*[@id = "drug-interactions-table_info"]'
        time.sleep(3)
        element = assets.single_element_find(xpath, entity_x_path)
        total_entries = extract_last_number_from_text(element.text)
        print('Total entries', total_entries)
        return total_entries


    except TimeoutException:
        status = 'TL'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(file_path, index=False)
        print("Timeout occurred while waiting for the element to be clickable.")
        return None
    except NoSuchElementException:
        status = 'N'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(file_path, index=False)
        print("No element found")
        return None
    except ElementClickInterceptedException:
        status = 'EN'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\NotScrap\not_scrap_data.csv", index=False)
        print("Element click intercepted.")
        return None
    except StaleElementReferenceException:
        status = 'SE'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\DrugBankData\DrugBankData.csv", index=False)
        print("StaleElementReferenceException.")
        return None
    except WebDriverException:
        status = 'WD'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\DrugBankData\DrugBankData.csv", index=False)
        print("Web driver not found.")
        return None


def extract_last_number_from_text(text):
    # Regular expression to find all numbers, including those with commas
    numbers = re.findall(r'\d{1,3}(?:,\d{3})*|\d+', text)
    # Remove commas and convert to integers
    numbers = [int(number.replace(',', '')) for number in numbers]
    # Return the last number
    return numbers[-1] if numbers else None


def drug_and_interactions(assets):
    drug_name_list = []
    drug_interaction_list = []
    drug_url_list = []

    soup = BeautifulSoup(assets.browser.page_source, "html.parser")
    tables = soup.find(id="drug-interactions-table")

    # Ensure there are enough tables found
    if tables:
        tbody = tables.find('tbody')
        tr_tags = tbody.find_all("tr")

        # Loop through each <tr> tag
        for tr_tag in tr_tags:
            # Extract all <td> tags within the current <tr> tag
            td_tags = tr_tag.find_all("td")

            # Extract text from the <td> tags
            if td_tags:
                drug_name = td_tags[0].text.strip()
                drug_name_list.append(drug_name)
                drug_interaction = td_tags[1].text.strip()
                drug_interaction_list.append(drug_interaction)

                # Extract href attribute from each <a> tag within the <td> tags
                for td in td_tags:
                    a_tags = td.find_all("a")
                    for a_tag in a_tags:
                        row_data = a_tag.get("href")
                        url = "https://go.drugbank.com" + row_data
                        drug_url_list.append(url)
        return ModelClass(drug_name_list, drug_interaction_list, drug_url_list)
    else:
        print("Table with id 'drug-interactions-table' not found.")
        return None


if __name__ == '__main__':
    selenuim_assets = Assets()
    selenuim_assets.url()
    automation(selenuim_assets, 'dmg@saya.net.in', 'Saya12!')
