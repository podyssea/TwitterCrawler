import json

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

from source.database_classes import connect_to_mongo, Tweet, ProcessedTweet

connect_to_mongo()

# # Load mechanical turk results into familiar format
# initial_df = pd.read_csv("data/tweets-raw.csv")
# initial_df = initial_df[["emotion_label", "id_str"]]
# initial_df = initial_df["id_str"].apply(str)
#
# resutls_df = pd.read_csv("data/tweets-processed.csv")
# results_df = results_df[["emotion_label", "id_str"]]
# results_df["id_str"] = results_df["id_str"].apply(str)
# results_df.rename(columns={'emotion_label': 'Answer.emotion.label'}

initial_df = pd.read_csv("data/tweets-raw.csv")
initial_df = initial_df[["emotion_label", "id_str"]]
initial_df['id_str']=initial_df['id_str'].astype(str)

results_df = pd.read_csv("data/tweets-processed.csv")
results_df = results_df[["emotion_label", "id_str"]]
results_df['id_str']=results_df['id_str'].astype(str)

merged = pd.merge(initial_df, results_df, on="id_str")
merged["id_str"] = merged["id_str"].apply(str)

MTURK_TO_EMOTION = {
    "Excitement": "excitement",
    "Happiness": "happy",
    "Fear": "fear",
    "Surprise": "surprise",
    "Pleasant": "pleasant",
    "Anger": "anger",
}
def map_mturk_name_to_emotion(mturk):
    return MTURK_TO_EMOTION.get(mturk, mturk)

merged["human_emotion_label"] = merged["emotion_label_y"].map(map_mturk_name_to_emotion)
merged = merged[["emotion_label_x", "id_str", "human_emotion_label"]]
merged.set_index("id_str", drop=True, inplace=True)

# load processed tweets
# queryset = ProcessedTweet.objects.all()
# pt_df = pd.DataFrame(list(map(lambda x: json.loads(x.to_json()), queryset)))
# pt_df = pt_df[["id_str", "emotion_label", "raw_text", "processed_text"]]
# pt_df.set_index(["id_str"], inplace=True, drop=True)
#
# df = merged.merge(pt_df, how="inner", left_index=True, right_index=True)

cl_report = classification_report(merged['human_emotion_label'].values, merged['emotion_label_x'].values, labels=merged['emotion_label_x'].unique().sort())
with open("results/cl_report.txt", "w") as f:
    f.write(cl_report)
