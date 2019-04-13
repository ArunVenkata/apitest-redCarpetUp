import json
import unittest as tester
from json import dumps as jsonify

import requests as req

post_url = "http://localhost:5000/post_location"


class TestPostLoc(tester.TestCase):

    def test_if_posted(self):
        # Can be run only once as data is added after running once
        # which makes it fail next time
        reqdata = {"lat": 17.726675,
                   "long": 83.312320,
                   "address": "CBM Compound",
                   "state": "Andhra Pradesh",
                   "pin": 530003
                   }
        res = req.post(post_url, json=jsonify(reqdata))
        self.assertEqual(json.loads(res.text)["Status"], "200")

    def test_bad_request(self):
        req_data = {}
        res = req.post(post_url, json=req_data)
        self.assertEqual(json.loads(res.text)["Status"], "400")


if __name__ == '__main__':
    tester.main()
