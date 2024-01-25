"""
Usage: python3 tools/spider_schema_to_sqlite.py
Input: Reads data/spider-schema.csv
Output: Creates databases/*.sqllite files.
Author: prasad
"""
import os
import csv
import sqlite3

with open("data/spider-schema.csv") as f:
    databases = {}

    csvfile = csv.reader(f, skipinitialspace=True)
    header = None
    for line in csvfile:
        if header is None:
            header = line
            continue
        row = dict(zip(header, line))
        
        db = row["Database name"].lower()
        table = row["Table Name"].lower()
        column = row["Field Name"].lower()
        column_type = row["Type"]
        column_primray = row["Is Primary Key"]
        if db not in databases:
            databases[db] = {"tables": {}}
        if table not in databases[db]["tables"]:
            databases[db]["tables"][table] = {"columns": {}, "primary": []}
        if column not in databases[db]["tables"][table]["columns"]:
            databases[db]["tables"][table]["columns"][column] = { "name": column, "type": column_type }
            if column_primray == "True":
                databases[db]["tables"][table]["primary"].append(column)

    for db in databases:
        os.makedirs("databases/" + db)
        dbconn = sqlite3.connect("databases/" + db + "/" + db + ".sqlite")
        dbcur = dbconn.cursor()

        for table in databases[db]["tables"]:
            if "sqlite_sequence" == table:
                continue
            tablesql = "CREATE TABLE " + table + "("
            coldelim = " "
            for col in databases[db]["tables"][table]["columns"]:
                col = databases[db]["tables"][table]["columns"][col]
                tablesql += coldelim + '"' + col["name"] + '" ' + col["type"]
                coldelim = ","
            if len(databases[db]["tables"][table]["primary"]):
                tablesql += ",PRIMARY KEY ("+ ",".join(databases[db]["tables"][table]["primary"]) +")"
            tablesql += ");"
            print (tablesql)
            dbcur.execute(tablesql)
        dbconn.commit()
        
    f.close()
    print("\nYou can now use databases/*.sqlite files\n")
