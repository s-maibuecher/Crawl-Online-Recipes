""" Script for Data Preprocessing, especially fields like ingredients which contains big JSON-like Objects: """

import pandas as pd
import xml.etree.ElementTree as ET

df = pd.read_csv('./CSV/recipe_dataframe.csv', encoding='utf-8', sep='\t')

new_df = df.copy()

new_df['yield_amounts'] = None

for index, row in df.iterrows():
    print(f'Neue Zeile: {index}')

    ingr_tree = '<root>' + df['ingredients'][index] + '</root>'

    yields_root = ET.fromstring('<root>' + df['yields'][index] + '</root>')

    yield_amounts = []
    yield_list = yields_root.findall('./item/yields')

    for y in yield_list:
        yield_amounts.append(y.text)

    new_df['yield_amounts'][index] = yield_amounts

    # Todo die meißten Gerichte haben ['2', '3', '4'] yield amounts, siehe Grafik
    # das hier sind Werte aus den ersten 250 Rezepten
    # einige haben aber auch ['2', '4', '6', '8']
    # und eins hat [3]
    # also müssen die Stückzahlen unten genormt werden
    # soll ich noch aufnehmen welches Rezept wieviele yields anbietet?

    root = ET.fromstring(ingr_tree)

    items = root.findall('item') #take the family name to normalize the ingredients

    for item in items:
        item_name = item.find('./family/name')
        try:
            column_name = f'ingr_normalized_{item_name.text}'
        except AttributeError: # when <family type="null"/>
            column_name = f'ingr_normalized_{item.text}'

        if not column_name in new_df.columns:
            new_df[column_name] = None

        item_id = item.find('./id').text

        yield_item = yields_root.find(f'./item[1]/ingredients/item[id="{item_id}"]')
        yield_item_amount = int(yields_root.find(f'./item[1]/yields').text)

        try:
            yield_string = yield_item.find('./amount').text + '/' + str(yield_item_amount) + ' ' + yield_item.find('./unit').text
        except TypeError:
            yield_string = None

        new_df[column_name][index] = yield_string

        # todo test that ;)


print(new_df.shape)


# Todo unwichtige Zutaten wie Salz, Pfeffer werden nicht mitgeliefert, bekommen bei shipped den Wert False
#
# Todo xml rezept dateien einchecken
#
# Todo im oxygen abchecken, ob alle die gleichen nutritionnames beinhalten
