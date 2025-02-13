import csv
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Remove unwanted characters and extra spaces
    text = re.sub(r'[^\x00-\x7F]+', "", text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    
    # Remove unwanted phrases
    text = re.sub(r"Death Row Information skip to main content", "", text, flags=re.IGNORECASE)
    text = re.sub(r"TDCJ Number \d+", "", text)
    text = re.sub(r"Date of Birth \d{1,2}/\d{1,2}/\d{4}", "", text)
    text = re.sub(r'#\d+', "", text)
    text = re.sub(r'\([^)]*\)', "", text)  # Remove parenthetical content
    
    return text.strip()

def extract_inmate_info(text):
    text = clean_text(text)
    
    inmate_info = {
        "Name": "",
        "Date Received": "",
        "Age when Received": "",
        "Education Level": "",
        "Date of Offense": "",
        "Age at the time of Offense": "",
        "Prior Occupation": "",
        "Prior Prison Record": "",
        "Summary of Incident": "",
    }
    
    patterns = {
        "Name": r"Name[:\-]?\s*([^,]+)",
        "Date Received": r"Date Received[:\-]?\s*(\d{1,2}/\d{1,2}/\d{2,4})",
        "Age when Received": r"Age when Received[:\-]?\s*(\d+)",
        "Education Level": r"Education Level[:\-]?\s*(.*?)\s*(?:Date|Age|Prior|Summary|$)",
        "Date of Offense": r"Date of Offense[:\-]?\s*(\d{1,2}/\d{1,2}/\d{2,4})",
        "Age at the time of Offense": r"Age at the time of Offense[:\-]?\s*(\d+)",
        "Prior Occupation": r"Prior Occupation[:\-]?\s*(.*?)\s*(?:Prior|Summary|$)",
        "Prior Prison Record": r"Prior Prison Record[:\-]?\s*(.*?)\s*(?:Summary|$)",
        "Summary of Incident": r"Summary of Incident[:\-]?\s*(.*)"
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            inmate_info[field] = match.group(1).strip()
    
    return inmate_info

def process_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = ["Execution Number", "Name", "Date Received", "Age when Received", 
                  "Education Level", "Date of Offense", "Age at the time of Offense", 
                  "Prior Occupation", "Prior Prison Record", "Summary of Incident"]
        writer.writerow(header)

        for row in reader:
            if len(row) < 2:
                continue
            execution_number, info = row[0], row[1]
            
            if "Death Row Information" in info:
                inmate_info = extract_inmate_info(info)
                writer.writerow([
                    execution_number,
                    inmate_info.get("Name", ""),
                    inmate_info.get("Date Received", ""),
                    inmate_info.get("Age when Received", ""),
                    inmate_info.get("Education Level", ""),
                    inmate_info.get("Date of Offense", ""),
                    inmate_info.get("Age at the time of Offense", ""),
                    inmate_info.get("Prior Occupation", ""),
                    inmate_info.get("Prior Prison Record", ""),
                    inmate_info.get("Summary of Incident", "")
                ])



if __name__ == "__main__":
    input_csv = "DATA/inmate_info.csv"
    output_csv = "DATA/Clean_Inmate_info.csv"
    process_csv(input_csv, output_csv)
    print(f"Cleaned data saved to {output_csv}")
