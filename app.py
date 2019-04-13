import ast
import json

import psycopg2 as sql
from flask import Flask, jsonify, request
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from earthdist import earth_distance

app = Flask(__name__)
conn = sql.connect(host="localhost", database="in-data",
                   user="postgres", password="root", port="5555")

c = conn.cursor()

bad_req = {"Status": "400", "Msg": "Check request data Properly!"}
frbd_req = {"Status": "403", "Msg": "Forbidden"}


@app.route('/post_location', methods=["POST"])
def post_loc():
    if request.json:

        req_data = json.loads(request.json)

        # get all latitudes and longitudes
        c.execute("SELECT latitude,longitude from indata WHERE latitude!='' or longitude!='';")
        ll = list(set(c.fetchall()))
        close_locs = []

        # check if given ones are close enough to any
        for lat1, long1 in ll:

            dist = earth_distance(float(lat1), float(long1), float(req_data["lat"]), float(req_data["long"]))

            # Assumption - If distance is less than 500 meters
            # If close, Get location of close vals
            if dist <= 0.5:
                c.execute("select place_name,admin_name1 from indata where latitude=%s and longitude=%s",
                          (lat1, long1,))
                close_locs = c.fetchall()

        c.execute("SELECT ID,key FROM indata ORDER BY ID DESC LIMIT 2")
        res = c.fetchall()

        # get next Id
        next_num = int(res[0][0]) + 1

        # get next key
        next_key = "IN/" + str(req_data["pin"])

        # if the same pin code exists then dont allow to add
        if next_key == res[0][1]:
            return jsonify(frbd_req)

        # Add to db
        c.execute("INSERT INTO indata VALUES(%s, %s, %s, %s, %s, %s, %s)",
                  (next_num, next_key, req_data["address"], req_data["state"],
                   req_data["lat"], req_data["long"], ""))

        conn.commit()

        return jsonify({"Status": "200",
                        "Locations": close_locs}) if close_locs else jsonify({"Status": "200"})

    else:
        return jsonify(bad_req)


def getlocs(lat, lon, by_self=False):
    c.execute("SELECT key, latitude,longitude from indata;")
    rows = c.fetchall()
    li = []
    if by_self:
        # One Liner for the whole process
        li = [x[0] for x in rows if
              x[1] != "" and x[2] != "" and earth_distance(lat, lon, float(x[1]), float(x[2])) <= 5]

    else:
        c.execute("CREATE EXTENSION IF NOT EXISTS cube CASCADE;")
        c.execute("CREATE EXTENSION  IF NOT EXISTS earthdistance CASCADE;")

        print("ROWS", rows)
        for x in rows:
            # get Distance for each point
            if x[1] == "" or x[2] == "":
                continue

            c.execute("""SELECT (point({0},{1}) <@> point({2}, {3}))""".format(
                lat, lon, x[1], x[2]))

            res = c.fetchall()[0][0]
            print("RES", res)
            if float(res) <= 5:
                li.append(x[0])
    return li


@app.route("/get_using_postgres", methods=["POST", "GET"])
def get_using_postgres():
    if request.method == "POST":
        if request.json:
            req_data = json.loads(request.json)
            try:
                # check if "lat" exists
                print(req_data["lat"])

                # check if "long" exists
                print(req_data["long"])

            except KeyError:
                return jsonify(bad_req)

            else:
                return jsonify({"Status": "200", "Nearby Locations": getlocs(req_data["lat"], req_data["long"])})

        else:
            return jsonify(bad_req)
    else:
        # define params on server
        lat = 28.55
        lon = 77.2667

        return jsonify({"Status": "200", "Nearby Locations": getlocs(lat, lon)})


@app.route("/get_using_self", methods=["POST", "GET"])
def get_using_self():
    if request.method == "POST":
        if request.json:
            req_data = json.loads(request.json)
            try:
                # check if "lat" exists
                print(req_data["lat"])

                # check if "long" exists
                print(req_data["long"])

            except KeyError:
                return jsonify(bad_req)

            else:
                return jsonify(
                    {"Status": "200", "Nearby Locations": getlocs(req_data["lat"], req_data["long"], by_self=True)})

        else:
            return jsonify(bad_req)
    else:
        # define params on server
        lat = 28.55
        lon = 77.2667

        return jsonify({"Status": "200", "Nearby Locations": getlocs(lat, lon, by_self=True)})


@app.route("/get_place", methods=["POST"])
def get_place():
    if request.json:
        req_data = json.loads(request.json)
        try:
            # check if "lat" exists
            print(req_data["lat"])

            # check if "long" exists
            print(req_data["long"])

        except KeyError:
            return jsonify(bad_req)

        c.execute("SELECT * FROM geojson;")
        rows = c.fetchall()
        res = {}
        for row in rows:
            li = ast.literal_eval(row[4])
            point = Point(float(req_data["lat"]), float(req_data["long"]))
            polygon = Polygon(li)
            if polygon.contains(point):
                res["parent"] = row[3]
                res["name"] = row[1]
                return jsonify(res)
        return jsonify({"Status": "404", "Msg": "Not Found"})
    else:
        return jsonify(bad_req)


@app.route('/<path:dummy>')
def fallback(dummy):
    return jsonify({"Error 404": dummy + " is an INVALID URL"})


if __name__ == '__main__':
    app.run()
