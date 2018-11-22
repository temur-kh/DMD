from faker import Faker
from random import randint
from datetime import datetime
from mysql.connector import MySQLConnection


def get_car_part_names():
    with open('car_part_names.txt', 'r') as file:
        names = file.readlines()
    return names


def get_fake_date_time(fake, start=datetime(2018, 1, 1, 0, 0, 0), end=datetime(2018, 12, 31, 23, 59, 59)):
    return fake.date_time_between_dates(
        datetime_start=start,
        datetime_end=end
    )


class Customer:
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

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO customers " \
              "(full_name, phone_number, email, bank_account, username, gps_location, address, nearest_station)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.name, self.phone_number, self.email, self.bank_account,
               self.username, self.gps_location, self.address, self.nearest_station)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class Deposit:
    def __init__(self, fake=Faker()):
        self.id = None
        self.bank_account = fake.credit_car_number()

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO deposits " \
              "(bank_account) " \
              "VALUES (%s)"
        val = (self.bank_account,)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class CarModel:
    def __init__(self, plug, fake=Faker()):
        self.model = fake.company()
        self.rent_price = randint(10, 100)
        self.charging_capacity = randint(100, 300)
        self.plug = plug

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO car_models " \
              "(model, rent_price, charging_capacity, pmodel) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.model, self.rent_price, self.charging_capacity, self.plug.model)
        cursor.execute(sql, val)
        db.commit()


class Car:
    def __init__(self, car_model, fake=Faker()):
        self.plate = fake.license_plate()
        self.car_model = car_model
        self.color = fake.safe_color_name()

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO cars " \
              "(plate, cmodel, color) " \
              "VALUES (%s, %s, %s)"
        val = (self.plate, self.car_model, self.color)
        cursor.execute(sql, val)
        db.commit()


class ChargingStation:
    def __init__(self, fake=Faker()):
        self.id = None
        self.gps_location = str(fake.latitude()) + " " + str(fake.longitude())
        self.price_per_amount = randint(5, 50)
        self.total_no_of_sockets = randint(1, 25)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO charging_stations " \
              "(gps_location, price_per_amount, total_no_of_sockets) " \
              "VALUES (%s, %s, %s)"
        val = (self.gps_location, self.price_per_amount, self.total_no_of_sockets)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class Plug:
    def __init__(self, fake=Faker()):
        self.model = fake.company()
        self.shape = fake.random_uppercase_letter()
        self.size = fake.random_digit_not_null()
        self.charging_speed = randint(5, 10)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO plugs " \
              "(model, shape, size, charging_speed) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.model, self.shape, self.size, self.charging_speed)
        cursor.execute(sql, val)
        db.commit()


class Workshop:
    def __init__(self, fake=Faker()):
        self.id = None
        self.location = fake.address()
        self.available_timing = randint(0, 24)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO workshops " \
              "(location, available_timing) " \
              "VALUES (%s, %s)"
        val = (self.location, self.available_timing)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class Provider:
    def __init__(self, fake=Faker()):
        self.id = None
        self.name = fake.company()
        self.address = fake.address()
        self.phone_number = fake.phone_number()
        self.bank_account = fake.credit_car_number()

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO providers " \
              "(name, address, phone_number, bank_account) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.name, self.address, self.phone_number, self.bank_account)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class CarPart:
    def __init__(self, provider, fake=Faker()):
        self.trade_name = fake.user_name()
        self.provider = provider
        self.type = fake.random_element(elements=tuple(get_car_part_names()))
        self.price = randint(25, 500)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO car_parts " \
              "(trade_name, pid, type, price) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.trade_name, self.provider.id, self.type, self.price)
        cursor.execute(sql, val)
        db.commit()


class Order:
    def __init__(self, workshop, provider, payment, fake=Faker()):
        self.id = None
        self.workshop = workshop
        self.provider = provider
        self.date_time = get_fake_date_time(fake)
        self.payment = payment

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO orders " \
              "(wid, pid, date_time, no_of_transaction) " \
              "VALUES (%s, %s, '%s', %s)"
        val = (self.workshop.id, self.provider.id, self.date_time, self.payment.transaction)
        cursor.execute(sql, val)  # TODO insertion of datetime is to be checked
        db.commit()
        self.id = cursor.lastrowid


