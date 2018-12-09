import requests
import json

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/movies/api/v1.0', methods=['GET'])
def get_token():
    url = 'https://api.thetvdb.com/login'

    post_fields = {"apikey": "BMQP6TTS0FJXZHXQ"}

    r = requests.post(url, json=post_fields)

    data = r.json()

    print(data["token"])


    return r.content

def getToken():
    url = 'https://api.thetvdb.com/login'
    # post_fields = {"apikey":"HDOCBES5IGL47V4B","username":"zarmion5ry", "userkey": "0QLEERFW5DYUCHBW"}
    post_fields = {"apikey": "BMQP6TTS0FJXZHXQ"}

    r = requests.post(url, json=post_fields)

    data = r.json()

    return data["token"]


def getMoviePicture(id):
    url = "https://api.thetvdb.com/series/" + str(id) + "/images/query?keyType=poster"
    headers = {"Authorization": "Bearer " + getToken()}

    r = requests.get(url, headers=headers)

    data = r.json()

    if 'data' in data and 'thumbnail' in data['data']:
        return "https://www.thetvdb.com/banners/" + data["data"][0]['thumbnail']

    return ""


@app.route('/movies/api/v1.0/search/<string:serieName>', methods=['GET'])
def get_movie(serieName):
    url = 'https://api.thetvdb.com/search/series?name=' + serieName
    jsonAnswer = {}

    headers = {"Authorization": "Bearer " + getToken()}

    if 'Accept-Language' in request.headers:
        headers['Accept-Language'] = request.headers['Accept-Language']

    r = requests.get(url, headers=headers)

    data = r.json()

    idSerie = data["data"][0]["id"]

    jsonAnswer["idSerie"] = idSerie
    jsonAnswer["name"] = data["data"][0]["seriesName"]
    jsonAnswer["thumbnail"] = getMoviePicture(idSerie)
    jsonAnswer["synopsis"] = data["data"][0]["overview"]

    return jsonify(jsonAnswer)


if __name__ == '__main__':
    app.run()
