import requests
import json
from pprint import pprint
username = "tiangolo"
url = f"https://api.github.com/users/{username}/repos"
response = requests.get(url)
#pprint(response.json())
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f)

