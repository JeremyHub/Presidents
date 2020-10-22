import numpy as np
import pandas as pd

# apply the z-score method in Pandas using the .mean() and .std() methods
def z_score(df):
    # copy the dataframe
    df_std = df.copy()
    # apply the z-score method
    for column in df_std.columns:
        df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()

    return df_std

CSV_COLUMN_NAMES = ["role", 'isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
ROLES = ['pres', 'vp', 'va', 'ass']

# train_path = open('trainData.csv')
test_path = open('evalData.csv')

# train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
# call the z_score function
df_cars_standardized = z_score(test)

print(max(df_cars_standardized["4"]))
print(min(df_cars_standardized["4"]))
print(df_cars_standardized)