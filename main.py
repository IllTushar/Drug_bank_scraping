import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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


def extract_last_number_from_text(text):
    # Regular expression to find all numbers in the text
    numbers = re.findall(r'\d+', text)
    # Convert the found numbers to integers and return the last number
    return int(numbers[-1]) if numbers else None


def automation(assets, email, password):
    global csv_value
    csv_value_list = []
    drug_data_list: List[ModelClass] = []
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

    drug_list = ["Abacavir hydroxyacetate", "Abacavir"]

    for drug in drug_list:
        time.sleep(5)
        value = search_drug(assets, xpath, drug_data_list, drug)
        csv_value_list.append(value)
    # Check if csv_value is defined and not empty before using it
    for csv_value in csv_value_list:
        if csv_value is not None and not csv_value.empty:
            csv_value.to_csv(fr"C:\Users\gtush\Desktop\SayaCsv\InteractionData.csv", index=False)
        else:
            print("Data not found")

    # Extract cookies from the browser
    cookies = assets.browser.get_cookies()
    print("Cookies:", cookies)


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

    # Interaction
    click_x_path = '//*[@id = "interactions-sidebar-header"]'
    click_button = assets.single_element_find(xpath, click_x_path)
    click_button.click()

    # Row Spinner
    spinner_x_path = '//*[starts-with(@aria-controls,"drug-interactions-table")]'
    # assets.explict_wait(5, xpath, spinner_x_path)
    try:
        assets.mouse_hover(xpath, spinner_x_path)
        # Wait for the dropdown to be visible and interactable
        select_x_path = '//*[@id="drug-interactions-table_length"]/label/select'
        assets.explict_wait(5, xpath, select_x_path)
        select_element = assets.single_element_find(xpath, select_x_path)
        # Use the Select class to interact with the dropdown
        select = Select(select_element)
        select.select_by_index(4)  # Selecting the fifth option (index starts from 0)

        # Entity
        entity_x_path = '//*[@id = "drug-interactions-table_info"]'
        time.sleep(5)
        element = assets.single_element_find(xpath, entity_x_path)
        total_entries = extract_last_number_from_text(element.text)
        print("Total Entries:", total_entries)

        rows_per_page = total_entries / 100
        pages = math.ceil(rows_per_page)

        for l in range(1, pages + 1):
            time.sleep(5)
            drug_data = drug_and_interactions(assets)
            if drug_data is not None:
                drug_data_list.append(drug_data)

            select_x_path_next_page = "//*[@id = 'drug-interactions-table_next']"

            # Wait for the next page button to be clickable
            try:
                assets.explict_wait(5, xpath, select_x_path_next_page)
                next_page_button = assets.single_element_find(xpath, select_x_path_next_page)
                next_page_button.click()
            except StaleElementReferenceException:
                print("Stale element reference exception occurred. Retrying...")
                assets.explict_wait(5, xpath, select_x_path_next_page)
                next_page_button = assets.single_element_find(xpath, select_x_path_next_page)
                next_page_button.click()

        print(len(drug_data_list))
        drug_data_rows = []
        for data in drug_data_list:
            for drug, interaction, url in zip(data.drug_name_list, data.drug_interaction_list, data.drug_url_list):
                drug_data_rows.append({"Drug": drug, "Interaction": interaction, "URL": url,
                                       "Base Drug": "https://go.drugbank.com/drugs/DB01048"})

        csv_data = pd.DataFrame(drug_data_rows)
        return csv_data

    except TimeoutException:
        print("Timeout occurred while waiting for the element to be clickable.")
        return None
        # Handle the timeout exception (e.g., retrying the operation, logging the error)
    except NoSuchElementException:
        print("Element not found.")
        return None


def web_scraping():
    drug_name_list = []
    drug_description_list = []
    drug_url = []
    drug_weight = []
    drug_category = []
    count = 0

    # Iterate over the range of pages you want to scrape
    for index in range(1, 113):  # Assuming you want to scrape pages 1 to 112
        data = rq.get(f"https://go.drugbank.com/drugs?approved=1&c=name&d=up&page={index}")
        response = data.text
        soup = BeautifulSoup(response, "html.parser")

        # Find the table containing drug data
        table = soup.find("div", class_="index-content")
        if table:
            rows = table.find_all("tr")[1:]  # Skip the header row
            for row in rows:
                name_data = row.find("td", class_="name-value text-sm-center drug-name")
                description_data = row.find("td", class_="description-value")
                drug_weight_data = row.find("td", class_="weight-value")
                drug_category_data = row.find_next("td", class_="categories-value")
                url_data = row.find("a", href=True)

                if name_data and description_data and drug_weight_data and drug_category_data and url_data:
                    drug_name_list.append(name_data.text.strip())
                    drug_description_list.append(description_data.text.strip())
                    drug_weight.append(drug_weight_data.text.strip())
                    drug_category.append(drug_category_data.text.strip())
                    drug_url.append(f"https://go.drugbank.com{url_data['href']}")

        count += 1
        print(f"page-> {count}")
    # Ensure all lists are of the same length
    if not (len(drug_name_list) == len(drug_description_list) == len(drug_weight) == len(
            drug_category) == len(drug_url)):
        raise ValueError("All arrays must be of the same length")

    data_frame = pd.DataFrame(
        {"Name": drug_name_list, "Description": drug_description_list, "Drug Weight": drug_weight,
         "Drug Category": drug_category, "Drug URL": drug_url})
    data_frame.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv", index=False)


if __name__ == '__main__':
    # web_scraping()
    selenuim_assets = Assets()
    selenuim_assets.url()
    automation(selenuim_assets, "gtushar697@gmail.com", "Tushar@12345")
