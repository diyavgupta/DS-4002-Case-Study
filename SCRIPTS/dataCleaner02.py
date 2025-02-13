import csv
import re

def find(text):
    match = re.search(r"Inmate:\s*([A-Za-z]+(?:[,\s]+[A-Za-z]+)*)", inmate_name)
    if match:
        inmate_name = match.group(1)
        return inmate_name
    return ""
    
def cut(text):
    point = text.find("Employee Resources")
    if point != -1:
        text = text[:point].strip()
        return text
def slice(inmate_name):
    inmate_name = re.sub(r"[^A-Za-z,\s].*", "", inmate_name).strip()
    inmate_name = re.sub(r"\bTDCJ\b", "", inmate_name, flags=re.IGNORECASE).strip()
    return inmate_name
def extract_info(text):
    inmate_name = ""
    last_statement = ""
    modified = cut(text)
    lines = modified.split("\n")
    for line in lines:
        if "Last Statement:" in line:
            last_statement = line.split("Last Statement:")[1].strip()
        if "Inmate:" in line:
            inmate_name = line.split("Inmate:")[1].strip()
    inmate_name = slice(inmate_name)
    return inmate_name, last_statement

input_file = "last_statements.csv"
output_file = "cleaned_last_statements.csv"

with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["Execution Number", "Inmate Name", "Last Statement"])
    
    for idx, row in enumerate(reader):
        text = row["Text"]
        inmate_name, last_statement = extract_info(text)
        execution_number = 591 - idx
        writer.writerow([execution_number, inmate_name, last_statement])

print(f"Cleaned data saved to {output_file}")
