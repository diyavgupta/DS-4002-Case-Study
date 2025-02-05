import re
import requests
from bs4 import BeautifulSoup
import csv

# Load HTML content from a file
with open("deathRow.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all "Last Statement" links
last_statement_links = []
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) > 2:  # Ensure there are at least 3 columns
        link_cell = cells[2]  # The third column contains the "Last Statement" link
        if link_cell and link_cell.a:
            link = link_cell.a['href']
            # Ensure the link is not already a full URL
            if not link.startswith(('http://', 'https://')):
                link = f"https://www.tdcj.texas.gov{link}"
            last_statement_links.append(link)

# Function to scrape text from a link (with SSL verification disabled)
def scrape_text_from_link(url):
    try:
        # Disable SSL verification
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all text from the page
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Output file
output_file = "last_statements.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Link", "Text"])  # Write header

    # Scrape each link and save the results
    for link in last_statement_links:
        print(f"Scraping: {link}")
        text = scrape_text_from_link(link)
        
        if text:
            # Print the first 500 characters for debugging
            print(f"Text from {link}:\n{text[:500]}...\n")
            
            # Use regex to extract the inmate's name
            inmate_name_match = re.search(r"Inmate:\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)", text)
            if inmate_name_match:
                inmate_name = inmate_name_match.group(1)
                print(f"Extracted Inmate Name: {inmate_name}")
            
            # Save the full text to CSV
            writer.writerow([link, text])
        else:
            print(f"No text found for {link}\n")

print(f"Scraping complete. Data saved to {output_file}")