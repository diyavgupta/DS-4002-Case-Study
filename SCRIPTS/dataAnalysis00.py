## dataAnalysis00.py Script
## Required packages: pandas, matplotlib, wordcloud, nltk
## Params: DATA_PATH (cleaned_final_statements.csv), OUTPUT_PATH (outputs/wordcloud_last_statements.png)
## Function: Generates a word cloud from inmate last statements, filtering out stopwords, punctuation, and phrases like 'last statement' and 'inmate declined'.

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import string

nltk.download("stopwords")

DATA_PATH = "DATA/cleaned_final_statements.csv"
df = pd.read_csv(DATA_PATH)

target_column = "Last Statement"
if target_column not in df.columns:
    raise ValueError("Error: The dataset does not contain a 'Last Statement' column.")

text = " ".join(df[target_column].dropna())
stop_words = set(stopwords.words("english"))
text = text.translate(str.maketrans("", "", string.punctuation))  
words = text.lower().split() 
filtered_words = [word for word in words if word not in stop_words and word not in ['last', 'statement', 'inmate', 'declined']]  # Remove stopwords and unwanted words

# Generate word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",
    max_words=100
).generate(" ".join(filtered_words))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Inmate Last Statements")
plt.savefig("OUTPUTS/wordcloud_last_statements.png")

print("Word cloud saved to OUTPUTS/wordcloud_last_statements.png")
