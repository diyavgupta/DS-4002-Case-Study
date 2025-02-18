
# DS Project: Texas Death Row Last Statements Analysis

#### Authors: Connor Powell, Delaney Brown, Diya Gupta (leader)

## Overview  
This repository contains CSV data files generated using Python scripts to scrape and clean data from the Texas Department of Criminal Justice website, specifically the Death Row Information of all 592 inmates arrested in Texas since 1982. Our dataset includes the last statements of death row inmates, scripts to clean the data and quantify remorse using sentiment analysis tools, and visualizations demonstrating early findings.  

Our project examines the amount of remorse expressed by Texas death row prisoners in their last words in relation to:  
- The amount of time spent on death row  
- The year of execution (before or after increased sentencing restrictions)  
- The type of crime committed  

---

##  Software and Platforms  

- **Primary Software:** Python 3.11.4  
- **Python Packages Used for cleaning, and required to replicate:**  
  `pandas`, `BeautifulSoup`, `os`, `requests`, `cv2`, `urllib3`, `numpy`, `tesseract/pytesseract`, `spellchecker`, `nltk`  
- **Development Environment:**  
  - Linux  
  - Visual Studio Code  
  - Virtual Environment  

---

## Documentation Map  

This repository contains the following files and directories:  

### ** DATA** (CSV files containing raw and processed data)    
- `cleaned_final_statements.csv` – Execution #, inmate name, final statement  
- `Clean_Inmate_Info.csv` – Execution #, inmate name, dates of offense and incarceration, prior prison history, summary, etc.  
- `deathRowInitial.csv` – Execution #, inmate name, TDCJ number, age, execution date, race, county, URL to inmate info  
- `deathRow.html` – HTML file from [TDCJ Death Row Executions](https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html)  
- `inmate_infoInitial.csv` – Scraped data from inmate info URLs, including Tesseract OCR output of JPG links  
- `last_statement_links.csv` – URLs to last statements & scraped HTML outputs of inmates’ final words  
- `negative-words.txt` – List of negative connotation words for sentiment analysis
- 'Combined_Data.csv' - Final cleaned dataset with sentiment analysis
- `Data Appendix - Project 1.pdf`  

### ** SCRIPTS** (Python scripts for scraping & cleaning)  
- `dataCleaner00.py` – Scrapes & cleans `deathRow.html`, outputs `deathRowInitial.csv`  
- `dataCleaner01.py` – Scrapes last statement links from `deathRow.html`, outputs `last_statement_links.csv`  
- `dataCleaner02.py` – Cleans `last_statement_links.csv`, outputs `cleaned_final_statements.csv`  
- `dataCleaner03.py` – Scrapes `deathRowInitial.csv`, processes JPG links via Tesseract OCR, outputs `inmate_infoInitial.csv`  
- `dataCleaner04.py` – Cleans HTML outputs from `inmate_infoInitial.csv`, outputs `Clean_Inmate_Info.csv`  
- `dataCleaner05.py` – *(In Progress)*  

### ** OUTPUTS**  
- 'crime_sentiment_analysis.csv' - Cleaned dataset used to produce 'crime_sentiment_clusters.png'
- 'crime_sentiment_clusters.png' - Boxplot displaying sentiment scores by crime type
- 'statement_analysis_results.csv' - Cleaned dataset used to produce 'time_sentiment_scatter.png' 
- 'time_sentiment_scatter.png' - Scatterplot of sentiment scores over time
- 'wordcloud_last_statements.png' - Word cloud of last statements

### **LICENSE** and **README**

### 'requirements.txt' file (for reproducibility)

### 'References - Project 1.pdf'
---

##  Instructions for Reproducing Results  

To replicate our results, follow these steps:  

1. To reproduce the results of our project, start by cloning the repository and downloading the requirements.txt file to ensure all the proper packages are available.
2. Run dataCleaner00, which inputs the HTML script from the TDJC website and scrapes the data into the output deathRowInitial.csv.
3. Run dataCleaner01, which inputs the HTML script from TDJC and follows and scrapes the last statement link for each input outputting them into last_statement_links.csv
4. Run dataCleaner02, which inputs the last_statement_links.csv file, and cleans it outputting the data into cleaned_last_statements.csv
5. Run dataCleaner03, which inputs deathRowInitial.csv, following the links and preceding to scrape them using configured Tesseract OCR for JPG images, as well as scraping all the info from the HTML versions outputting to inmate_infoInitial.csv.
6. Run dataCleaner04, which inputs inmate_infoInitial.csv and cleans the data from the HTML outputs, placing the cleaned data in Clean_Inmate_info.csv


