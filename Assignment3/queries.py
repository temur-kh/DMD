from mysql.connector.connection import MySQLConnection
from datetime import datetime, timedelta
from random import randrange, randint
from sample_data.entity_classes import get_fake_date_time, getstr


def query1(conn: MySQLConnection):
    cursor = conn.cursor()

    def preload_data():
        # get one charging station to be used for nearest_station attribute of customers
        sql = "SELECT * FROM charging_stations LIMIT 1"
        cursor.execute(sql)
        station = cursor.fetchone()

        # insert a customer into table
        sql = "INSERT INTO customers (username, full_name, email, phone_number, " \
              "bank_account, gps_location, address, nearest_station) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        value = ("Liza", "Elizabeth", "elizabeth@gmail.com",
                 "123456789", "12341234", "gps-location", "address", station[0])
        cursor.execute(sql, value)
        conn.commit()
        customer_id = cursor.lastrowid

        # get 5 car plates to add rent records between the customer and cars
        sql = "SELECT * FROM cars LIMIT 5"
        cursor.execute(sql)
        rand_cplates = [car[0] for car in cursor.fetchall()]

        # create 5 rent records between the customer and chosen cars on a specific day
        date_time = datetime(2018, 11, 27, 0, 0, 0)
        for i in range(5):
            sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
                       "VALUES (%s, %s, %s, %s, %s)"
            date_from = get_fake_date_time(start=date_time, end=date_time + timedelta(hours=3))
            date_to = get_fake_date_time(start=date_from, end=date_time + timedelta(hours=3))
            value = (getstr(date_from), getstr(date_to), customer_id, rand_cplates[i], randint(1, 100))
            cursor.execute(sql, value)
            date_time = date_to
        conn.commit()

        # create a red car with using some car model and plate starting with 'AN'
        sql = "SELECT * FROM car_models LIMIT 1"
        cursor.execute(sql)
        model = cursor.fetchone()

        sql = "INSERT INTO cars (plate, cmodel, color) " \
              "VALUES(%s, %s, %s)"
        value = ("ANINAS", model[0], "red")
        cursor.execute(sql, value)
        conn.commit()
        cplate = cursor.lastrowid

        # create a rent record between the customer and this car
        sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
              "VALUES (%s, %s, %s, %s, %s)"
        date_from = get_fake_date_time(start=date_time, end=date_time + timedelta(hours=3))
        date_to = get_fake_date_time(start=date_from, end=date_time + timedelta(hours=3))
        value = (getstr(date_from), getstr(date_to), customer_id, cplate, randint(1, 100))
        cursor.execute(sql, value)
        conn.commit()

    preload_data()
    query = "SELECT * FROM rent_records AS r " \
            "INNER JOIN cars AS car ON r.cplate=car.plate " \
            "INNER JOIN customers AS c ON r.cid=c.id " \
            "WHERE c.full_name=%s AND DATE(r.date_from)=DATE(%s) " \
            "AND car.color=%s AND car.plate LIKE (%s+'%')"
    val = ("Elizabeth", datetime(2018, 11, 27), "red", "AN")
    cursor.execute(query, val)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query2(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime.datetime(2018, 5, 5, 0, 0, 0)

    def preload_data():
        # get five charging stations to be used for statistics
        sql = "SELECT * FROM charging_stations LIMIT 5"
        cursor.execute(sql)
        # get ids of five stations
        data = [station for station in cursor.fetchall()]
        rand_stations_id = [x[0] for x in data]
        no_of_socket = [x[3] for x in data]

        sql = "INSERT INTO charging_station_sockets (station_id, no_of_available_sockets, date_time) " \
              "VALUES (%s, %s, %s)"

        for i in range(len(rand_stations_id)):
            for j in range(randint(1, no_of_socket[i])):
                value = (rand_stations_id[i], randint(0, no_of_socket[j]), date + timedelta(hours=randint(0, 23)))
                cursor.execute(sql, value)
        conn.commit()
    preload_data()


def query3(conn: MySQLConnection):
    cursor = conn.cursor()

    def preload_data():
        return
    preload_data()
    sql = "SELECT * FROM rent_records " \
          "WHERE DATE(date_from) BETWEEN %s AND %s"
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
