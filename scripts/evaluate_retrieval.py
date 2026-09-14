import pandas as pd
threshold = 0.75
df = pd.read_csv("evaluation/evaluation.csv")
df["Prediction"] = df["Top1_distance"] <= threshold

tp = df[(df["Label"] == 1) & (df["Prediction"] == True)]
print("TP : ", len(tp))

fp = df[(df["Label"] == 0) & (df["Prediction"] == True)]
print("FP : ", len(fp))

fn = df[(df["Label"] == 1) & (df["Prediction"] == False)]
print("FN : ", len(fn))

tn = df[(df["Label"] == 0) & (df["Prediction"] == False)]
print("TN : ", len(tn))

accuracy = (len(tp) + len(tn)) / (len(tp) + len(fp) + len(fn) + len(tn))
print("Accuracy : ", accuracy)

precision = len(tp) / (len(tp) + len(fp))
print("Precision : ", precision)

recall = len(tp) / (len(tp) + len(fn))
print("Recall : ", recall)