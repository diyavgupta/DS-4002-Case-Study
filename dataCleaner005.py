import csv
import re


CATEGORIES = [
    "Name", "TDCJ Number", "Date of Birth", "Date Received", "Age (when Received)",
    "Education Level", "Date of Offense", "Age (at the time of Offense)", "County",
    "Race", "Gender", "Hair Color", "Height", "Weight", "Eye Color", "Native County",
    "Native State", "Prior Occupation", "Prior Prison Record", "Summary of Incident",
    "Co-Defendants", "Race and Gender of Victim"
]

def clean_text(text):
    text = re.sub(r'[^\w\s.,:;/()-]', ' ', text)  
    text = re.sub(r'\s+', ' ', text) 
    return text.strip()

def extract_html_data(text):
    data = {category: "" for category in CATEGORIES}  

    patterns = {
        "Name": r"Inmate Information\s*Name\s*([\w\s,]+)",
        "TDCJ Number": r"TDCJ Number\s*([\d-]+)",
        "Date of Birth": r"Date of Birth\s*([\d/]+)",
        "Date Received": r"Date Received\s*([\d/]+)",
        "Age (when Received)": r"Age \(when Received\)\s*(\d+)",
        "Education Level": r"Education Level \(Highest Grade Completed\)\s*([\w\s\d]+)",
        "Date of Offense": r"Date of Offense\s*([\d/]+)",
        "Age (at the time of Offense)": r"Age \(at the time of Offense\)\s*(\d+)",
        "County": r"County\s*([\w\s]+)",
        "Race": r"Race\s*([\w\s]+)",
        "Gender": r"Gender\s*([\w\s]+)",
        "Hair Color": r"Hair Color\s*([\w\s]+)",
        "Height": r"Height \(in Feet and Inches\)\s*([\d\'\"]+)",
        "Weight": r"Weight \(in Pounds\)\s*([\d\s]+)",
        "Eye Color": r"Eye Color\s*([\w\s]+)",
        "Native County": r"Native County\s*([\w\s]+)",
        "Native State": r"Native State\s*([\w\s]+)",
        "Prior Occupation": r"Prior Occupation\s*([\w\s,]+)",
        "Prior Prison Record": r"Prior Prison Record\s*([\w\s\d-]+)",
        "Summary of Incident": r"Summary of Incident\s*([\w\s.,:;()-]+)",
        "Co-Defendants": r"Co-Defendants\s*([\w\s,]+)",
        "Race and Gender of Victim": r"Race and Gender of Victim\s*([\w\s/]+)"
    }

    for category, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[category] = match.group(1).strip()

    return data

def extract_plain_text_data(text):
    data = {category: "" for category in CATEGORIES}  
    lines = text.split("\n") 

    for line in lines:
        line = clean_text(line)  
        for category in CATEGORIES:
            if re.search(rf'\b{re.escape(category)}\b', line, re.IGNORECASE):
                value = re.sub(rf'\b{re.escape(category)}\b', '', line, flags=re.IGNORECASE).strip()
                data[category] = value
                break  

    return data

def clean_and_write_csv(input_file, output_file):
    with open(input_file, mode="r", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        
        reader = csv.reader(infile)
        fieldnames = ["Execution Number"] + CATEGORIES  
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()  

        for row in reader:
            execution_number = row[0] 
            text = " ".join(row[1:])  

            if text.startswith("Death Row Information"):
                structured_data = extract_html_data(text)
            else:
                structured_data = extract_plain_text_data(text)

            structured_data["Execution Number"] = execution_number  

           
            writer.writerow(structured_data)


input_file = "inmate_info.csv"
output_file = "cleaned_inmate_info.csv"
clean_and_write_csv(input_file, output_file)

print(f"Cleaning complete. Structured data saved to {output_file}")