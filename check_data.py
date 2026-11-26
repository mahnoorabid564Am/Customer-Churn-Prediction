# performed basic functions on dataset
import pandas as pd

data = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print(data.head())
print(data.shape)
print(data.info())