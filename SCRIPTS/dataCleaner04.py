import csv
import re

def clean(text):
    if not text:
        return ""
    text = re.sub(r"TDCJ Number \d+", "", text)
    text = re.sub(r"Date of Birth \d{1,2}/\d{1,2}/\d{4}", "", text)
    text = re.sub(r'#\d+', "", text)
    text = re.sub(r'[^\x00-\x7F]+', "", text)

    text = re.sub(r"\([^)]*\)", "", text)
    unwanted_phrases = [
        "Date of Birth", "County", "Race", "Gender", "Hair Color", "Height", 
        "Weight", "Eye Color", "Native County", "Native State", "Native", 
        "Employee Resources", "Report Waste, Fraud and Abuse of TDCJ Resources", 
        "State Energy Savings Program", "TDCJ Intranet", "Site Policies", 
        "Office of the Inspector General", "TexasOnline", "Texas Veterans Portal", 
        "Texas Homeland Security", "TRAIL Statewide Search", "Where the Money Goes", 
        "Adobe Reader", "Texas Department of Criminal Justice", "PO Box 99", 
        "Huntsville, Texas 77342-0099", "295-6371", "Age", "Co.", "TDJC", "TDJC#", "Criminal Justice", "Victim", "Department of"
    ]
    for phrase in unwanted_phrases:
        text = re.sub(f"{phrase} [^ ]+", "", text)
    text = re.sub(r"Height [0-9]+′ [0-9]+″ Weight [0-9]+", "", text)
    text = re.sub(r"Height \d+ \d+ Weight \d+", "", text)

    text = re.sub(r"Native [^,]+", "", text) 
    text = re.sub(r"Height [^,]+", "", text)  # Remove native state and following info
    
    text = re.sub(r"\s+", " ", text).strip()

    return text
def slice(text):
    # Find the positions of "Age at the time of Offense" and "Prior Occupation"
    start_point = text.find("Age at the time of Offense")
    end_point = text.find("Prior Occupation")
    
    # If both points are found, remove the text in between
    if start_point != -1 and end_point != -1:
        # Keep the part before "Age at the time of Offense" and after "Prior Occupation"
        text = text[:start_point] + "Age at the time of Offense, Prior Occupation" + text[end_point + len("Prior Occupation"):].strip()

    return text
   
def cut(text): 
    point = text.find("Co-Defendants")
    if point != -1:
        text = text[:point].strip()
    return text

def extract_inmate_info(text):
    text = clean(text)
    text = slice(text)
    text = cut(text)
    
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
    
    fields = [
        "Name", "Date Received", "Age,,", "Education Level", "Date of Offense", 
        "Age,,", "Prior Occupation", "Prior Prison Record", "Summary of Incident", 
    ]

    # Iterate through fields to extract information
    for field in fields:
        if field in text:
            # Split the text at the field name and take the part after it
            parts = text.split(field, 1)
            if len(parts) > 1:
                value = parts[1].strip()
                # Remove any trailing field names or irrelevant text
                for next_field in fields:
                    if next_field in value:
                        value = value.split(next_field)[0].strip()
                # Assign the value to the corresponding key
                if field == "Age":
                    if "when Received" in text:
                        inmate_info["Age when Received"] = value
                    elif "at the time of Offense" in text:
                        clean_val = value.split(' ')[0]
                        inmate_info["Age at the time of Offense"] = clean_val
                else:
                    inmate_info[field] = value

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
                    inmate_info["Summary of Incident"]
                ])

if __name__ == "__main__":
    input_csv = "DATA/inmate_info.csv"
    output_csv = "DATA/HTML_clean_InmateInfo.csv"
    process_csv(input_csv, output_csv)
    print(f"Cleaned data saved to {output_csv}")