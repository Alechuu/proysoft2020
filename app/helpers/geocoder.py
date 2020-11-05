import requests

def geocoder(direccion):
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = 's0gvC3NKNulSUn6DSTyhf4jCcwVL5TN7C5oBELvwf3I' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'q':direccion} 
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']

    return [latitude,longitude]