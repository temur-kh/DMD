from faker import Faker
from random import randint
from datetime import datetime, timedelta
from mysql.connector import MySQLConnection
from .abstract_classes import Entity


def get_car_part_names():
    with open('sample_data/car_part_names.txt', 'r') as file:
        names = file.readlines()
    return names


def get_fake_date_time(fake, start=datetime(2018, 1, 1, 0, 0, 0), end=datetime(2018, 12, 31, 23, 59, 59)):
    return fake.date_time_between_dates(
        datetime_start=start,
        datetime_end=end
    )


def getstr(date_time):
    return str(date_time.isoformat())


class Customer(Entity):
    def __init__(self, nearest_station, fake=Faker()):
        self.id = None
        self.name = fake.name()
        self.phone_number = fake.phone_number()
        self.email = fake.email()
        self.bank_account = fake.credit_card_number()
        self.username = fake.user_name()
        self.gps_location = str(fake.latitude()) + " " + str(fake.longitude())
        self.address = fake.address()
        self.nearest_station = nearest_station

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM customers WHERE bank_account = %s OR phone_number = %s OR username = %s"
        val = (self.bank_account, self.phone_number, self.username)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO customers " \
              "(full_name, phone_number, email, bank_account, username, gps_location, address, nearest_station)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.name, self.phone_number, self.email, self.bank_account,
               self.username, self.gps_location, self.address, self.nearest_station.id)
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class Deposit(Entity):
    def __init__(self, fake=Faker()):
        self.id = None
        self.bank_account = fake.credit_card_number()

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM deposits WHERE bank_account = %s"
        val = (self.bank_account,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO deposits " \
              "(bank_account) " \
              "VALUES (%s)"
        val = (self.bank_account,)
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class CarModel(Entity):
    def __init__(self, plug, fake=Faker()):
        self.model = fake.company()
        self.rent_price = randint(10, 100)
        self.charging_capacity = randint(100, 300)
        self.plug = plug

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM car_models WHERE model = %s"
        val = (self.model,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO car_models " \
              "(model, rent_price, charging_capacity, pmodel) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.model, self.rent_price, self.charging_capacity, self.plug.model)
        cursor.execute(sql, val)
        conn.commit()


class Car(Entity):
    def __init__(self, car_model, fake=Faker()):
        self.plate = fake.license_plate()
        self.car_model = car_model
        self.color = fake.safe_color_name()

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM cars WHERE plate = %s"
        val = (self.plate,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO cars " \
              "(plate, cmodel, color) " \
              "VALUES (%s, %s, %s)"
        val = (self.plate, self.car_model.model, self.color)
        cursor.execute(sql, val)
        conn.commit()


class ChargingStation(Entity):
    def __init__(self, fake=Faker()):
        self.id = None
        self.gps_location = str(fake.latitude()) + " " + str(fake.longitude())
        self.price_per_amount = randint(5, 50)
        self.total_no_of_sockets = randint(1, 25)

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM charging_stations WHERE gps_location = %s"
        val = (self.gps_location,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO charging_stations " \
              "(gps_location, price_per_amount, total_no_of_sockets) " \
              "VALUES (%s, %s, %s)"
        val = (self.gps_location, self.price_per_amount, self.total_no_of_sockets)
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class Plug(Entity):
    def __init__(self, fake=Faker()):
        self.model = fake.company()
        self.shape = fake.random_uppercase_letter()
        self.size = fake.random_digit_not_null()
        self.charging_speed = randint(5, 10)

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM plugs WHERE model = %s"
        val = (self.model,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO plugs " \
              "(model, shape, size, charging_speed) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.model, self.shape, self.size, self.charging_speed)
        cursor.execute(sql, val)
        conn.commit()


class Workshop(Entity):
    def __init__(self, fake=Faker()):
        self.id = None
        self.location = fake.address()
        self.available_timing = randint(0, 24)

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM workshops WHERE location = %s"
        val = (self.location,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO workshops " \
              "(location, available_timing) " \
              "VALUES (%s, %s)"
        val = (self.location, self.available_timing)
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class Provider(Entity):
    def __init__(self, fake=Faker()):
        self.id = None
        self.name = fake.company()
        self.address = fake.address()
        self.phone_number = fake.phone_number()
        self.bank_account = fake.credit_card_number()

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM providers " \
              "WHERE name = %s OR address = %s OR phone_number = %s OR bank_account = %s"
        val = (self.name, self.address, self.phone_number, self.bank_account)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO providers " \
              "(name, address, phone_number, bank_account) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.name, self.address, self.phone_number, self.bank_account)
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class CarPart(Entity):
    def __init__(self, provider, fake=Faker()):
        self.trade_name = fake.user_name()
        self.provider = provider
        self.type = fake.random_element(elements=tuple(get_car_part_names()))
        self.price = randint(25, 500)

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM car_parts WHERE trade_name = %s AND pid = %s"
        val = (self.trade_name, self.provider.id)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO car_parts " \
              "(trade_name, pid, type, price) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.trade_name, self.provider.id, self.type, self.price)
        cursor.execute(sql, val)
        conn.commit()


class Order(Entity):
    def __init__(self, workshop, provider, fake=Faker()):
        self.id = None
        self.workshop = workshop
        self.provider = provider
        self.date_time = get_fake_date_time(fake)
        self.payment = None

    def is_unique(self, conn: MySQLConnection):
        _ = self.id
        _ = conn
        return True  # seems no checking is needed

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        if not self.id:
            sql = "INSERT INTO orders " \
                  "(wid, pid, date_time, no_of_transaction) " \
                  "VALUES (%s, %s, %s, %s)"
            val = (self.workshop.id, self.provider.id, getstr(self.date_time), None)
            cursor.execute(sql, val)
            conn.commit()
            self.id = cursor.lastrowid
        else:
            sql = "UPDATE orders SET " \
                  "wid=%s, pid=%s, date_time=%s, " \
                  "no_of_transaction=%s WHERE id=%s"
            val = (self.workshop.id, self.provider.id, getstr(self.date_time), self.payment.transaction)
            cursor.execute(sql, val)
            conn.commit()


class RentRecord(Entity):
    def __init__(self, customer, car, fake=Faker()):
        self.id = None
        self.customer = customer
        self.car = car
        self.distance = randint(1, 100)
        self.from_date_time = get_fake_date_time(fake)
        self.to_date_time = get_fake_date_time(fake,
                                               start=self.from_date_time,
                                               end=self.from_date_time + timedelta(days=1))

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM rent_records " \
              "WHERE (cid = %s OR cplate = %s) AND ((date_from BETWEEN %s AND %s) OR (date_to BETWEEN %s AND %s))"
        val = (self.customer.id, self.car.plate, self.from_date_time, self.to_date_time,
               self.from_date_time, self.to_date_time)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO rent_records " \
              "(cid, cplate, distance, date_from, date_to) " \
              "VALUES (%s, %s, %s, %s, %s)"
        val = (self.customer.id, self.car.plate, self.distance,
               getstr(self.from_date_time), getstr(self.to_date_time))
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class ChargingRecord(Entity):
    def __init__(self, charging_station, car, fake=Faker()):
        self.id = None
        self.charging_station = charging_station
        self.car = car
        self.price = charging_station.price_per_amount * car.car_model.charging_capacity
        self.date_time = get_fake_date_time(fake)

    def is_unique(self, conn: MySQLConnection):
        _ = self.id
        _ = conn
        return True  # need more complicated checking

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO charge_records " \
              "(sid, cplate, price, date_time) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.charging_station.id, self.car.plate, self.price, getstr(self.date_time))
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class RepairRecord(Entity):
    def __init__(self, workshop, car, fake=Faker()):
        self.id = None
        self.workshop = workshop
        self.car = car
        self.price = randint(50, 1000)
        self.date_time = get_fake_date_time(fake)

    def is_unique(self, conn: MySQLConnection):
        _ = self.id
        _ = conn
        return True  # seems no checking is needed or it is too complicated for a moment

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO repair_records " \
              "(wid, cplate, price, date_time) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.workshop.id, self.car.plate, self.price, getstr(self.date_time))
        cursor.execute(sql, val)
        conn.commit()
        self.id = cursor.lastrowid


