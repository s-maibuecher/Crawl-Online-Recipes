#https://www.hellofresh.de/recipes/gesunde-gerichte-collection

import scrapy
from selenium import webdriver
import os
import time
import selenium.common.exceptions


HOMEPAGE = 'https://www.hellofresh.de'
RECIPE_DIRECTORY_NAME = 'recipes'

recipe_urls = []


if not os.path.exists(RECIPE_DIRECTORY_NAME):
    os.makedirs(RECIPE_DIRECTORY_NAME)

class RecipeSpider(scrapy.Spider):
    name = "recipe-spider"
    allowed_domains = ["hellofresh.de"]
    start_urls = ['https://www.hellofresh.de/recipes/search/?order=-favorites']#, 'https://www.hellofresh.de/recipes/gesunde-gerichte-collection', 'https://www.hellofresh.de/recipes/schnelle-gerichte-collection', 'https://www.hellofresh.de/recipes/thermomix-rezepte-collection', ]

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def parse(self, response):

        self.driver.get(response.url)

        recipe_category = response.url.split('/')[-1]

        recipe_category_directory = os.path.join(RECIPE_DIRECTORY_NAME,recipe_category )

        recipe_category_directory = recipe_category_directory.replace('?order=-favorites', 'favorites')

        if not os.path.exists(recipe_category_directory):
            os.makedirs(recipe_category_directory)

        times_button_clicked = 0
        times_no_button_found = 0
        default_sleep_time = 0.1

        # tried to display:none the recipe items, but did not fasten the crawling:
        javascript_to_execute = '''
        var styleelement = document.createElement('style');
        styleelement.innerHTML = '.fela-twgrf7 { display: none !important; }';
        document.getElementsByTagName('head')[0].appendChild(styleelement);
        '''
        #comment in to test:
        #self.driver.execute_script(javascript_to_execute)

        # Code which let Selenium click the Button till all content is loaded
        # but slows down extremely after about 150 clicks. Seems to be a backend/network issue 
        # workaraound with http calls see get_recipes_via_http_calls_workaround.py

        while True:
            try:
                time.sleep(default_sleep_time)
                next = self.driver.find_element_by_xpath('//button')
                next.click()
                times_button_clicked += 1

                # I have implemented a break condition here, because this algorithm is too low in performance at this specific target page because of network issues. 
                if times_button_clicked == 50:
                    break

            except selenium.common.exceptions.ElementClickInterceptedException as e:
                    # Remove Newsletter Modal
                    print('Remove Newsletter Modal')
                    time.sleep(1)
                    modal_close_button = self.driver.find_element_by_xpath('//div[@class="dy-lb-close"]')
                    modal_close_button.click()
                    time.sleep(1)

            except selenium.common.exceptions.NoSuchElementException as e:
                time.sleep(5)
                print('!'*25, 'FOUND NO BUTTON MORE')
                times_no_button_found += 1
                default_sleep_time *= 2

                if times_no_button_found > 3:
                    print('Found no Mehr Anzeigen button for 15 seconds. Break.')
                    break

            except Exception as e:
                raise

            finally:
                print(f'Button was {times_button_clicked} times clicked.')

        print('Link page seems to be loaded.')
        image_links = response.xpath('//img/ancestor::a/@href').extract()
        image_links_sel = self.driver.find_elements_by_xpath('//img/ancestor::a') #returns a list

        relative_links_to_urls = []
        for l in image_links_sel:
            
            temp = l.get_attribute('href')

            if self.validate_recipe_URL(temp):          
                temp = temp.replace('?locale=de-DE', '').split('/')[-1]
                relative_links_to_urls.append(temp)

        for index, u in enumerate(relative_links_to_urls):
            time.sleep(0.2)
            yield response.follow(u, callback=self.saveRecipePage, meta={'recipe_category_directory' : recipe_category_directory, 'index' : index})

        self.driver.quit()

    def saveRecipePage(self, response):
        print('UNTERSEITE:', response.url)

        file_name = response.url.replace('?locale=de-DE', '').replace('?order=-favorites', 'favorites').split('/')[-1] + 'index' + str(response.meta['index'])

        with open(os.path.join( response.meta['recipe_category_directory'] , file_name +'.html'), 'wb') as file:
           file.write(response.body)


    def validate_recipe_URL(self, url):
        subdomain = 'hellofresh.de/recipes/'
        return subdomain in url
    

''' To-Do:
https://stackoverflow.com/questions/6682503/click-a-button-in-scrapy

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling

'''
