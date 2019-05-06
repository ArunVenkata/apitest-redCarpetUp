import psycopg2 as sql

conn = sql.connect(host="localhost", database="test_db",
                   user="arun", password="root", port="5432")

c = conn.cursor()

with open("in-data.csv", "r") as csvfile:
    li = [entry.split(",") for entry in csvfile.read().split("\n")]
    # c.execute("DROP TABLE indata;")
    # crt_part_query = " TEXT, ".join(li[0]).upper()
    # c.execute("CREATE TABLE indata(ID INTEGER PRIMARY KEY, {0} TEXT)".format(crt_part_query))
    # print(li[1:10])
    # conn.commit()

    # Load Data
    ins_part_query = ",".join(li[0]).upper()
    for x in range(1, len(li[:-1])):
        val_str = "'" + "', '".join(li[:-1][x]) + "'"
        ins_query = "INSERT INTO indata VALUES(" + str(x) + ", {0});".format(val_str)
        try:
            c.execute(ins_query)
            print("Loaded", val_str)
            conn.commit()
        except sql.DatabaseError as e:
            print("ERROR", ins_query)
            c.execute("ROLLBACK")
            conn.commit()
            print(e)

# close DB
conn.commit()
conn.close()
