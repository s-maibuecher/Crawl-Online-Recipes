import os
from lxml import etree
import pandas as pd

XML_SOURCE_DIRECTORY = 'http_requested_json_recipes'


# make directory if not exsists
if not os.path.exists('CSV'):
    os.makedirs('CSV')

# let's build a dict with key name (name for the pandas column), and a xpath (where to find in the recipe XML files):
# IMPORTANT: the XPath should be relative to the item (=recipe) element 
data_dict = {
    'name' : '/name',
    'url' : '/link',
    'subtitle' : '/headline',
    'nutritionnames2compare' : '/nutrition/item'
    # ...
}
    
data_column_list = []


def init_dataframe():
    '''
    init and returns the dataframe with the keys from the data_dict as columns values
    '''
    
    recipe_dataframe = pd.DataFrame(data_column_list)
    print(recipe_dataframe.head())

    return recipe_dataframe

def write_data_to_list(filepath):
    '''
    fetch the XPaths expressions from the data_dict and write the data to the data_column_list
    '''
    
    try:
        print(filepath)
        root = etree.parse(filepath)

        nr_of_items = len(root.xpath('/root/items/item'))

        for i in range(1, nr_of_items+1):
            
            XPATH_PREFIX = f'/root/items/item[{i}]'

            data_for_df = {}

            for dict_row in data_dict.keys():
                
                xpath_expression = XPATH_PREFIX + data_dict[dict_row]
                try:
                    element_list = root.xpath(xpath_expression)
                except etree.XPathEvalError as e:
                    print('Exception!', xpath_expression)
                    raise e
                finally:
                    # here you work with lists of https://lxml.de/api/lxml.etree._Element-class.html elements:
                    data_for_df = process_element_list(element_list)
                    
                    
                    # if len(element_list) == 1:
                    #   data_for_df[dict_row] = element_list[0]
                    # else:
                    #   data_for_df[dict_row] = [recursive_dict(e) for e in element_list]

                
            data_column_list.append(data_for_df)

    except etree.XMLSyntaxError as e:
        print('Fehler: lxml.etree.XMLSyntaxError!!')


def process_element_list(etree_element_list):
    '''
    function that returns all importants texts from xml structure:
    '''
    print([te.attrib for te in etree_element_list])
    return '' # hier weiter
    

def traverse_files():
    '''
    Returns all URLs to the recipe XML files.
    '''
    for subdir, dirs, files in os.walk( os.path.join(XML_SOURCE_DIRECTORY)):
        
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".xml") and file.startswith('recipe'):
                if file.startswith('recipe_debugging'): # for debugging!!
                    # for debugging!!
                    write_data_to_list(filepath)


def save_dataframe_to_csv(df):
    '''
    saves Dataframe to csv file
    '''
    df.to_csv(os.path.join('CSV', 'recipe_dataframe.csv'), sep='\t', encoding='utf-8')


def recursive_dict(element):
    '''
    convert xml structure into dict
    '''
    if element.text == None and len(element.attrib):
        return element.tag, element.attrib
    return element.tag, \
            dict(map(recursive_dict, element)) or element.text


if __name__ == '__main__':
    traverse_files()
    df = init_dataframe()
    save_dataframe_to_csv(df)


'''
description description/t
comment comment/t
difficulty  difficulty/t
prepTime    prepTime/t
totalTime   totalTime/t
servingSize servingSize/t
createdAt   createdAt/t
updatedAt   updatedAt/t
imageLink   imageLink/t
videoLink   videoLink/t
'''
