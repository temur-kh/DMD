from mysql.connector.connection import MySQLConnection
import datetime
from random import randrange


def query1(conn: MySQLConnection):
    cursor = conn.cursor()

    def preload_data():
        sql = "INSERT INTO customers (username, full_name, email, phone_number, " \
              "bank_account, gps_location, address, nearest_station) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        station_sql = "SELECT * FROM charging_stations LIMIT 1"
        cursor.execute(station_sql)
        station = cursor.fetchone()
        value = ("Liza", "Elizabeth", "elizabeth@gmail.com",
                 "123456789", "12341234", "gps-location", "address", station[0])
        cursor.execute(sql, value)
        sql = "INSERT INTO cars (plate, cmodel, color) " \
              "VALUES(%s, %s, %s)"
        model_sql = "SELECT * FROM car_models LIMIT 1"
        cursor.execute(model_sql)
        model = cursor.fetchone()
        value = ("ANINAS", model[0], "red")
        cursor.execute(sql, value)
        conn.commit()
    preload_data()
    query = "SELECT * FROM cars WHERE color = %s AND SUBSTRING(plate,1,2) = %s"
    val = ("red", "AN")
    cursor.execute(query, val)


def query2(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime.datetime(2018, 5, 5)

    def preload_data():
        for i in range(50):
            rndm_date = random_date(date, date + 1)
            sql = "INSERT INTO charge_records (date_time, cplate, price) VALUES (%s, %s, %s)"
            cplate_sql = "SELECT plate FROM cars LIMIT 1"
            cursor.execute(cplate_sql)
            cplate = cursor.fetchone()
            value = (rndm_date, cplate, 1234)
            cursor.execute(sql, value)
    preload_data()
    query = "SELECT date_time FROM charge_records WHERE date_time BETWEEN %s AND %s"
    value = (date, date + 1)
    cursor.execute(query, value)
    row = cursor.fetchone()
    result = [24]
    for x in row:
        result[x.hour] += 1


def query3(conn:MySQLConnection):
    cursor = conn.cursor()

    def preload_data():
        return
    preload_data()
    sql = "SELECT * FROM rent_records " \
          "WHERE DATE(date_from) BETWEEN %s AND %s AND HOUR(date_from)"
    d1 = datetime.datetime(2018, 5, 7)
    d2 = datetime.datetime(2018, 5, 14)
    value = (d1, d2)
    cursor.execute(sql, value)
    selected = cursor.fetchone()
    sql = "SELECT * FROM selected "

def query4(conn: MySQLConnection):
    cursor = conn.cursor()

    def preload_data():
        deposit_sql = "SELECT id FROM deposits LIMIT 1"
        cursor.execute(deposit_sql)
        deposit = cursor.fetchone()
        customer_sql = "SELECT id FROM customers WHERE full_name = %s"
        cursor.execute(customer_sql, "Elizabeth")
        customer = cursor.fetchone()
        for i in range(30):
            sql = "INSERT INTO payment_records (no_of_transaction, date_time, cid, did, price) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            d1 = datetime.datetime(2018, 5, 5)
            d2 = datetime.datetime(2018, 5, 25)
            date = random_date(d1, d2)
            value = (i, date, customer[0], deposit[0], 1234)
            cursor.execute(sql, value)

            sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            cplate_sql = "SELECT plate FROM cars LIMIT 1"
            cursor.execute(cplate_sql)
            cplate = cursor.fetchone()
            value = (date, random_date(date, d2), customer[0], cplate[0], 1234)
            cursor.execute(sql, value)
            conn.commit()
    preload_data()

    customer_sql = "SELECT id FROM customers WHERE full_name = %s"
    cursor.execute(customer_sql, "Elizabeth")
    customer = cursor.fetchone()
    query = "SELECT * FROM payment_records WHERE cid = %s"
    cursor.execute(query, customer[0])


def query5(conn:MySQLConnection):
    cursor = conn.cursor()


def query5():
    return


def get_all_query_results():
    return []


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)
