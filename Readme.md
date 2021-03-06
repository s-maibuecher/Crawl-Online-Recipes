# Build up a Food Recipes Dataset with web-crawled HTML recipes :fork_and_knife: :stew: :pizza:

**tl;dr** study final dataset here: `/CSV/final_dataframe.csv`

# Data Science is OSEMN
Data Science projects are subdivided into five steps: (1) obtaining data, (2) scrubbing data, (3) exploring data, (4) modeling data, and (5) interpreting data.  
This project covers steps (1) and (2) and is building up a dataset from web-crawled HTML recipes.  
Steps (3)-(5) are covered in my next project.


## Summary

Scrapy and Selenium based Web Crawler to crawl thousands of Food Receipes for a nice DataScience Dataset.

`scrapy crawl recipe-spider`

Go to subdirectory ./recipes to see crawled recipes.

## Milestones

* Crawl all recipes which are displayed.
* __Problem:__ There is a 'Mehr Anzeigen' (Show more) Button after some few recipes, which have to be clicked to enrich more content to the site
	* _Solution:_ Bind in Selenium which continuous clicks this button
	![Button](./docs/button.jpg)
* __Problem:__ Every recipe contains an info box about the nutrition facts (Nähwertangaben). You can choose to see the nutrition facts of one portion or of 100 grams of this meal. Default selection is the former selection. I guess it to get a cleaner dataset it is better to crawl the data normalized by the 100gr amount. Problem here is, that the data of the 100 grams selection is not included in the html source code, so do I have to run selenium at every recipe page to simulate a click at this form? Damn.
	* _Solution:_ No. I found out, that there no network traffic recorded when you click that button. So the calculation has to be done locally. There is a fiels called "servingSize" in the source code, which can be used to calculate the ratio between both fields. + Further benefit: there is even more hidden date in the source, which is not shown at the website: e.g. ratingsCount, favoritesCount, ...

![Nutrition Facts](./docs/nutrition_facts.jpg)

* __Problem:__ Selenium gets very slow / crashes after about 150 times of clicking the Show More button. Need a more resource-friendly way to crawl. First tried to delete items at the top of the page which were already crawled, but the React Backend resends them to the browser. Then I tried to set display:hide to these elements to fasten the page loading. But does not work, seems to be a network issue.
	* _Solution:_ Studied HTTP traffic. Found a way to get all recipes by plain HTTP calls. See _get_recipes_via_http_calls_workaround.py_

* Henceforward I use the _get_recipes_via_http_calls_workaround.py_ script to fetch all recipes. It returns XML files into the _http_requested_json_recipes_ directory

`python get_recipes_via_http_calls_workaround.py`

* __Problem:__ Sadly there were some encoding problems within the recipe data. See screenshot.
![Encoding Problems](./docs/encoding-problems.jpg)
	* _Solution:_ I had to use a mass search and replace tool to replace these characters. About 5min work.

`python build_dataframe.py` now builds a CSV dataset out of all recipes. You can find it in the _CSV_ subdirectory.
![CSV Dataset](./docs/csv_dataset.jpg)

* __Problem:__ Some important fields like ingredients contain huge objects which are not ready for DataScience processing.
![Objects for feature engineering](./docs/objects-for-feature-engineering.jpg)	
	* _Solution:_ First: Saved these objects into xml structure, because I like to use XPATH, when I inspect bigger objects.

* save the final dataframe with `python scrubbing_data.py`

* :raised_hands: Study final data at `CSV/final_dataframe.csv` :raised_hands:

:clap::clap::clap:

### ~~To-Do~~:
- [x] build initial spider to crawl some recipes
- [x] saving scraped recipes
- [x] simulate click html button 'Mehr Anzeigen' to see more sources
- [x] for production: click button till all content is visible
- [x] for production: add more subpages to crawl
- [x] study HTTP Requests/Responses
- [x] send HTTP requests via python
- [x] look for hidden data in the sourcecode, like "ratingsCount", "favoritesCount", ...
- [x] scrubbing data 
- [x] save as CSV dataset

### Troubleshooting
* [Maybe you have to install geckodriver](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path)
* [Maybe you have to install cURL and add it to your Path](https://curl.haxx.se/)