#https://www.hellofresh.de/recipes/gesunde-gerichte-collection

import scrapy
from selenium import webdriver
import os


HOMEPAGE = 'https://www.hellofresh.de'
RECIPE_DIRECTORY_NAME = 'recipes'

recipe_urls = []


directory = 'cover'
if not os.path.exists(RECIPE_DIRECTORY_NAME):
    os.makedirs(RECIPE_DIRECTORY_NAME)

class RecipeSpider(scrapy.Spider):
    name = "recipe-spider"
    allowed_domains = ["hellofresh.de"]
    start_urls = ['https://www.hellofresh.de/recipes/gesunde-gerichte-collection']

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self):
        #self.driver = webdriver.Firefox()
    
    def parse(self, response):

        #self.driver.get('https://www.example.org/abc')

        image_links = response.xpath('//img/ancestor::a/@href').extract()

        for i in image_links:
            if self.validate_recipe_URL(i):
                yield response.follow(i, callback=self.saveRecipePage)


    def saveRecipePage(self, response):
        print('UNTERSEITE:', response.url)

        file_name = response.url.replace('?locale=de-DE', '').split('/')[-1]

        with open('./' + RECIPE_DIRECTORY_NAME + '/' + file_name +'.html', 'wb') as file:
           file.write(response.body)


    def validate_recipe_URL(self, url):
        
        return url.startswith('/recipes')
    

''' To-Do:
https://stackoverflow.com/questions/6682503/click-a-button-in-scrapy

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling

'''
