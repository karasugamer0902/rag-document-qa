import pandas as pd
import numpy as np
thresholds = np.arange(0.6, 0.71, 0.01)
result = []
df = pd.read_csv("evaluation/evaluation.csv")
for threshold in thresholds:
    print("\nThreshold : ", threshold)

    df["Prediction"] = df["Top1_distance"] <= threshold

    tp = df[(df["Label"] == 1) & (df["Prediction"] == True)]

    fp = df[(df["Label"] == 0) & (df["Prediction"] == True)]

    fn = df[(df["Label"] == 1) & (df["Prediction"] == False)]

    tn = df[(df["Label"] == 0) & (df["Prediction"] == False)]

    accuracy = (len(tp) + len(tn)) / (len(tp) + len(fp) + len(fn) + len(tn))

    precision = len(tp) / (len(tp) + len(fp))

    recall = len(tp) / (len(tp) + len(fn))

    F1_score = (precision * recall) / (precision + recall) * 2

    data = {
        "Threshold": round(threshold, 2),
        "TP": len(tp),
        "FP": len(fp),
        "TN": len(tn),
        "FN": len(fn),
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": F1_score
    }

    result.append(data)

result_df = pd.DataFrame(result)

print(result_df)
print("\n\nMax : ", result_df["F1"].max())
print("\n\nIdxMax : ", result_df["F1"].idxmax())
print("\n\nIdx : ", result_df.iloc[result_df["F1"].idxmax()])

best_result = result_df[result_df["F1"] == result_df["F1"].max()]
print("\n\nBest Result : ")
print(best_result)

df["Prediction"] = df["Top1_distance"] <= 0.65
fp = df[(df["Label"] == 0) & (df["Prediction"] == True)]
print("\n\nFP List : ")
print(fp[["Question", "Top1_distance", "Category"]])

result_df.to_csv("evaluation/threshold_results.csv", index=False)