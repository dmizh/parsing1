import requests
from pprint import pprint
import random
key = "v1BV9CO95lKqpiyv"
url = f"http://api.isportsapi.com/sport/football/league?api_key={key}"
response = requests.get(url)
list_lig = []
for item in response.json()['data']:
    list_lig.append(item['leagueId'])
random_id = list_lig[random.randint(0,len(list_lig))]
params = {"leagueId": random_id}
response = requests.get(url, params=params)
gdata = response.json()
print(f"Country - {gdata['data'][0]['country']}.\nLeague - {gdata['data'][0]['name']}.\nLogo - {gdata['data'][0]['logo']}")
