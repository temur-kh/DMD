from mysql.connector.connection import MySQLConnection
from datetime import datetime, timedelta, time
from random import randint, choice
from pandas import DataFrame
from utils import get_fake_date_time, getstr


def query1(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime(2018, 11, 27, 0, 0, 0)

    def preload_data():
        # get one charging station to be used for nearest_station attribute of customers
        sql = "SELECT * FROM charging_stations LIMIT 1"
        cursor.execute(sql)
        station = cursor.fetchone()

        sql = "DELETE FROM customers WHERE username = %s OR full_name = %s OR " \
              "email = %s OR phone_number = %s OR bank_account = %s "
        value = ("Liza", "Elizabeth Test", "elizabeth@gmail.com",
                 "123456789", "12341234")
        cursor.execute(sql, value)
        conn.commit()

        # insert a customer into table
        sql = "INSERT INTO customers (username, full_name, email, phone_number, " \
              "bank_account, gps_location, address, nearest_station) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        value = value + ("gps-location", "address", station[0])
        cursor.execute(sql, value)
        conn.commit()
        customer_id = cursor.lastrowid

        # get 5 car plates to add rent records between the customer and cars
        sql = "SELECT * FROM cars LIMIT 5"
        cursor.execute(sql)
        rand_cplates = [car[0] for car in cursor.fetchall()]

        # create 5 rent records between the customer and chosen cars on a specific day
        date_time = date + timedelta(hours=0)
        sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
              "VALUES (%s, %s, %s, %s, %s)"
        for i in range(5):
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
        value = ("ANINAS123", model[0], "red")
        cursor.execute(sql, value)
        conn.commit()

        # create a rent record between the customer and this car
        sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
              "VALUES (%s, %s, %s, %s, %s)"
        date_from = get_fake_date_time(start=date_time, end=date_time + timedelta(hours=3))
        date_to = get_fake_date_time(start=date_from, end=date_time + timedelta(hours=3))
        value = (getstr(date_from), getstr(date_to), customer_id, "ANINAS123", randint(1, 100))
        cursor.execute(sql, value)
        conn.commit()

    preload_data()
    query = "SELECT car.plate AS Plate, car.cmodel AS Model, car.color AS Color " \
            "FROM rent_records AS r " \
            "INNER JOIN cars AS car ON r.cplate = car.plate " \
            "INNER JOIN customers AS c ON r.cid = c.id " \
            "WHERE c.username = %s AND DATE(r.date_from) = DATE(%s) " \
            "AND car.color = %s AND car.plate LIKE (CONCAT(%s, '%'))"
    val = ("Liza", date, "red", "AN")
    cursor.execute(query, val)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query2(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime(2018, 10, 5, 0, 0, 0)

    def preload_data():
        # get five charging stations to be used for statistics
        sql = "SELECT * FROM charging_stations LIMIT 5"
        cursor.execute(sql)
        # get ids and # of sockets of five stations
        data = [station for station in cursor.fetchall()]
        rand_stations_id = [x[0] for x in data]
        no_of_socket = [x[3] for x in data]

        sql = "INSERT INTO charging_station_sockets (station_id, no_of_available_sockets, date_time) " \
              "VALUES (%s, %s, %s)"
        date_times = [date + timedelta(hours=x) for x in range(24)]
        for i in range(len(rand_stations_id)):
            for date_time in date_times:
                value = (rand_stations_id[i], randint(0, no_of_socket[i]), getstr(date_time))
                cursor.execute(sql, value)
        conn.commit()

    preload_data()
    query = "SELECT CONCAT(HOUR(css.date_time), 'h-', HOUR(css.date_time) + 1, 'h') AS Period, " \
            "SUM(cs.total_no_of_sockets - css.no_of_available_sockets) AS OccupiedSockets " \
            "FROM charging_station_sockets AS css " \
            "INNER JOIN charging_stations AS cs ON css.station_id = cs.id " \
            "WHERE DATE(css.date_time) = DATE(%s) GROUP BY TIME(css.date_time)"
    val = (getstr(date),)
    cursor.execute(query, val)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query3(conn: MySQLConnection):
    def preload_data():
        return  # no need to preload data, use the sample data from the database

    preload_data()
    cursor = conn.cursor()
    sql = "SELECT (SELECT COUNT(DISTINCT cplate) FROM rent_records " \
          "WHERE (DATE(date_from) BETWEEN DATE(%s) AND DATE(%s)) AND " \
          "(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s)))/(SELECT COUNT(*) FROM cars) AS Morning, " \
          "(SELECT COUNT(DISTINCT cplate) FROM rent_records " \
          "WHERE (DATE(date_from) BETWEEN DATE(%s) AND DATE(%s)) AND " \
          "(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s)))/(SELECT COUNT(*) FROM cars) AS Afternoon, " \
          "(SELECT COUNT(DISTINCT cplate) FROM rent_records " \
          "WHERE (DATE(date_from) BETWEEN DATE(%s) AND DATE(%s)) AND " \
          "(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s)))/(SELECT COUNT(*) FROM cars) AS Evening"
    d1 = getstr(datetime(2018, 9, 1))
    d2 = getstr(datetime(2018, 9, 7))
    mor1 = time(7, 0)
    mor2 = time(10, 0)
    aft1 = time(12, 0)
    aft2 = time(14, 0)
    eve1 = time(17, 0)
    eve2 = time(19, 0)
    value = (d1, d2, mor1, mor2, d1, d2, aft1, aft2, d1, d2, eve1, eve2)
    cursor.execute(sql, value)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query4(conn: MySQLConnection):
    cursor = conn.cursor()
    d1 = datetime(2018, 9, 1)
    d2 = datetime(2018, 9, 30)

    def preload_data():
        # get one deposit
        sql = "SELECT id FROM deposits LIMIT 1"
        cursor.execute(sql)
        deposit_id = cursor.fetchone()[0]

        # get the customer id
        sql = "SELECT id FROM customers WHERE username = %s"
        val = ("Liza",)
        cursor.execute(sql, val)
        customer_id = cursor.fetchone()[0]

        # get one car plate
        sql = "SELECT plate FROM cars LIMIT 1"
        cursor.execute(sql)
        cplate = cursor.fetchone()[0]

        # delete previous payment records with trans_no between 1 and 31 to avoid insertion errors
        sql = "DELETE FROM payment_records WHERE no_of_transaction BETWEEN 1 AND 30"
        cursor.execute(sql)
        conn.commit()

        date = d1 + timedelta(hours=0)
        # insert payment and rent records
        for i in range(1, 31):
            date_from = get_fake_date_time(start=date, end=date + timedelta(days=1))
            date_to = get_fake_date_time(start=date_from, end=date_from + timedelta(hours=3))
            sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            val = (getstr(date_from), getstr(date_to), customer_id, cplate, randint(10, 100))
            cursor.execute(sql, val)

            pay_time = get_fake_date_time(start=date_from, end=date_to)
            sql = "INSERT INTO payment_records (no_of_transaction, date_time, cid, did, price) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            val = (i, getstr(pay_time), customer_id, deposit_id, randint(10, 100))
            cursor.execute(sql, val)
            date = date_to
        conn.commit()

    preload_data()
    query = "SELECT rr.id AS RentId, rr.date_to AS RentFromDateTime, rr.date_to AS RentToDateTime, " \
            "pr.no_of_transaction AS NoOfTransaction, pr.date_time AS PaymentDateTime " \
            "FROM rent_records AS rr " \
            "INNER JOIN payment_records AS pr ON (pr.date_time BETWEEN rr.date_from AND rr.date_to) " \
            "AND rr.cid = pr.cid " \
            "INNER JOIN customers AS c ON rr.cid = c.id WHERE c.username = %s " \
            "AND DATE(pr.date_time) BETWEEN DATE(%s) AND DATE(%s) " \
            "GROUP BY rr.id HAVING COUNT(pr.no_of_transaction) > 1"
    value = ("Liza", getstr(d1), getstr(d2))
    cursor.execute(query, value)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query5(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime(2018, 11, 27, 0, 0, 0)

    def preload_data():
        sql = "SELECT * FROM customers LIMIT 100"
        cursor.execute(sql)
        ids = [x[0] for x in cursor.fetchall()]

        sql = "SELECT * FROM cars LIMIT 50"
        cursor.execute(sql)
        plates = [x[0] for x in cursor.fetchall()]

        # remove all rent records on the date loaded by sample data
        sql = "DELETE FROM rent_records WHERE DATE(date_from) = DATE(%s)"
        cursor.execute(sql, (date,))
        conn.commit()

        # insert random rent records on the date with random pairs of customers and cars
        for i in range(100):
            sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            date_from = get_fake_date_time(start=date, end=date + timedelta(days=1))
            date_to = get_fake_date_time(start=date_from, end=date + timedelta(days=1))
            val = (date_from, date_to, choice(ids), choice(plates), randint(1, 100))
            cursor.execute(sql, val)
        conn.commit()

    preload_data()
    query = "SELECT AVG(MINUTE(TIMEDIFF(date_from, date_to))) AS AvgTripDurationInMinutes " \
            "FROM rent_records WHERE DATE(date_from) = %s"
    value = (date,)
    cursor.execute(query, value)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query6(conn: MySQLConnection):
    def preload_data():
        pass  # no need to preload data, use the sample data from the database

    preload_data()
    mor1 = time(7, 0)
    mor2 = time(10, 0)
    aft1 = time(12, 0)
    aft2 = time(14, 0)
    eve1 = time(17, 0)
    eve2 = time(19, 0)
    cursor = conn.cursor()
    sql = "SELECT COUNT(IF(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s), 1, NULL)) AS MorningTravels," \
          "COUNT(IF(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s), 1, NULL)) AS AfternoonTravels," \
          "COUNT(IF(TIME(date_from) BETWEEN TIME(%s) AND TIME(%s), 1, NULL)) AS EveningTravels " \
          "FROM rent_records"
    value = (mor1, mor2, aft1, aft2, eve1, eve2)
    cursor.execute(sql, value)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query7(conn: MySQLConnection):
    def preload_data():
        pass  # no need to preload data, use the sample data from the database

    start_first_month = datetime(2018, 8, 1)
    end_third_month = datetime(2018, 10, 31)
    preload_data()
    cursor = conn.cursor()
    # create variable in database - 10% of amount of all cars
    sql = "SELECT 0.1 * COUNT(*) FROM cars"
    cursor.execute(sql)
    limit = int(cursor.fetchone()[0])
    sql = "SELECT cplate AS CarPlate, COUNT(rr.id) AS RentAmount FROM rent_records AS rr " \
          "WHERE DATE(rr.date_from) BETWEEN DATE(%s) AND DATE(%s) " \
          "GROUP BY cplate ORDER BY RentAmount LIMIT %s"
    val = (start_first_month, end_third_month, limit)
    cursor.execute(sql, val)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query8(conn: MySQLConnection):
    cursor = conn.cursor()
    start_date = datetime(2018, 8, 1)
    end_date = datetime(2018, 8, 31)

    def preload_data():
        # get one customer_id to demostrate how our query works
        sql = "SELECT id FROM customers WHERE username = %s"
        val = ("Liza",)
        cursor.execute(sql, val)
        customer_id = cursor.fetchone()[0]
        # get 10 car plates to add them to renting and charge records
        sql = "SELECT plate FROM cars ORDER BY RAND() LIMIT 10"
        cursor.execute(sql)
        cplates = [car[0] for car in cursor.fetchall()]
        # get one random charging station id to add it to charge records
        sql = "SELECT id FROM charging_stations ORDER BY RAND() LIMIT 1"
        cursor.execute(sql)
        station_id = cursor.fetchone()[0]

        rent_sql = "INSERT INTO rent_records (date_from, date_to, cid, cplate, distance) " \
                   "VALUES (%s, %s, %s, %s, %s)"
        charge_sql = "INSERT INTO charge_records (date_time, sid, cplate, price) " \
                     "VALUES (%s, %s, %s, %s)"
        for cplate in cplates:
            # insert rent record
            date_from = get_fake_date_time(start=start_date, end=end_date - timedelta(days=1, hours=3))
            date_to = get_fake_date_time(start=date_from, end=date_from + timedelta(hours=2, minutes=59))
            val = (getstr(date_from), getstr(date_to), customer_id, cplate, randint(10, 100))
            cursor.execute(rent_sql, val)
            # insert charge record the same day of rent record
            date_time = get_fake_date_time(start=date_from.date(), end=date_from.date() + timedelta(hours=12))
            val = (getstr(date_time), station_id, cplate, randint(10, 100))
            cursor.execute(charge_sql, val)
        conn.commit()

    preload_data()
    query = "SELECT rr.cid AS CustomerId, COUNT(cr.id) AS Amount FROM rent_records AS rr " \
            "INNER JOIN charge_records AS cr ON rr.cplate = cr.cplate " \
            "AND DATE(rr.date_from) = DATE(cr.date_time) " \
            "WHERE DATE(cr.date_time) BETWEEN DATE(%s) AND DATE(%s) GROUP BY rr.cid"
    value = (start_date, end_date)
    cursor.execute(query, value)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query9(conn: MySQLConnection):
    def preload_data():
        pass  # no need to preload data, use the sample data from the database

    preload_data()
    cursor = conn.cursor()
    sql = "SELECT wid AS WorkshopID, type AS CarPartType, MAX(amount) AS Amount " \
          "FROM (SELECT D.wid, D.type, SUM(D.amount) AS amount " \
          "FROM (SELECT d.amount, o.wid, p.type FROM order_details as d " \
          "INNER JOIN orders AS o ON d.order_id = o.id " \
          "INNER JOIN car_parts AS p ON p.trade_name = d.trade_name AND p.pid = d.pid) AS D " \
          "GROUP BY D.wid, D.type ORDER BY Amount DESC) AS D2 GROUP BY WorkshopID"
    cursor.execute(sql)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def query10(conn: MySQLConnection):
    def preload_data():
        pass  # no need to preload data, use the sample data from the database

    preload_data()
    cursor = conn.cursor()
    sql = "SELECT cplate AS CarPlate, AVG(day_price) AS AvgPrice " \
          "FROM (SELECT cplate, SUM(price) AS day_price " \
          "FROM ((SELECT date_time, price, cplate FROM repair_records) UNION " \
          "(SELECT date_time, price, cplate FROM charge_records)) AS records " \
          "GROUP BY DATE(date_time), cplate) AS prices " \
          "GROUP BY cplate ORDER BY AvgPrice DESC LIMIT 1"
    cursor.execute(sql)
    return cursor.fetchall(), [i[0] for i in cursor.description]


def get_all_query_results(conn: MySQLConnection):
    results = []

    query_table, query_columns = query1(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_1', 'dataframe': df})

    query_table, query_columns = query2(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_2', 'dataframe': df})

    query_table, query_columns = query3(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_3', 'dataframe': df})

    query_table, query_columns = query4(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_4', 'dataframe': df})

    query_table, query_columns = query5(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_5', 'dataframe': df})

    query_table, query_columns = query6(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_6', 'dataframe': df})

    query_table, query_columns = query7(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_7', 'dataframe': df})

    query_table, query_columns = query8(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_8', 'dataframe': df})

    query_table, query_columns = query9(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_9', 'dataframe': df})

    query_table, query_columns = query10(conn)
    df = DataFrame(query_table, columns=query_columns)
    results.append({'name': 'Query_10', 'dataframe': df})

    return results
