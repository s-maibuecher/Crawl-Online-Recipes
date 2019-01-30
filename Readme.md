# UNDER CONSTRUCTION

Scrapy and Selenium based Web Crawler to crawl thousands of Food Receipes for a nice DataScience Dataset.

`scrapy crawl recipe-spider`

Go to subdirectory ./recipes to see crawled recipes.

## Milestones

* Crawl all recipes which are displayed.
* __Problem:__ There is a 'Mehr Ansehen' (See more.) Button after some few recipes, which have to be clicked to enrich more content to the site
* _Solution:_ Bind in Selenium which continuous clicks this button
	* ![Button](./docs/button.jpg)


### To-Do:
- [x] build initial spider to crawl some recipes
- [x] saving scraped recipes
- [x] simulate click html button 'Mehr Ansehen...' to see more sources
- [ ] for production: click button till all content is visible
- [ ] for production: add more subpages to crawl

### Troubleshooting
[Maybe you have to install geckodriver](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path)
