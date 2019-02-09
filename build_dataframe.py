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
	'name' : '/name/text()',
	'url' : '/link/text()'
	# ...
}
	
data_column_list = []
temp_dict = {}

def init_dataframe():
	'''
	init and returns the dataframe with the keys from the data_dict as columns values
	'''
	recipe_dataframe = pd.DataFrame(temp_dict)
	print(recipe_dataframe.head())

	return recipe_dataframe

def write_data_to_list(filepath):
	'''
	fetch the XPaths expressions from the data_dict and write the data to the data_column_list
	'''
	try:
		print(filepath)
		root = etree.parse(filepath)
		XPATH_PREFIX = '/root/items/item'

		for dict_row in data_dict.keys():
			t = root.xpath(XPATH_PREFIX + data_dict[dict_row])
			temp_dict[dict_row] = t


	except etree.XMLSyntaxError as e:
		print('Fehler: lxml.etree.XMLSyntaxError!!')


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

if __name__ == '__main__':
	traverse_files()
	df = init_dataframe()
	save_dataframe_to_csv(df)