class RentRecord:
    def __init__(self, customer, car, fake=Faker()):
        self.id = None
        self.customer = customer
        self.car = car
        self.distance = randint(1, 100)
        self.from_date_time = get_fake_date_time(fake)
        self.to_date_time = get_fake_date_time(fake)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO rent_records " \
              "(cid, cplate, distance, date_from, date_to) " \
              "VALUES (%s, %s, %s, '%s', '%s')"
        val = (self.customer.id, self.car.plate, self.distance, self.from_date_time, self.to_date_time)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class ChargingRecord:
    def __init__(self, charging_station, car, fake=Faker()):
        self.id = None
        self.charging_station = charging_station
        self.car = car
        self.price = charging_station.price_per_amount * car.charging_capacity
        self.date_time = get_fake_date_time(fake)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO charge_records " \
              "(sid, cplate, price, date_time) " \
              "VALUES (%s, %s, %s, '%s')"
        val = (self.charging_station.id, self.car.plate, self.price, self.date_time)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class RepairRecord:
    def __init__(self, workshop, car, fake=Faker()):
        self.id = None
        self.workshop = workshop
        self.car = car
        self.price = randint(50, 1000)
        self.date_time = get_fake_date_time(fake)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO repair_records " \
              "(wid, cplate, price, date_time) " \
              "VALUES (%s, %s, %s, '%s')"
        val = (self.workshop.id, self.car.plate, self.price, self.date_time)
        cursor.execute(sql, val)
        db.commit()
        self.id = cursor.lastrowid


class PaymentRecord:
    def __init__(self, customer, deposit, fake=Faker()):
        self.transaction = fake.random_number(digits=9, fix_len=True)
        self.customer = customer
        self.deposit = deposit
        self.price = randint(10, 10000)
        self.date_time = get_fake_date_time(fake)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO payment_records " \
              "(no_of_transaction, cid, did, price, date_time) " \
              "VALUES (%s, %s, %s, %s, '%s')"
        val = (self.transaction, self.customer.id, self.deposit.id, self.price, self.date_time)
        cursor.execute(sql, val)
        db.commit()


class PlugProperty:
    def __init__(self, charging_station, plug, fake=Faker()):
        self.charging_station = charging_station
        self.plug = plug
        self.amount = randint(1, 10)
        _ = fake

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO plug_properties " \
              "(sid, pmodel, amount) " \
              "VALUES (%s, %s, %s)"
        val = (self.charging_station.id, self.plug.model, self.amount)
        cursor.execute(sql, val)
        db.commit()


class CarPartProperty:
    def __init__(self, workshop, car_part, fake=Faker()):
        self.workshop = workshop
        self.car_part = car_part
        self.amount = randint(0, 50)
        _ = fake

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO car_part_properties " \
              "(wid, trade_name, pid, amount) " \
              "VALUES (%s, %s, %s, %s)"
        val = (self.workshop.id, self.car_part.trade_name, self.car_part.provider.id, self.amount)
        cursor.execute(sql, val)
        db.commit()


class OrderPayment:
    def __init__(self, deposit, provider, order, fake=Faker()):
        self.transaction = fake.random_number(digits=9, fix_len=True)
        self.deposit = deposit
        self.provider = provider
        self.price = randint(25, 10000)
        self.date_time = get_fake_date_time(fake, start=order.date_time)

    def save(self, db: MySQLConnection):
        cursor = db.cursor()
        sql = "INSERT INTO order_payment_records " \
              "(no_of_transaction, did, pid, price, date_time) " \
              "VALUES (%s, %s, %s, %s, '%s')"
        val = (self.transaction, self.deposit.id, self.provider.id, self.price, self.date_time)
        cursor.execute(sql, val)
        db.commit()


#############################################################################################
#############################################################################################

# for testing purposes
if __name__ == "__main__":
    fk = Faker()
    user = Customer(fk)
    print(user.name, user.phone_number)
