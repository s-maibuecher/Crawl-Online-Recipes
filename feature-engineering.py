""" Script for Data Preprocessing, especially fields like ingredients which contains big JSON-like Objects: """

import pandas as pd
import xml.etree.ElementTree as ET

df = pd.read_csv('./CSV/recipe_dataframe.csv', encoding='utf-8', sep='\t')

new_df = df.copy()

for index, row in df.iterrows():
    ingr = '<root>' + df['ingredients'][index] + '</root>'

    yields_root = ET.fromstring(df['yields'][index])

    root = ET.fromstring(ingr)

    items = root.findall('item') #take the family name to normalize the ingredients

    for item in items:
        item_name = item.find('./family/name')
        column_name = f'ingr_{item_name.text}'
        if not column_name in new_df.columns:
            new_df[column_name] = None

        item_id = item.find('./id').text

        yield_item = yields_root.find(f'./ingredients/item[id="{item_id}"]')

        try:
            yield_string = yield_item.find('./amount').text + ' ' + yield_item.find('./unit').text
        except TypeError:
            yield_string = None

        new_df[column_name][index] = yield_string




print(new_df.shape)


# Todo unwichtige Zutaten wie Salz, Pfeffer werden nicht mitgeliefert, bekommen bei shipped den Wert False
#
# Todo xml rezept dateien einchecken
#
# Todo im oxygen abchecken, ob alle die gleichen nutritionnames beinhalten
