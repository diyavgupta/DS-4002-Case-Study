import csv
import re

def cut(text):
    if text == "N/A":
        return text
    text = re.sub(r'\b(Summary of Incident|Co-Defendants|Race and Gender of Victim|Employee Resources)\b.*', '', text, flags=re.IGNORECASE)  # Remove trailing fields
    text = re.sub(r'\s+', ' ', text).strip()  
    return text
def extract_inmate_info(text):
    patterns = {
        "Name": r"Name\s+([A-Za-z]+,\s+[A-Za-z]+)",
        "Date Received": r"Date Received\s+(\d{1,2}/\d{1,2}/\d{2,4})",
        "Age when Received": r"Age \(when Received\)\s+(\d+)",
        "Education Level": r"Education Level \(Highest Grade Completed\)\s+([\w\s]+)",
        "Date of Offense": r"Date of Offense\s+(\d{1,2}/\d{1,2}/\d{2,4})",
        "Age at the time of Offense": r"Age \(at the time of Offense\)\s+(\d+)",
        "Prior Occupation": r"Prior Occupation\s+([\w\s]+)",
        "Prior Prison Record": r"Prior Prison Record\s+([\w\s.,-]+)",
        "Summary of Incident": r"Summary of Incident\s+([\w\s.,-]+)(.+?)(?=\s+(Co-Defendants|Race and Gender of Victim|Employee Resources|$))",
        "Co-Defendants": r"Co-Defendants\s+([\w\s.,-]+)"
    }
    inmate_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            inmate_info[key] = cut(match.group(1))
        else:
            inmate_info[key] = "N/A"  

    return inmate_info

def process_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = ["Execution Number", "Name", "Date Received", "Age when Received", 
                  "Education Level", "Date of Offense", "Age at the time of Offense", 
                  "Prior Occupation", "Prior Prison Record", "Summary of Incident", "Co-Defendants"]
        writer.writerow(header)
       
        for row in reader:
            execution_number, info = row[0], row[1]
            if info.startswith("Death Row Information"):
                inmate_info = extract_inmate_info(info)
                writer.writerow([
                    execution_number,
                    inmate_info["Name"],
                    inmate_info["Date Received"],
                    inmate_info["Age when Received"],
                    inmate_info["Education Level"],
                    inmate_info["Date of Offense"],
                    inmate_info["Age at the time of Offense"],
                    inmate_info["Prior Occupation"],
                    inmate_info["Prior Prison Record"],
                    inmate_info["Summary of Incident"],
                    inmate_info["Co-Defendants"]
                ])


if __name__ == "__main__":
    input_csv = "inmate_info.csv"
    output_csv = "HTML_clean_InmateInfo.csv"
    process_csv(input_csv, output_csv)
    print(f"Cleaned data saved to {output_csv}")
