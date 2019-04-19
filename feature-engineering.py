""" Script for Data Preprocessing, especially fields like ingredients which contains big JSON-like Objects: """

import pandas as pd

df = pd.read_csv('./CSV/recipe_dataframe.csv', encoding='utf-8') # first version needs also the sep='\t' seperator

print(df['ingredients'][0])


# Todo: und weiter geht's

# ... fetch all ingredients of all recipes and onehotecode these fields to every row...