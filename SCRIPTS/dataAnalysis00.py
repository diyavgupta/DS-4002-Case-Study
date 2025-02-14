import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import string

nltk.download("stopwords")

DATA_PATH = "DATA/cleaned_final_statements.csv"
df = pd.read_csv(DATA_PATH)

if "Last Statement" not in df.columns:
    raise ValueError("Error: The dataset does not contain a 'last_statement' column.")

text = " ".join(df["Last Statement"].dropna())

stop_words = set(stopwords.words("english"))
text = text.translate(str.maketrans("", "", string.punctuation))  
words = text.lower().split() 
filtered_words = [word for word in words if word not in stop_words]  # Remove stopwords

# Generate word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",
    max_words=100
).generate(" ".join(filtered_words))

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # Hide axis
plt.title("Word Cloud of Inmate Last Statements")
plt.show()

# Save the word cloud as an image
OUTPUT_PATH = "outputs/wordcloud_last_statements.png"
wordcloud.to_file(OUTPUT_PATH)
print(f"Word cloud saved to {OUTPUT_PATH}")
