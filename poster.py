from json import dumps as jsonify

import requests as req


def post():
    reqdata = {"lat": 17.783966,
               "long": 83.382980,
               "address": "Rushikonda",
               "state": "Andhra Pradesh",
               "pin": 530045
               }
    res = req.post("http://localhost:5000/post_location", json=jsonify(reqdata))
    print(res.text)


def get():
    reqdata = {"lat": 28.55,
               "long": 77.2667
               }
    res = req.post("http://localhost:5000/get_place", json=jsonify(reqdata))
    print(res.text)


get()
