import os
from lxml import etree
import pandas as pd
from collections import defaultdict


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
        if not os.path.exists('PKL'):
            os.makedirs('PKL')
        
        # let's build a dict with key name (name for the pandas column), and a xpath (where to find in the recipe XML files):
        # IMPORTANT: the XPath should be relative to the item (=recipe) element 
        self.data_dict = {
            'name' : '/name',
            'url' : '/link',
            'id': '/id',
            'subtitle' : '/headline',
            'nutritionnames2compare' : '/nutrition/item',
            'description': '/description',
            'comment': '/comment',
            'category' : '/category',
            'difficulty': '/difficulty',
            'prepTime': '/prepTime',
            'totalTime': '/totalTime',
            'servingSize': '/servingSize',
            'createdAt': '/createdAt',
            'updatedAt': '/updatedAt',
            'imageLink': '/imageLink',
            'videoLink': '/videoLink',
            'ingredients': '/ingredients/item',
            'allergens': '/allergens/item',
            #'utensils': '/utensils/item', # is always an empty element till now
            # tags

                # Todo: Was mache ich mit diesen bisher leeren Listen Elementen wie utensils?
                # Leer führen sie zu Verarbeitungsfehlern. Daher auskommentiert.
                # Dann bekomme ich aber nicht mit, wenn die irgendwann gefüllt sein sollten...

            'cuisines' : '/cuisines/item',
            #'wines': '/wines/item', # Todo wirft Fehler
            # 'marketplaceItems' : '/marketplaceItems/item', # hier auch
            'author': '/author',
            'label' : '/label',
            'yieldType' : '/yieldType',
            'yields': '/yields/item',
            'steps': '/steps/item',
            'averageRating': '/averageRating',
            'ratingsCount': '/ratingsCount',
            'favoritesCount': '/favoritesCount',
            'active': '/active',
            'highlighted': '/highlighted',
            'isDinnerToLunch': '/isDinnerToLunch',
            'isExcludedFromIndex': '/isExcludedFromIndex',
            'isPremium': '/isPremium',
            'clonedFrom': '/clonedFrom',
            'canonical': '/canonical',
        }


        self.data_column_list = []
        self.recipe_df = None
    


    def init_dataframe(self):
        '''
        init and returns the dataframe with the keys from the self.data_dict as columns values
        '''
        print("Liste für das Dataframe:", self.data_column_list)
        recipe_dataframe = pd.DataFrame(self.data_column_list)
        print("Dataframe Head:", recipe_dataframe.head())

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
                        data_for_df[dict_row] = self.process_element_list(element_list)
                    
                    
                self.data_column_list.append(data_for_df)

        except etree.XMLSyntaxError as e:
            print('Fehler: lxml.etree.XMLSyntaxError!!')


    def process_element_list(self, etree_element_list):
        '''
        function that returns all importants texts from xml structure:
        '''

        all_type_of_elements = set([el.attrib['type'] for el in etree_element_list])

        if not len(all_type_of_elements) == 1:
            if len(all_type_of_elements) == 0:
                return ''
            raise MyBuildDataFrameException('Too many Types of XML Elements!')

        type_of_element = all_type_of_elements.pop()

        if type_of_element == 'int':
            return etree_element_list[0].text

        elif type_of_element == 'list':
            raise ToDoException(f'This Type of Element: {type_of_element} has not yet a execution path')

        elif type_of_element == 'dict':
            d = defaultdict(list)
            for el in etree_element_list:
                el, di = self.recursive_dict(el)
                d[el].append(di)

            return d

        elif type_of_element == 'str':
            return etree_element_list[0].text

        elif type_of_element == 'null':
            return ''

        elif type_of_element == 'float':
            return etree_element_list[0].text

        elif type_of_element == 'bool':
            return etree_element_list[0].text

        else:
        
            return ''


    def traverse_files(self):
        '''
        Returns all URLs to the recipe XML files.
        '''
        for subdir, dirs, files in os.walk( os.path.join(self.XML_SOURCE_DIRECTORY)):
            
            for file in files:
                filepath = subdir + os.sep + file

                if filepath.endswith(".xml") and file.startswith('recipe'):
                    #if file.startswith('recipe_debugging'): # for debugging!!
                        # for debugging!!
                        self.write_data_to_list(filepath)


    def save_dataframe_to_csv(self):
        '''
        saves Dataframe to csv file and to pkl file
        '''
        self.recipe_df.to_csv(os.path.join('CSV', 'recipe_dataframe.csv'), sep='\t', encoding='utf-8')

        #self.recipe_df.to_pickle(os.path.join('PKL', 'recipe_dataframe.pkl'))


    def recursive_dict(self, element):
        '''
        convert xml structure into dict
        '''
        if element.text == None and len(element.attrib):
            return element.tag, element.attrib
        return element.tag, \
                dict(map(self.recursive_dict, element)) or element.text


if __name__ == '__main__':

    df_builder = BuildDataframe('http_requested_json_recipes')
    df_builder.traverse_files()
    df_builder.init_dataframe()
    df_builder.save_dataframe_to_csv()


