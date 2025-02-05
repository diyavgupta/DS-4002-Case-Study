import requests
from bs4 import BeautifulSoup
import csv

with open("deathRow.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

last_statement_links = []
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) > 2: 
        link_cell = cells[2]  
        if link_cell and link_cell.a:
            link = link_cell.a['href']
            if not link.startswith(('http://', 'https://')):
                link = f"https://www.tdcj.texas.gov{link}"
            last_statement_links.append(link)
def scrape_text_from_link(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None


output_file = "last_statements.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Link", "Text"])  
    for link in last_statement_links:
        print(f"Scraping: {link}")
        text = scrape_text_from_link(link)
        
        if text:
           
            print(f"Text from {link}:\n{text[:500]}...\n")
            writer.writerow([link, text])
        else:
            print(f"No text found for {link}\n")

print(f"Scraping complete. Data saved to {output_file}")