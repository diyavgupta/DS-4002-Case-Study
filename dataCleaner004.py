from PIL import Image, ImageOps, ImageEnhance
from bs4 import BeautifulSoup
import pytesseract
import requests
import csv
import os


def preProcess(img_path):
    img = Image.open(img_path)
    gray = ImageOps.grayscale(img)
    enhancer = ImageEnhance.Contrast(gray)
    contrast_img = enhancer.enhance(2.0) 
    scale_factor = 2
    resized = contrast_img.resize((contrast_img.width * scale_factor, contrast_img.height * scale_factor), resample=Image.LANCZOS)
    return resized


def scrape_HTML(url):
    try: 
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None


def scrape_JPG(url):
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as img_file:
            for chunk in response.iter_content(chunk_size=8192):
                img_file.write(chunk)
        img = preProcess(temp_image_path)
        
        
        config = '--psm 4 -l eng'  
        text = pytesseract.image_to_string(img, config=config)
        os.remove(temp_image_path)
        return text
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


def sort(filename: str) -> list[str]:
    urls = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append(row[8])  
    return urls


filename = "deathRow.csv"
info_links = sort(filename)
execution_number = 592
output_file = "inmate_info.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Execution Number", "Info"])  
    for link in info_links:
        print(f"Scraping: {link}")
        if link.lower().endswith('.jpg') or link.lower().endswith('.jpeg'):
            text = scrape_JPG(link)  
        else:
            text = scrape_HTML(link)  

      
        if text:
            print(f"Text from {link}:\n{text[:500]}...\n")  
            writer.writerow([execution_number, text])
            execution_number -= 1  
        else:
            print(f"No text found for {link}\n")

print(f"Scraping complete. Data saved to {output_file}")