import requests

querystring = {
    "location":"33, -84",
    "fields":["temperature", "cloudCover"],
     "units":"imperial",
     "timesteps":"1d",
     "apikey":"a6kMpxFiGtKckBzdaCrdHULSIPRlgQwO"}

response = requests.request("GET", url, params=querystring)
print(response.text)