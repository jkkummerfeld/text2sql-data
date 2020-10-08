from typing import List
import sqlite3

def get_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    return conn

def insert_into(cursor: sqlite3.Cursor,
                table: str,
                columns: List[str],
                values: List[str]) -> None:

    sql = f"INSERT INTO {table}({','.join(columns)}) VALUES({','.join(['?' for _ in values])})"
    cursor.execute(sql, values)

create_geographic = """ CREATE TABLE IF NOT EXISTS GEOGRAPHIC (
                               CITY_NAME varchar(255) PRIMARY KEY,
                               COUNTY varchar(255),
                               REGION varchar(255)
                               ); """

create_restaurants = """ CREATE TABLE IF NOT EXISTS
                                RESTAURANT ( RESTAURANT_ID int(11) PRIMARY KEY,
                                NAME varchar(255),
                                FOOD_TYPE varchar(255),
                                CITY_NAME varchar(255),
                                RATING decimal(1,1),
                                FOREIGN KEY (CITY_NAME) REFERENCES GEOGRAPHIC(CITY_NAME)
                                );"""

create_location = """ CREATE TABLE IF NOT EXISTS LOCATION (
                             RESTAURANT_ID int(11) PRIMARY KEY,
                             HOUSE_NUMBER int(11),
                             STREET_NAME varchar(255),
                             CITY_NAME varchar(255),
                             FOREIGN KEY (RESTAURANT_ID) REFERENCES GEOGRAPHIC(RESTAURANT_ID)
                             ); """

def main(input_path: str, output_path: str = "./restuarants.db"):
    restaurant_data = {"RESTAURANT": [], "LOCATION": [], "GEOGRAPHIC": []}
    column_count = {"RESTAURANT": 5, "LOCATION": 4, "GEOGRAPHIC": 3}

    with open(input_path, "r") as infile:

        for line in infile:
            line = line.strip()
            split_at = line.find("(")
            table_name = line[:split_at]
            table = line[split_at + 1:]
            table = table.strip(")").split(",")
            if len(table) > column_count[table_name]:
                # Manually fix some problems from spliting on commas.
                if table_name == "RESTAURANT":
                    table_id = table[0]
                    rating = table[-1]
                    location = table[-2]
                    food_type = table[-3]
                    name = ",".join(table[1:-3])
                    table = [table_id, name, food_type, location, rating]
                elif table_name == "LOCATION":
                    street_name = ",".join(table[2:-1])
                    table = [table[0], table[1], street_name, table[-1]]
                else:
                    print(table)
                    raise ValueError("Table read from file didn't match schema.")

            # Clean up some trailing spaces and quotation marks in the columns.
            table = [x.strip('" ').strip("'") for x in table]
            restaurant_data[table_name].append(table)


    connection = get_connection(output_path)

    cursor = connection.cursor()
    print(f"Creating database at {output_path}")
    cursor.execute(create_geographic)
    cursor.execute(create_restaurants)
    cursor.execute(create_location)

    # Put the values into the tables
    for value in restaurant_data["RESTAURANT"]:
        insert_into(cursor, "RESTAURANT", ["RESTAURANT_ID", "NAME", "FOOD_TYPE", "CITY_NAME", "RATING"], value)

    for value in restaurant_data["LOCATION"]:
        insert_into(cursor, "LOCATION", ["RESTAURANT_ID", "HOUSE_NUMBER", "STREET_NAME", "CITY_NAME" ], value)

    for value in restaurant_data["GEOGRAPHIC"]:
        insert_into(cursor, "GEOGRAPHIC", ["CITY_NAME", "COUNTY", "REGION"], value)

    connection.commit()

    # Superficial test that we can run queries.
    sql = "SELECT RESTAURANT.NAME FROM RESTAURANT WHERE RESTAURANT.RESTAURANT_ID = 234"
    print(f"Running query as a test: {sql}")
    cursor.execute(sql)
    results = cursor.fetchall()
    print("Result: ", results)
    connection.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) not in [2, 3]:
        print("Usage: python create_restaurant_database.py <path to restaurants-db.txt> <output path (optional, default = ./restuarants.db)>")
    else:
        main(*sys.argv[1:])
