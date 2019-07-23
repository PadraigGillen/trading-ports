import requests

base_url = "http://localhost:5000"

def put(url, data):
    return requests.put(base_url + url, data).text
