from mysql.connector.connection import MySQLConnection
import datetime

def query1(conn: MySQLConnection):
    def preload_data():
        sql = "INSERT INTO customers (username, full_name, email, phone_number, bank_account, gps_location, address, nearest_station) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("Liza", "Elizabeth", "elizabeth@gmail.com", "123456789", "")
        cursor.execute(sql, val)
        sql = "INSERT INTO cars (plate, cmodel, color) " \
              "VALUES(%s, %s, %s)"
        model = "INSERT INTO car_models (model, rent_price, charging_capacity, pmodel) " \
                "VALUES (%s, %s, %s, %s)"
        val = ("VOLVO", "123", "123", "VOLVO")
        cursor.execute(model, val)
        val = ("ANINAS", "red")
        cursor.execute(sql, val)
    preload_data()
    cursor = conn.cursor()
    query = "SELECT * FROM cars WHERE color = %s AND SUBSTRING(plate,1,2) = %s"
    val = ("red", "AN")
    cursor.execute(query, val)



def query2(conn: MySQLConnection):
    cursor = conn.cursor()
    date = datetime.date(2010, 5, 5)
    for i in range()
    query = "SELECT * FROM charge_records WHERE date_time BETWEEN %s AND %s"
    for i in range(24):
        count = 0
        currentHour = datetime.datetime.combine(date, datetime.time(i))
        nextHour = datetime.datetime.combine(date, datetime.time(i + 1))
        cursor.execute(query, (currentHour, nextHour))
        myresult = cursor.fetchall()
        for x in cursor:
            count += 1
        print(i + "h - " + (i+1) + "h:" + count)
