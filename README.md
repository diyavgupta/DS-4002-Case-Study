# DS-Project

This repository contains CSV data files, which were generated using python scripts to scrape and clean the data from the Texas Department of Criminal Justice website, spefically, the Death Row Information of all 592 inmates arrested in Texas since 1982.

#### Authors: Connor Powell, Delaney Brown, Diya Gupta

## Software Used
- Python version 3.11.4
- Packages used for cleaning, and required to replicate:
    - Pandas, BeautifulSoup, os, requests, cv2, numpy, tesseract/pytesseract, spellchecker, nltk, urllib3. 
- Coded on linux, using vscode and a virtual python enviorment.
  
## Documentation
- Repo Layout:

DS-Project/
├── DATA/                        
│   ├── cleaned_final_statements.csv (contains exc #, inmate name, final statement)
│   ├── Cleaned_Inmate_Info.csv (contains exc #, inmate name, dates of offense and incarceration, prior prison history, summary, etc)          
│   ├── negative-words.txt  (contains a list of negative connotation words)      
│   ├── deathRowInitial.csv  (contains exc #,inmate name ,TDCJ number, age, execution date, race, county, URL to inmate info)
│   ├── inmateinfoInitial.csv (contains all scrapped data from inmate info URLs, inlcuding tesseract output of JPG links)
│   ├── last_statement_links.csv (contains URL to last statements, and the scraped output of the html pages including inmates last statements)
│   ├── deathRow.html (the html file of https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html )
│
├── SCRIPTS/                     
│   ├── dataCleaner00.py   (scrapes and cleans deathRow.html and outputs to deathRowIntitial.csv)    
│   ├── dataCleaner01.py   (scrapes last statement links in deathRow.html and ouputs to last_statement_links.csv)       
│   ├── dataCleaner02.py   (cleans last_statement_links.csv and outputs to cleaned_final_statements.csv)       
│   ├── dataCleaner03.py   (scrapes deathRowInitial.csv using tesseract for JPG links and outputs to inmate_infoInitial.csv)       
│   ├── dataCleaner04.py   (cleans the html outputs in inmate_infoInitial.csv and outputs to Clean_Inmate_Info.csv)      
│   ├── dataCleaner05.py   (In Progress)     
│  
├── README.md              
│
├── LICENSE         
│                     
├── requirements.txt              
├── .gitignore                    