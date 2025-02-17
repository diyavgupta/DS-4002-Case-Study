## dataAnalysis02.py Script
## Required packages: pandas, nltk, vaderSentiment, matplotlib, seaborn, scikit-learn
## Params: input_file (Combined_Data.csv)
## Function: Extracts crime types from the Summary of Incident, clusters inmates by crime type, and visualizes sentiment scores by crime clusters.

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import re

# Load the dataset
input_file = 'DATA/Combined_Data.csv'
df = pd.read_csv(input_file)

df.columns = df.columns.str.strip()
df['Crime Type'] = df['Summary of Incident'].str.extract(r'(murder|homicide|assault|robbery|kidnapping|arson|rape|burglary|theft|fraud|drug)', flags=re.IGNORECASE, expand=False)

analyzer = SentimentIntensityAnalyzer()
df['Sentiment Score'] = df['Last Statement'].fillna('').apply(lambda x: analyzer.polarity_scores(x)['compound'])

crime_dummies = pd.get_dummies(df['Crime Type'], drop_first=True)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(crime_dummies)

kmeans = KMeans(n_clusters=5, random_state=42)
df['Crime Cluster'] = kmeans.fit_predict(scaled_features)

crime_clusters = {
    0: '1 (drug, burglary, fraud)',
    1: '2 (murder)',
    2: '3 (robbery)',
    3: '4 (assault)',
    4: '5 (rape)'
}

df['Cluster Label'] = df['Crime Cluster'].map(crime_clusters)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Cluster Label', y='Sentiment Score', palette='Set2')
plt.title('Sentiment Scores by Crime Clusters')
plt.xlabel('Crime Clusters')
plt.ylabel('Sentiment Score')
plt.xticks(rotation=15)
plt.savefig('OUTPUTS/crime_sentiment_clusters.png')

df[['Execution Number', 'Crime Type', 'Sentiment Score', 'Cluster Label']].to_csv('OUTPUTS/crime_sentiment_analysis.csv', index=False)
print("Crime sentiment analysis results saved to OUTPUTS/crime_sentiment_analysis.csv")
print("Plot saved to OUTPUTS/crime_sentiment_clusters.png")
