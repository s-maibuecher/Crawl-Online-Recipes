import os
from lxml import etree
import pandas as pd


class MyBuildDataFrameException(Exception):
    """Raise for my specific kind of exception"""

class ToDoException(Exception):
    """This Type of Elements has not yet a execution path"""

class BuildDataframe(object):
    """build a pandas dataframe from several recipes xml files"""
    
    def __init__(self, xml_directory_name):

        self.XML_SOURCE_DIRECTORY = xml_directory_name

        # make directory if not exsists
        if not os.path.exists('CSV'):
            os.makedirs('CSV')
        
        # let's build a dict with key name (name for the pandas column), and a xpath (where to find in the recipe XML files):
        # IMPORTANT: the XPath should be relative to the item (=recipe) element 
        self.data_dict = {
            'name' : '/name',
            'url' : '/link',
            'subtitle' : '/headline',
            'nutritionnames2compare' : '/nutrition/item'
            # ...
        }

        self.data_column_list = []
        self.recipe_df = None
    
    


    def init_dataframe(self):
        '''
        init and returns the dataframe with the keys from the self.data_dict as columns values
        '''
        
        recipe_dataframe = pd.DataFrame(self.data_column_list)
        print(recipe_dataframe.head())

        self.recipe_df = recipe_dataframe

    def write_data_to_list(self, filepath):
        '''
        fetch the XPaths expressions from the self.data_dict and write the data to the self.data_column_list
        '''
        
        try:
            print(filepath)
            root = etree.parse(filepath)

            nr_of_items = len(root.xpath('/root/items/item'))

            for i in range(1, nr_of_items+1):
                
                XPATH_PREFIX = f'/root/items/item[{i}]'

                data_for_df = {}

                for dict_row in self.data_dict.keys():
                    
                    xpath_expression = XPATH_PREFIX + self.data_dict[dict_row]
                    try:
                        element_list = root.xpath(xpath_expression)
                    except etree.XPathEvalError as e:
                        print('Exception!', xpath_expression)
                        raise e
                    finally:
                        # here you work with lists of https://lxml.de/api/lxml.etree._Element-class.html elements:
                        data_for_df = self.process_element_list(element_list)
                        
                        
                        # if len(element_list) == 1:
                        #   data_for_df[dict_row] = element_list[0]
                        # else:
                        #   data_for_df[dict_row] = [recursive_dict(e) for e in element_list]

                    
                self.data_column_list.append(data_for_df)

        except etree.XMLSyntaxError as e:
            print('Fehler: lxml.etree.XMLSyntaxError!!')


    def process_element_list(self, etree_element_list):
        '''
        function that returns all importants texts from xml structure:
        '''

        all_type_of_elements = set([el.attrib['type'] for el in etree_element_list])

        if not len(all_type_of_elements) == 1:
            raise MyBuildDataFrameException('Too many Types of XML Elements!')

        type_of_element = all_type_of_elements.pop()

        print(type_of_element)

        if type_of_element == 'int':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'list':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'dict':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'str':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'null':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'float':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')
        elif type_of_element == 'bool':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')

        
        return '' # hier weiter


    def traverse_files(self):
        '''
        Returns all URLs to the recipe XML files.
        '''
        for subdir, dirs, files in os.walk( os.path.join(self.XML_SOURCE_DIRECTORY)):
            
            for file in files:
                filepath = subdir + os.sep + file

                if filepath.endswith(".xml") and file.startswith('recipe'):
                    if file.startswith('recipe_debugging'): # for debugging!!
                        # for debugging!!
                        self.write_data_to_list(filepath)


    def save_dataframe_to_csv(self):
        '''
        saves Dataframe to csv file
        '''
        self.recipe_df.to_csv(os.path.join('CSV', 'recipe_dataframe.csv'), sep='\t', encoding='utf-8')


    def recursive_dict(self, element):
        '''
        convert xml structure into dict
        '''
        if element.text == None and len(element.attrib):
            return element.tag, element.attrib
        return element.tag, \
                dict(map(recursive_dict, element)) or element.text


if __name__ == '__main__':

    df_builder = BuildDataframe('http_requested_json_recipes')
    df_builder.traverse_files()
    df_builder.init_dataframe()
    df_builder.save_dataframe_to_csv()


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
    ingredients ingredients/item
    allergens   allergens/item
    utensils    utensils/item


    alle items mit vorgänger namen speichern?


    was ist mit?

    tags/item
    cuisines/item
    '''
