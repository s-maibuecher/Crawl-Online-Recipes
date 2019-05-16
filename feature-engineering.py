""" Script for Data Preprocessing, especially fields like ingredients which contains big JSON-like Objects: """

import pandas as pd
import xml.etree.ElementTree as ET
import os
import math

df = pd.read_csv('./CSV/recipe_dataframe.csv', encoding='utf-8', sep='\t')

print('Shape before feature engineering: ' + str(df.shape))

# Todo bind in later:
# df.drop(df.columns[df.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)
# df.set_index('id', inplace=True)

new_df = df.copy()

new_df['yield_amounts'] = None


def func_applied_to_category(xml_string):
    ''' function that extracts the values of the category feature: '''
    if str(xml_string) == 'nan':
        return None
    root = ET.fromstring(xml_string)
    root_type_attr = root.attrib['type']
    if root_type_attr == 'null':
        return None
    else:
        return root.find('./name').text


new_df['category'] = new_df['category'].apply(func_applied_to_category)

def func_applied_to_cuisines(xml_string):
    ''' function that extracts the values of the cuisines feature: '''
    if str(xml_string) == 'nan':
        return None
    xml_string = '<root>' +xml_string+ '</root>'
    root = ET.fromstring(xml_string)

    return '#'.join([x.text for x in root.findall('./item/name')])


new_df['cuisines'] = new_df['cuisines'].apply(func_applied_to_cuisines)


def func_applied_to_label(xml_string):
    ''' function that extracts the values of the label feature: '''
    if str(xml_string) == 'nan':
        return None
    root = ET.fromstring(xml_string)
    root_type_attr = root.attrib['type']
    if root_type_attr == 'null':
        return None
    else:
        return root.find('./text').text


new_df['label'] = new_df['label'].apply(func_applied_to_label)


# new nutrition columns:
nutr_col_names = ['Energie (kJ)', 'Energie (kcal)', 'Fett', 'davon gesättigte Fettsäuren', 'Kohlenhydrate', 'davon Zucker', 'Ballaststoffe', 'Eiweiß', 'Cholesterol', 'Salz']

for n in nutr_col_names:
    new_df['nutrition_' + n] = None


new_df['how_many_steps_needed'] = None

for index, row in df.iterrows():

    # Todo delete that for production:
    # FOR DEBUGGING
    if index > 50:
        break
    # END DEBUGGING

    #howmanystepsneeded:
    steps_tree = '<root>' + df['steps'][index] + '</root>'
    steps_root = ET.fromstring(steps_tree)
    all_steps = steps_root.findall('./item/index')
    steps_needed = max([int(x.text) for x in all_steps])
    new_df['how_many_steps_needed'][index] = steps_needed if steps_needed > 1 else None # if only one step is in the data, this seems to be a placeholder


    # fill nutrition columns:
    nut_tree = '<root>' + df['nutritionnames2compare'][index] + '</root>'
    nut_root = ET.fromstring(nut_tree)
    nut_items = nut_root.findall('./item')

    for item in nut_items:
        col_name = item.find('./name').text
        if col_name not in nutr_col_names:
            raise Exception('neues nutration Feld gefunden? '+ col_name)
        else:
            amount = item.find('./amount').text
            unit = item.find('./unit').text
            new_df['nutrition_' + col_name][index] = f'{amount} {unit}'

    print(f'Neue Zeile: {index}')

    # ingredients calculations:
    ingr_tree = '<root>' + df['ingredients'][index] + '</root>'

    yields_root = ET.fromstring('<root>' + df['yields'][index] + '</root>')

    yield_amounts = []
    yield_list = yields_root.findall('./item/yields')

    for y in yield_list:
        yield_amounts.append(y.text)

    new_df['yield_amounts'][index] = yield_amounts

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

    # till here: ingredients calculations



print('Shape after feature engineering: ' + str(new_df.shape))

# new_df.to_hdf('recipes.h5', key='df', mode='w')

new_df.to_csv(os.path.join('CSV', 'final_dataframe.csv'), sep='\t', encoding='utf-8')

# Todo unwichtige Zutaten wie Salz, Pfeffer werden nicht mitgeliefert, bekommen bei shipped den Wert False
#
# Todo xml rezept dateien einchecken
#
# Todo im oxygen abchecken, ob alle die gleichen nutritionnames beinhalten
#
# Todo alte große Spalten rauslöschen
#
# Todo nutrition Werte sind pro Portion??

# inspect columns:

# active is always True -> boring
# author are 17 unique values
# averageRating self-explaining
# canonical can be dropped
# category i've already extracted
# clonedFrom is interesting
# comment just two values, what for?
# createdAt can be timeplotted
# cuisines is extraced, if more that one value, than # seperated
# isDinnerToLunch is always False :)
# isExcludedFromIndex is always False :)
# label is extracted
# name, why is "Marokkanische Rindfleisch-Burger" used 8 times??
# nutrition extracted
# steps extracted - are there only none or 6 steps??
# subtitle only 374 unique values
# yieldType always servings -> boring
