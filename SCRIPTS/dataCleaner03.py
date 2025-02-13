
import cv2
import numpy as np
import pytesseract
import requests
import csv
import os
from PIL import Image
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
import urllib3
import logging

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata/"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(filename='ocr_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import nltk
nltk.download('words')

def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image was unable to load.")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        binary_img = cv2.adaptiveThreshold(blurred, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        coords = np.column_stack(np.where(binary_img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle
        (h, w) = binary_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed_img = cv2.warpAffine(binary_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return deskewed_img
    except Exception as e:
        logging.error(f"Error preprocessing image {image_path}: {e}")
        return None
    
def load_negative_words(file_path):
    try:
        with open(file_path, 'r') as file:
            negative_words = set(file.read().splitlines())
        return negative_words
    except Exception as e:
        logging.error(f"Error preprocessing words: {e}")
        return set()

def create_custom_spell_checker(negative_words_file):
    spell = SpellChecker()
    nltk_words = set(nltk.corpus.words.words())
    target_words = {
        "Name:", "Received:", "Age:", "at", "time", "of", "Two", "Arrested", "Serve", "Serving" "(when received)", "Date of Offense", "Age at time of offense", 
        "Weight", "Native County", "State", "Prior Occupation", "Education Level", "years", 
        "Prior Prison Record", "Summary:", "Race of Victim(s):", "D.R. #", "County", "Prior", 
        "Occupation", "Education", "Level", "Summary", "Received", "Offense", "Native", "State", 
        "Record", "Co-Defendants", "Victim", "Race", "Gender", "Height", "Weight", "Eyes", "Hair",
        "Harris", "Texas", "New York", "Galveston", "Dallas", "El Paso", "Laborer", "Welder", 
        "Cook", "Public Safety Officer", "None", "Fry Cook", "Two Black Females", ""
    }
    
    negative_words = load_negative_words(negative_words_file)
    all_words = nltk_words.union(target_words).union(negative_words)
    spell.word_frequency.load_words(all_words)
    return spell

def correct_spelling(text, spell):
    corrected_text = []
    words = text.split()
    for word in words:
        if word in spell:
            corrected_text.append(word)
        else: 
            corrected_word = spell.correction(word)
            corrected_text.append(corrected_word if corrected_word else word)
    return ' '.join(corrected_text)

def scrape_HTML(url):
    try: 
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        inmate_info = soup.find('div', class_='inmate-info')  
        if inmate_info:
            text = inmate_info.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_JPG(url, spell):
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as img_file:
            for chunk in response.iter_content(chunk_size=8192):
                img_file.write(chunk)
        img = preprocess_image(temp_image_path)
        config = '--psm 12 --oem 3 -l eng'
      
        text = pytesseract.image_to_string(img, config=config)
        os.remove(temp_image_path)
        corrected_text = correct_spelling(text, spell)
        return corrected_text
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def sort(filename: str) -> list[str]:
    """Extract URLs from a CSV file"""
    urls = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append(row[8])  # Assuming URLs are in the 9th column
    return urls

def main():
    filename = "deathRow.csv"
    info_links = sort(filename)
    execution_number = 592
    output_file = "inmate_info.csv"
    negataive_words_file = "negative-words.txt"

    # Create a custom spell checker
    spell = create_custom_spell_checker(negataive_words_file)

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Execution Number", "Info"])

        for link in info_links:
            print(f"Scraping: {link}")
            if link.lower().endswith('.jpg') or link.lower().endswith('.jpeg'):
                text = scrape_JPG(link, spell)  # Apply spell checker to JPG outputs
            else:
                text = scrape_HTML(link)  # No spell checker for HTML outputs
            
            if text:
                print(f"Text from {link}:\n{text[:500]}...\n")
                writer.writerow([execution_number, text])
                execution_number -= 1
            else:
                print(f"No text found for {link}\n")

    print(f"Scraping complete. Data saved to {output_file}")

if __name__ == "__main__":
    main()