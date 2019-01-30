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
    start_urls = ['https://www.hellofresh.de/recipes/gesunde-gerichte-collection'] # LATER: , 'https://www.hellofresh.de/recipes/schnelle-gerichte-collection'] AND SO ON...

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def parse(self, response):

        self.driver.get(response.url)

        for i in range(1):
            next = self.driver.find_element_by_xpath('//button')
            next.click()
            #print('Button gedrückt.')

        image_links = response.xpath('//img/ancestor::a/@href').extract()
        image_links_sel = self.driver.find_elements_by_xpath('//img/ancestor::a') #returns a list

        relative_links_to_urls = []
        for l in image_links_sel:
            
            temp = l.get_attribute('href')

            if self.validate_recipe_URL(temp):          
                temp = temp.replace('?locale=de-DE', '').split('/')[-1]
                relative_links_to_urls.append(temp)

        for u in relative_links_to_urls:
            yield response.follow(u, callback=self.saveRecipePage)


    def saveRecipePage(self, response):
        print('UNTERSEITE:', response.url)

        file_name = response.url.replace('?locale=de-DE', '').split('/')[-1]

        with open('./' + RECIPE_DIRECTORY_NAME + '/' + file_name +'.html', 'wb') as file:
           file.write(response.body)


    def validate_recipe_URL(self, url):
        subdomain = 'hellofresh.de/recipes/'
        return subdomain in url
    

''' To-Do:
https://stackoverflow.com/questions/6682503/click-a-button-in-scrapy

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling

'''
