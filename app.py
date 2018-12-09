import requests
import json

from flask import Flask, jsonify, request
from cachetools import cached, TTLCache

app = Flask(__name__)

# let's cache the token for one day (the expiration time for the API)
tokenCached = TTLCache(maxsize=1, ttl=86300)


# function to get the token from the API key for the tvdb API
@cached(tokenCached)
def getToken():
    url = 'https://api.thetvdb.com/login'

    with open('data.json') as json_data:
        data_dict = json.load(json_data)
        api_key = data_dict['apikey']

    post_body = {"apikey": api_key}

    r = requests.post(url, json=post_body)

    data = r.json()

    return data["token"]


# function to get the thumbnail if it exist
def getThumbnail(id):
    # the url to get the picture of a serie from the API
    url = "https://api.thetvdb.com/series/" + str(id) + "/images/query?keyType=poster"

    # puting the token to the header
    headers = {"Authorization": "Bearer " + getToken()}

    # request the pictures
    data = requests.get(url, headers=headers).json()

    if 'data' in data:
        # should use a while loop, it's cleaner. browsing the answer looking for a thumbnail if there is an answer
        for picture in data["data"]:
            if 'thumbnail' in picture:
                return "https://www.thetvdb.com/banners/" + data["data"][0]['thumbnail']

    return ""


# function to get the actors of a serie
def getActors(id):

    actors = []
    # the url to get the actors of a series from the API
    url = "https://api.thetvdb.com/series/" + str(id) + "/actors"

    # puting the token to the header
    headers = {"Authorization": "Bearer " + getToken()}

    # request the actors list
    data = requests.get(url, headers=headers).json()

    if 'data' in data:
        # should use a while loop, it's cleaner. browsing the answer looking for a thumbnail if there is an answer
        for actor in data["data"]:
            if actor["sortOrder"] == 1:
                actors.append({
                    "name": actor["name"],
                    "role": actor["role"]
                })

    return actors


# route to research a serie, return a json containing a list
@app.route('/series/api/v1.0/search/<string:serieName>', methods=['GET'])
def getSerieList(serieName):
    url = 'https://api.thetvdb.com/search/series?name=' + serieName

    series = []

    headers = {"Authorization": "Bearer " + getToken()}

    if 'Accept-Language' in request.headers:
        headers['Accept-Language'] = request.headers['Accept-Language']

    data = requests.get(url, headers=headers).json()

    if 'data' in data:
        for serie in data["data"]:
            series.append(getSerie(serie["id"]))

    return json.dumps(series, ensure_ascii=False).encode('utf8')

@app.route('/series/api/v1.0/<int:id>', methods=['GET'])
def getSerieById(id):

    return json.dumps(getSerie(id), ensure_ascii=False).encode('utf8')

def getSerie(id):

    url = 'https://api.thetvdb.com/series/' + str(id)
    headers = {"Authorization": "Bearer " + getToken()}

    if 'Accept-Language' in request.headers:
        headers['Accept-Language'] = request.headers['Accept-Language']

    data = requests.get(url, headers=headers).json()

    if 'data' in data:
        return fetchSerie(data["data"])

    return data

# getting the relevant data from the api
def fetchSerie(entry):
    serie = {}
    # if they exist we fetch the values
    if 'seriesName' in entry:
        serie["name"] = entry["seriesName"]
    if 'overview' in entry:
        serie["synopsis"] = entry["overview"]
    if 'banner' in entry:
        serie["thumbnail"] = getThumbnail(entry["id"])
    if 'imdbId' in entry:
        serie["imbId"] = entry["imdbId"]
    if 'id' in entry:
        serie["id"] = entry["id"]

    serie["actors"] = getActors(entry["id"])

    return serie


##################################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, threaded=True)
