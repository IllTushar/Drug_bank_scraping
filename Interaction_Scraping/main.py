import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    WebDriverException

from selenium.common import StaleElementReferenceException

from assets.assets import Assets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Model.data_model import ModelClass
from typing import List
import time
import re
import math

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


def extract_last_number_from_text(text):
    # Regular expression to find all numbers, including those with commas
    numbers = re.findall(r'\d{1,3}(?:,\d{3})*|\d+', text)
    # Remove commas and convert to integers
    numbers = [int(number.replace(',', '')) for number in numbers]
    # Return the last number
    return numbers[-1] if numbers else None


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

    read_csv_file_for_drug_name = pd.read_csv(r"C:\Users\gtush\Desktop\NotScrap\not_scrap_data.csv")

    for index, base_drug in read_csv_file_for_drug_name.iterrows():
        drug_data_list: List[ModelClass] = []
        base_drug_code = base_drug['Drug URL']
        splits_code = base_drug_code.split("/")[-1]
        print(f"drug name: {base_drug['Name']}, index is: {index}")
        time.sleep(5)
        value, status = search_drug(assets, xpath, drug_data_list, base_drug, index, read_csv_file_for_drug_name)
        if value is not None:
            df = pd.DataFrame()  # for clear the dataframe
            df = pd.DataFrame(value)  # for create a new dataframe
            df.to_csv(fr"C:\Users\gtush\Desktop\Collection_2\{splits_code}.csv", index=False)
            print(fr"C:\Users\gtush\Desktop\Collection_2\{splits_code}.csv")
            # Explicitly clearing the DataFrame
            if status == 'INT':  ## INT -> Interaction in
                # Update the status in the DataFrame
                read_csv_file_for_drug_name.at[index, 'Extract'] = status
                read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\NotScrap\not_scrap_data.csv", index=False)
            else:
                status = 'T'
                # Update the status in the DataFrame
                read_csv_file_for_drug_name.at[index, 'Extract'] = status
                read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\NotScrap\not_scrap_data.csv", index=False)


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


def search_drug(assets, xpath, drug_data_list, base_drug, index, read_csv_file_for_drug_name):
    status = None
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
        print("Total Entries:", total_entries)

        rows_per_page = total_entries / 100
        pages = math.ceil(rows_per_page)
        print(f"No of pages {pages}")

        for l in range(1, pages + 1):
            time.sleep(3)
            drug_data = drug_and_interactions(assets)
            if drug_data is not None:
                drug_data_list.append(drug_data)

            select_x_path_next_page = "//*[@id = 'drug-interactions-table_next']"

            # Retry mechanism for the next page button
            retry_count = 3  # Number of retry attempts
            for attempt in range(retry_count):
                try:
                    # Scroll the next page button into view
                    next_page_button = assets.single_element_find(xpath, select_x_path_next_page)
                    next_page_button.click()
                    original_scroll_position = assets.driver.execute_script("return window.pageYOffset;")
                    assets.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                    # Adding a short delay to ensure the element is in view
                    time.sleep(1)  # Short delay to allow the action to take effect
                    assets.driver.execute_script(f"window.scrollTo(0, {original_scroll_position});")
                    status = 'T'
                    break  # If successful, exit the retry loop
                except StaleElementReferenceException:
                    print(f"Stale element reference exception occurred on attempt {attempt + 1}. Retrying...")
                    time.sleep(1)  # Adding a short delay before retrying
                    status = 'INT'
                except Exception as e:
                    print(f"An error occurred on attempt {attempt + 1}: {e}")
                    status = 'INT'
                    time.sleep(1)  # Adding a short delay before retrying

        print(len(drug_data_list))
        drug_data_rows = []
        for data in drug_data_list:
            for drug, interaction, url in zip(data.drug_name_list, data.drug_interaction_list, data.drug_url_list):
                drug_data_rows.append(
                    {"Drug": drug, "Interaction": interaction, "URL": url, "Base Drug": name_of_base_drug,
                     "Base_Drug URL": base_drug_url})

        return drug_data_rows, status

    except TimeoutException:
        status = 'TL'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\DrugBankData\DrugBankData.csv", index=False)
        print("Timeout occurred while waiting for the element to be clickable.")
        return None
    except NoSuchElementException:
        status = 'N'
        read_csv_file_for_drug_name.at[index, 'Extract'] = status
        read_csv_file_for_drug_name.to_csv(r"C:\Users\gtush\Desktop\NotScrap\not_scrap_data.csv", index=False)
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


if __name__ == '__main__':
    # web_scraping()
    selenuim_assets = Assets()
    selenuim_assets.url()
    automation(selenuim_assets, "dmg@saya.net.in", "Saya12!")
    # web_scraping()
