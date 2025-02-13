from bs4 import BeautifulSoup
import pandas as pd 

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
df.to_csv("deathRow.csv", index=False)  
print("CSV file saved: deathRow.csv")


