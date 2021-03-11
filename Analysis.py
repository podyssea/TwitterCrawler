import json

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

from source.database_classes import connect_to_mongo, Tweet, ProcessedTweet

#this python returns the classification report with the statistical analysis of the data fetched and processed from twitter
connect_to_mongo()

initial_df = pd.read_csv("data/tweets_saved.csv")
initial_df = initial_df[["emotion_label", "id_str"]]
initial_df['id_str']=initial_df['id_str'].astype(str)

results_df = pd.read_csv("data/tweets_processed.csv")
results_df = results_df[["emotion_label", "id_str"]]
results_df['id_str']=results_df['id_str'].astype(str)

merged = pd.merge(initial_df, results_df, on="id_str")
merged["id_str"] = merged["id_str"].apply(str)

SENTIMENT_TO_EMOTION = {
    "Excitement": "excitement",
    "Happiness": "happy",
    "Fear": "fear",
    "Surprise": "surprise",
    "Pleasant": "pleasant",
    "Anger": "anger",
}

def map_name_to_emotion(emotion):
    return SENTIMENT_TO_EMOTION.get(emotion, emotion)

merged["human_emotion_label"] = merged["emotion_label_y"].map(map_name_to_emotion)
merged = merged[["emotion_label_x", "id_str", "human_emotion_label"]]
merged.set_index("id_str", drop=True, inplace=True)

cl_report = classification_report(merged['human_emotion_label'].values, merged['emotion_label_x'].values, labels=merged['emotion_label_x'].unique().sort())
with open("results/classification_analysis.txt", "w") as f:
    f.write(cl_report)
