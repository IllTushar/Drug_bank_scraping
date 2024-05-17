import pandas as pd
from bs4 import BeautifulSoup
import requests as rq


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

    data_frame = pd.DataFrame({"Name": drug_name_list, "Description": drug_description_list, "Drug Weight": drug_weight,
                               "Drug Category": drug_category, "Drug URL": drug_url})
    data_frame.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv", index=False)


def drug_and_interactions():
    drug_name_list = []
    drug_interaction_list = []
    drug_url_list = []

    # Request the page content
    url = "https://go.drugbank.com/drugs/DB01048"
    data_rq = rq.get(url)
    soup = BeautifulSoup(data_rq.text, "html.parser")
    title = soup.title.text
    splits_title = title.split(":")

    tables = soup.find(id="drug-interactions-table")
    # Ensure there are enough tables found
    if tables:
        tr_tags = tables.find_all("tr")
        print(len(tr_tags))
        # Loop through each <tr> tag
        for tr_tag in tr_tags:
            # Extract all <td> tags within the current <tr> tag
            td_tags = tr_tag.find_all("td")

            # Extract text from the first <td> tag (which contains drug names)
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

        data_frame = pd.DataFrame({"Drug": drug_name_list, "Interaction": drug_interaction_list, "URL": drug_url_list})
        data_frame.to_csv(fr"C:\Users\gtush\Desktop\SayaCsv\{splits_title[0]}InteractionData.csv")
    else:
        print("Table with id 'drug-interactions-table' not found.")


if __name__ == '__main__':
    # web_scraping()
    drug_and_interactions()
