''' # To-Do: Get recipes via cURL, because scrapy + selenium slows down after about 150 button clicks
'''

'''
Script to load the recipes via HTTP Request calls, instead of the Scrapy/Selenium solution:
'''

import os
import json
import dicttoxml
from pprint import pprint


JSON_DIRECTORY_NAME = 'http_requested_json_recipes'

HOW_MANY_RECIPES = 2250

# make directory if not exsists
if not os.path.exists(JSON_DIRECTORY_NAME):
    os.makedirs(JSON_DIRECTORY_NAME)


# generator for returning JSON filepaths
def get_json_files():
    for subdir, dirs, files in os.walk(os.path.join(JSON_DIRECTORY_NAME)):
        
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".json"):
                yield filepath


# converts JSON to XML
def save_json_file_to_xml():
    
    file_iterator = get_json_files()

    for file in file_iterator:

        with open(file) as f:
            data = json.load(f)
            xml = dicttoxml.dicttoxml(data)
            new_file_name = file.replace('json', 'xml').split('\\')[-1]
            
            with open(os.path.join(JSON_DIRECTORY_NAME, new_file_name) , "wb") as xml_file:
                xml_file.write(xml)

            print('Wrote new XML-File:', new_file_name)


# make http requests via cURL commands
def fetch_json_recipes():
    for recipe_range in range(0, HOW_MANY_RECIPES, 250):
        recipe_range_end = str(recipe_range + 250)
        recipe_range = str(recipe_range)
        os.system(f'curl "https://gw.hellofresh.com/api/recipes/search?offset={recipe_range}&limit=250&order=-date&locale=de-DE&country=de" -H "Host: gw.hellofresh.com" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0" -H "Accept: application/json, text/plain, */*" -H "Accept-Language: de,en-US;q=0.7,en;q=0.3" -H "Referer: https://www.hellofresh.de/recipes/search/?order=-date" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NTE5MDY5NjgsImp0aSI6ImVhYWM2NGNiLTQ5YjAtNDI3ZC05OGViLTVkZTIyYmFmODM0NiIsImlhdCI6MTU0OTI3NzIyNSwiaXNzIjoic2VuZiJ9.j8seLD0i8CMNooXQ_vjKx98PmQ8aZyllyujve1oQGW8" -H "Origin: https://www.hellofresh.de" -H "Connection: keep-alive" --output "./{JSON_DIRECTORY_NAME}/recipe_{recipe_range}-{recipe_range_end}.json"')
        print('_'*40)


fetch_json_recipes()

save_json_file_to_xml()