class PaymentRecord(Entity):
    def __init__(self, customer, deposit, fake=Faker()):
        self.transaction = fake.random_number(digits=9, fix_len=True)
        self.customer = customer
        self.deposit = deposit
        self.price = randint(10, 10000)
        self.date_time = get_fake_date_time(fake)

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM payment_records WHERE no_of_transaction = %s"
        val = (self.transaction,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO payment_records " \
              "(no_of_transaction, cid, did, price, date_time) " \
              "VALUES (%s, %s, %s, %s, %s)"
        val = (self.transaction, self.customer.id, self.deposit.id, self.price, getstr(self.date_time))
        cursor.execute(sql, val)
        conn.commit()


class PlugProperty(Entity):
    def __init__(self, charging_station, plug, fake=Faker()):
        self.charging_station = charging_station
        self.plug = plug
        self.amount = randint(1, 10)
        _ = fake

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM plug_properties WHERE sid = %s AND pmodel = %s"
        val = (self.charging_station.id, self.plug.model)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO plug_properties " \
              "(sid, pmodel, amount) " \
              "VALUES (%s, %s, %s)"
        val = (self.charging_station.id, self.plug.model, self.amount)
        cursor.execute(sql, val)
        conn.commit()


class CarPartProperty(Entity):

    def __init__(self, workshop, car_part, fake=Faker()):
        self.workshop = workshop
        self.car_part = car_part
        self.amount = randint(0, 50)
        _ = fake

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM car_part_properties WHERE wid = %s AND trade_name = %s AND pid = %s"
        val = (self.workshop.id, self.car_part.trade_name, self.car_part.provider.id)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO car_part_properties " \
              "(wid, trade_name, pid, amount) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.workshop.id, self.car_part.trade_name, self.car_part.provider.id, self.amount)
        cursor.execute(sql, val)
        conn.commit()


class OrderPayment(Entity):
    def __init__(self, deposit, provider, order, fake=Faker()):
        self.transaction = fake.random_number(digits=9, fix_len=True)
        self.deposit = deposit
        self.provider = provider
        self.price = randint(25, 10000)
        self.date_time = get_fake_date_time(fake, start=order.date_time)
        self.order = order
        self.order.payment = self

    def is_unique(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM order_payment_records WHERE no_of_transaction = %s"
        val = (self.transaction,)
        cursor.execute(sql, val)
        return not cursor.fetchone()[0]

    def save(self, conn: MySQLConnection):
        cursor = conn.cursor()
        sql = "INSERT INTO order_payment_records " \
              "(no_of_transaction, did, pid, price, date_time) " \
              "VALUES (%s, %s, %s, %s, %s)"
        val = (self.transaction, self.deposit.id, self.provider.id, self.price, getstr(self.date_time))
        cursor.execute(sql, val)
        self.order.save(conn)
        conn.commit()
