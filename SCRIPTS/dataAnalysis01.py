## dataAnalysis01.py Script
## Required packages: pandas, nltk, vaderSentiment, matplotlib, seaborn
## Params: input_file (Combined_Data.csv)
## Function: Analyzes the length of final statements and calculates the time spent on death row (date received - execution date) and performs sentiment analysis on the final statements using VADER and explores potential correlations between statement length, sentiment, and time spent on death row.

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import matplotlib.pyplot as plt

input_file = 'DATA/Combined_Data.csv'
df = pd.read_csv(input_file)
df.columns = df.columns.str.strip()

# Convert dates to datetime objects
df['Date Received'] = pd.to_datetime(df['Date Received'], errors='coerce')
df['Date Executed'] = pd.to_datetime(df['Date Executed'], errors='coerce')
df['Days on Death Row'] = (df['Date Executed'] - df['Date Received']).dt.days

analyzer = SentimentIntensityAnalyzer()
df['Sentiment Score'] = df['Last Statement'].fillna('').apply(lambda x: analyzer.polarity_scores(x)['compound'])

# Scatter plot for Days on Death Row vs Sentiment Score
plt.figure(figsize=(10, 6))
plt.scatter(df['Days on Death Row'], df['Sentiment Score'], alpha=0.6, c=df['Sentiment Score'], cmap='viridis')
plt.colorbar(label='Sentiment Score')
plt.xlabel('Days on Death Row')
plt.ylabel('Sentiment Score')
plt.title('Days on Death Row vs Sentiment Score')
plt.savefig('OUTPUTS/time_sentiment_scatter.png')

print("Scatter plot saved to OUTPUTS/time_sentiment_scatter.png")

