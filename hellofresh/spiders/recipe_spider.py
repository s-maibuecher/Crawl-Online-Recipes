#https://www.hellofresh.de/recipes/gesunde-gerichte-collection

import scrapy
from selenium import webdriver


HOMEPAGE = 'https://www.hellofresh.de'
RECIPE_DIRECTORY = './recipes/'

recipe_urls = []

class RecipeSpider(scrapy.Spider):
    name = "recipe-spider"
    allowed_domains = ["hellofresh.de"]
    start_urls = ['https://www.hellofresh.de/recipes/gesunde-gerichte-collection']

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def parse(self, response):

        if response.meta["depth"] == 0:

            #self.driver.get('https://www.example.org/abc')

            image_links = response.xpath('//img/ancestor::a/@href').extract()

            for i in image_links:
                if validate_recipe_URL(i):
                    yield response.follow(i)

        else:
            print('UNTERSEITE:', response.url)

            file_name = response.url.replace('?locale=de-DE', '').split('/')[-1]

            with open(RECIPE_DIRECTORY + file_name +'.html', 'wb') as file:
               file.write(response.body)


def validate_recipe_URL(url):
    
    return url.startswith('/recipes')
    

''' To-Do:
https://stackoverflow.com/questions/6682503/click-a-button-in-scrapy

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling

'''
