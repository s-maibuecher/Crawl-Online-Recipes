import os
from lxml import etree
import pandas as pd
import unittest
from build_dataframe import BuildDataframe

class TestBuildDataframe(unittest.TestCase):
    

    # @classmethod
    # def setUpClass(cls):
    #     print('setupClass')

    # @classmethod
    # def tearDownClass(cls):
    #     print('teardownClass')
    
    def setUp(self):
        print('setUp')
        # connect to XML test file:
        self.bdf_object = BuildDataframe('http_requested_json_recipes')

    def tearDown(self):
        print('tearDown\n')

    # def init_dataframe(self):
    #     '''
    #     init and returns the dataframe with the keys from the self.data_dict as columns values
    #     '''
        
    #     recipe_dataframe = pd.DataFrame(self.data_column_list)
    #     print(recipe_dataframe.head())

    #     self.recipe_df = recipe_dataframe

    # def write_data_to_list(self, filepath):
    #     '''
    #     fetch the XPaths expressions from the self.data_dict and write the data to the self.data_column_list
    #     '''
        
    #     try:
    #         print(filepath)
    #         root = etree.parse(filepath)

    #         nr_of_items = len(root.xpath('/root/items/item'))

    #         for i in range(1, nr_of_items+1):
                
    #             XPATH_PREFIX = f'/root/items/item[{i}]'

    #             data_for_df = {}

    #             for dict_row in self.data_dict.keys():
                    
    #                 xpath_expression = XPATH_PREFIX + self.data_dict[dict_row]
    #                 try:
    #                     element_list = root.xpath(xpath_expression)
    #                 except etree.XPathEvalError as e:
    #                     print('Exception!', xpath_expression)
    #                     raise e
    #                 finally:
    #                     # here you work with lists of https://lxml.de/api/lxml.etree._Element-class.html elements:
    #                     data_for_df = self.process_element_list(element_list)
                        
                        
    #                     # if len(element_list) == 1:
    #                     #   data_for_df[dict_row] = element_list[0]
    #                     # else:
    #                     #   data_for_df[dict_row] = [recursive_dict(e) for e in element_list]

                    
    #             self.data_column_list.append(data_for_df)

    #     except etree.XMLSyntaxError as e:
    #         print('Fehler: lxml.etree.XMLSyntaxError!!')


    # def process_element_list(self, etree_element_list):
    #     '''
    #     function that returns all importants texts from xml structure:
    #     '''
    #     print([te.attrib for te in etree_element_list])
    #     return '' # hier weiter

    #     '''
    #     possible types:
    #     int
    #     list
    #     dict
    #     str
    #     null
    #     float
    #     bool
    #     '''


    def test_traverse_files(self):
        '''
        Returns all URLs to the recipe XML files.
        '''
        self.assertEqual(type(self.bdf_object.XML_SOURCE_DIRECTORY), str)

        # for subdir, dirs, files in os.walk( os.path.join(self.XML_SOURCE_DIRECTORY)):
            
        #     for file in files:
        #         filepath = subdir + os.sep + file

        #         if filepath.endswith(".xml") and file.startswith('recipe'):
        #             if file.startswith('recipe_debugging'): # for debugging!!
        #                 # for debugging!!
        #                 self.write_data_to_list(filepath)


    # def save_dataframe_to_csv(self):
    #     '''
    #     saves Dataframe to csv file
    #     '''
    #     self.recipe_df.to_csv(os.path.join('CSV', 'recipe_dataframe.csv'), sep='\t', encoding='utf-8')


    # def recursive_dict(self, element):
    #     '''
    #     convert xml structure into dict
    #     '''
    #     if element.text == None and len(element.attrib):
    #         return element.tag, element.attrib
    #     return element.tag, \
    #             dict(map(recursive_dict, element)) or element.text


if __name__ == '__main__':
    unittest.main()