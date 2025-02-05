from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

## Script for transferring data from html format and accessing embedded info from links
## Outputs 2 files: deathrow_full.csv [contains all data] and deathRow.csv [does not contain info from links]

BASE_URL = "https://www.tdcj.texas.gov" ## base url, need for extracting from links

## access all the straightforward data
with open("deathRow.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table")

data = []
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) >= 10:
        execution_num = cells[0].get_text(strip=True)
        last_name = cells[3].get_text(strip=True)
        first_name = cells[4].get_text(strip=True)
        tdcj_number = cells[5].get_text(strip=True)
        age = cells[6].get_text(strip=True)
        date = cells[7].get_text(strip=True)
        race = cells[8].get_text(strip=True)
        county = cells[9].get_text(strip=True)
        
        link_tag = cells[1].find("a")
        profile_link = None
        if link_tag and "href" in link_tag.attrs:
            relative_link = link_tag["href"]
            if relative_link.startswith("http"):
                profile_link = relative_link  
            else:
                profile_link = f"{BASE_URL}{relative_link}"  
        data.append([execution_num, last_name, first_name, tdcj_number, age, date, race, county, profile_link])

df = pd.DataFrame(data, columns=["Execution#", "Last Name", "First Name", "TDCJ Number", "Age", "Date", "Race", "County", "Profile Link"])

df.to_csv("deathRow.csv", index=False)  ##contains all data other than the two links for statement and info
print("CSV file saved: deathRow.csv")


## function to access text data from the links that give inmate info and final words
def fetch_profile_details(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        profile_soup = BeautifulSoup(response.text, "html.parser")
        
        details = {}
        for row in profile_soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                details[key] = value
        
        return details
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

profile_details_list = []
for index, row in df.iterrows():
    if row["Profile Link"]:
        print(f"Fetching details for {row['First Name']} {row['Last Name']}...")
        details = fetch_profile_details(row["Profile Link"])
        profile_details_list.append(details)
        time.sleep(1)  
    else:
        profile_details_list.append(None)

profile_df = pd.DataFrame(profile_details_list)
final_df = pd.concat([df, profile_df], axis=1)
final_df.to_csv("deathRow_full.csv", index=False)
print("Full dataset saved: deathRow_full.csv")
