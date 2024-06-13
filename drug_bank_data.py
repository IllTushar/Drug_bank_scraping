import math
import requests as rq
from assets.assets import Assets
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd


def automation(assets, email, password):
    xpath = By.XPATH
    email_xpath = "//*[starts-with(@placeholder ,'name@example')]"
    assets.explict_wait(10, xpath, email_xpath)

    # Email
    user_email = assets.single_element_find(xpath, email_xpath)
    user_email.clear()  # Clear the field before sending keys
    user_email.send_keys(email)

    # Password
    password_x_path = "//*[@type = 'password']"
    assets.explict_wait(10, xpath, password_x_path)
    user_password = assets.single_element_find(xpath, password_x_path)
    user_password.clear()  # Clear the field before sending keys
    user_password.send_keys(password)

    # Login
    login_x_path = '//*[@data-disable-with ="Log in"]'
    assets.explict_wait(10, xpath, login_x_path)
    login = assets.single_element_find(xpath, login_x_path)
    login.click()

    explore_x_path = '//*[text()="Explore"]'
    assets.explict_wait(10, xpath, explore_x_path)
    assets.mouse_hover(xpath, explore_x_path)

    filter_element_array = ['Investigational', 'Nutraceutical', 'Illicit', 'Withdrawn', 'Experimental']
    all_dataframes = []
    temp = None
    # Apply Filter
    for row in range(len(filter_element_array)):

        # Approved
        if row == 0:
            time.sleep(5)
            apply_filter_x_path = f'//*[text() = "Approved"]'
            apply_filter = assets.single_element_find(xpath, apply_filter_x_path)
            apply_filter.click()

        approved_x_path = f"//*[text()='{filter_element_array[row]}']"
        if temp is not None:
            assets.mouse_hover(xpath, temp)

        temp = approved_x_path
        assets.mouse_hover(xpath, approved_x_path)

        # Apply filter
        time.sleep(2)
        apply_filter_x_path = '//*[@data-disable-with = "Apply Filter"]'
        apply_filter = assets.single_element_find(xpath, apply_filter_x_path)
        apply_filter.click()

        # Extract page info and print the last <b> element text
        page_info_xpath = "//div[@class='page_info']/b[last()]"
        time.sleep(2)
        assets.explict_wait(10, xpath, page_info_xpath)
        last_b_element = assets.single_element_find(xpath, page_info_xpath)
        last_b_text = last_b_element.text.replace(',', '')  # Remove any commas if present
        range_of_the_element = math.ceil(int(last_b_text) / 25)
        print(f"Total number of pages: {range_of_the_element}")

        for l in range(1, range_of_the_element + 1):
            time.sleep(5)
            dataframe = web_scraping(l, filter_element_array[row])
            all_dataframes.append(dataframe)
            next_x_path = '//*[@class = "page-item next"]'
            next_button = assets.single_element_find(xpath, next_x_path)
            next_button.click()
            break

    final_dataframe = pd.concat(all_dataframes, ignore_index=True)
    return final_dataframe


def web_scraping(page_number, filter_name):
    drug_name_list = []
    drug_description_list = []
    drug_url = []
    drug_weight = []
    drug_category = []
    group_status = []
    data = None
    if filter_name == 'Investigational':
        data = rq.get(
            f"https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental={0}&illicit={0}&investigational={1}&nutraceutical={0}&page={page_number}&us=0&withdrawn={0}")
    elif filter_name == 'Nutraceutical':
        data = rq.get(
            f"https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental={0}&illicit={0}&investigational={0}&nutraceutical={1}&page={page_number}&us=0&withdrawn={0}")

    elif filter_name == 'Illicit':
        data = rq.get(
            f"https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental={0}&illicit={1}&investigational={0}&nutraceutical={0}&page={page_number}&us=0&withdrawn={0}")

    elif filter_name == 'Withdrawn':
        data = rq.get(
            f"https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental={0}&illicit={0}&investigational={0}&nutraceutical={0}&page={page_number}&us=0&withdrawn={1}")

    elif filter_name == 'Experimental':
        data = rq.get(
            f"https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental={1}&illicit={0}&investigational={0}&nutraceutical={0}&page={page_number}&us=0&withdrawn={0}")

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
            group_status.append(filter_name)

            if name_data and description_data and drug_weight_data and drug_category_data and url_data:
                drug_name_list.append(name_data.text.strip())
                drug_description_list.append(description_data.text.strip())
                drug_weight.append(drug_weight_data.text.strip())
                drug_category.append(drug_category_data.text.strip())
                drug_url.append(f"https://go.drugbank.com{url_data['href']}")

    # Ensure all lists are of the same length
    if not (len(drug_name_list) == len(drug_description_list) == len(drug_weight) == len(drug_category) == len(
            drug_url)):
        raise ValueError("All arrays must be of the same length")

    data_frame = pd.DataFrame(
        {"Name": drug_name_list, "Description": drug_description_list, "Drug Weight": drug_weight,
         "Drug Category": drug_category, "Drug URL": drug_url, "Group Status": group_status,
         "Drug Group": "Small Molecule"})
    return data_frame


if __name__ == '__main__':
    assets = Assets()
    assets.url()
    df = automation(assets, "dmg@saya.net.in", "Saya12!")
    df.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\Drug_bank2.csv', index=False)
