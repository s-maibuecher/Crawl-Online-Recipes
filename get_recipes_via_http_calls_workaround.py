''' # To-Do: Get recipes via cURL, because scrapy + selenium slows down after about 150 button clicks
'''
import os

JSON_DIRECTORY_NAME = 'http_requested_json_recipes'

if not os.path.exists(JSON_DIRECTORY_NAME):
    os.makedirs(JSON_DIRECTORY_NAME)

# To-Do: loop JSON Requests, till all recipes are fetched:

#os.system('curl "https://gw.hellofresh.com/api/recipes/search?offset=1750&limit=250&order=-date&locale=de-DE&country=de" -H "Host: gw.hellofresh.com" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0" -H "Accept: application/json, text/plain, */*" -H "Accept-Language: de,en-US;q=0.7,en;q=0.3" -H "Referer: https://www.hellofresh.de/recipes/search/?order=-date" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NTE5MDY5NjgsImp0aSI6ImVhYWM2NGNiLTQ5YjAtNDI3ZC05OGViLTVkZTIyYmFmODM0NiIsImlhdCI6MTU0OTI3NzIyNSwiaXNzIjoic2VuZiJ9.j8seLD0i8CMNooXQ_vjKx98PmQ8aZyllyujve1oQGW8" -H "Origin: https://www.hellofresh.de" -H "Connection: keep-alive" --output "recipe_1750-2000.json"')
