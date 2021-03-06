"""
This module contains two classes used to create a database:
SampleDatabase: a class to create fake data and upload it to a database
SampleTable: a class to create fake data, upload data and create a DataFrame object from it.

File name: sample_database.py
Author: Temur Kholmatov
Email: t.holmatov@innopolis.ru
Course: Data Modeling and Databases
Python Version: 3.5

"""

from .entity_classes import *
from faker import Faker
from random import choice
from mysql.connector.errors import IntegrityError
from pandas import DataFrame


class SampleDatabase:

    def __init__(self, conn: MySQLConnection, fake=Faker(), **kwargs):
        self.conn = conn
        self.fake = fake
        # initialize numbers of records in each table
        no_of_deposits = 10
        no_of_customers = 500
        no_of_providers = 20
        no_of_workshops = 10
        no_of_cars = 60
        no_of_car_models = 5
        no_of_charging_stations = 15
        no_of_plugs = 5
        no_of_car_parts = 100
        no_of_orders = 50
        no_of_rent_records = 5000
        no_of_charging_records = 300
        no_of_repair_records = 80
        no_of_payment_records = 5000
        no_of_plug_properties = 30
        no_of_car_part_properties = 100
        no_of_order_payments = 50
        no_of_station_sockets = 100
        no_of_order_details = 60

        # reinitialize some attributes if provided
        for key, value in kwargs:
            try:
                locals()[key] = value
            except KeyError as e:
                raise KeyError("Attribute does not exist!\n" + e.__str__())

        # initialize sample table objects
        self.tables = []
        self.tables.append(SampleTable(self, 'deposits', no_of_deposits, Deposit))
        self.tables.append(SampleTable(self, 'providers', no_of_providers, Provider))
        self.tables.append(SampleTable(self, 'workshops', no_of_workshops, Workshop))
        self.tables.append(SampleTable(self, 'charging_stations', no_of_charging_stations, ChargingStation))
        self.tables.append(SampleTable(self, 'plugs', no_of_plugs, Plug))
        self.tables.append(SampleTable(self, 'customers', no_of_customers, Customer,
                                       context={'nearest_station': 'charging_stations'}))
        self.tables.append(SampleTable(self, 'car_models', no_of_car_models, CarModel,
                                       context={'plug': 'plugs'}))
        self.tables.append(SampleTable(self, 'cars', no_of_cars, Car,
                                       context={'car_model': 'car_models'}))
        self.tables.append(SampleTable(self, 'car_parts', no_of_car_parts, CarPart,
                                       context={'provider': 'providers'}))
        self.tables.append(SampleTable(self, 'rent_records', no_of_rent_records, RentRecord,
                                       context={'customer': 'customers',
                                                'car': 'cars'}))
        self.tables.append(SampleTable(self, 'charging_station_sockets', no_of_station_sockets, StationSockets,
                                       context={'station': 'charging_stations'}))
        self.tables.append(SampleTable(self, 'charge_records', no_of_charging_records, ChargingRecord,
                                       context={'charging_station': 'charging_stations',
                                                'car': 'cars'}))
        self.tables.append(SampleTable(self, 'repair_records', no_of_repair_records, RepairRecord,
                                       context={'workshop': 'workshops',
                                                'car': 'cars'}))
        self.tables.append(SampleTable(self, 'payment_records', no_of_payment_records, PaymentRecord,
                                       context={'customer': 'customers',
                                                'deposit': 'deposits'}))
        self.tables.append(SampleTable(self, 'plug_properties', no_of_plug_properties, PlugProperty,
                                       context={'charging_station': 'charging_stations',
                                                'plug': 'plugs'}))
        self.tables.append(SampleTable(self, 'car_part_properties', no_of_car_part_properties, CarPartProperty,
                                       context={'workshop': 'workshops',
                                                'car_part': 'car_parts'}))
        self.tables.append(SampleTable(self, 'orders', no_of_orders, Order,
                                       context={'workshop': 'workshops',
                                                'provider': 'providers'}))
        self.tables.append(SampleTable(self, 'order_details', no_of_order_details, OrderDetails,
                                       context={'order': 'orders',
                                                'car_part': 'car_parts'}))
        self.tables.append(SampleTable(self, 'order_payment_records', no_of_order_payments, OrderPayment,
                                       context={'deposit': 'deposits',
                                                'provider': 'providers',
                                                'order': 'orders'}))

    def create_data(self):
        # create data for tables
        for table in self.tables:
            table.create_data()
            print("Data created: " + table.name)
        print("Creation of data in database is completed!")

    def upload(self):
        for table in self.tables:
            table.upload()
            print("Data uploaded: " + table.name)
        print("Upload of data to database is completed!")


class SampleTable:
    def __init__(self, database: SampleDatabase, name, no_of_records, entity_model, context=None):
        self.database = database
        self.name = name
        self.no_of_records = no_of_records
        self.records = []
        self.entity_model = entity_model
        self.context = context

    def create_data(self):
        for i in range(self.no_of_records):
            record = None
            unique_find_attempts = 100
            while unique_find_attempts:
                try:
                    if self.context is not None:
                        attributes = self.__create_attr_dict()
                        record = self.entity_model(**attributes, fake=self.database.fake)
                    else:
                        record = self.entity_model(fake=self.database.fake)
                    if self.__in_records(record):
                        raise IntegrityError("Duplicate entry")
                except IntegrityError:
                    unique_find_attempts -= 1
                    if not unique_find_attempts:
                        raise IntegrityError("Cannot find unique sample data to insert to table. "
                                             "Attempts left: {}.\n".format(unique_find_attempts))
                    del record
                    continue
                else:
                    break
            self.records.append(record)

    def __in_records(self, record):
        for other in self.records:
            if record.duplicates(other):
                return True
        return False

    def __create_attr_dict(self):
        attributes = dict()
        for key, val in self.context.items():
            try:
                ref_table = [table for table in self.database.tables if table.name == val][0]
            except IndexError as e:
                raise KeyError("The key reference to the table does not exist!\n" + e.__str__())
            if self.no_of_records == ref_table.no_of_records:
                attributes[key] = ref_table.records[len(self.records)]  # in case of one-to-one relationship
            else:
                attributes[key] = choice(ref_table.records)
        return attributes

    def upload(self):
        for record in self.records:
            record.save(self.database.conn)

    def get_dataframe(self):
        cursor = self.database.conn.cursor()
        sql = "SELECT * FROM %s"
        cursor.execute(sql % self.name)
        df = DataFrame(cursor.fetchall())
        df.columns = [i[0] for i in cursor.description]
        cursor.close()
        return df
