from .entity_classes import *
from faker import Faker
from random import choice
from mysql.connector.errors import IntegrityError


class SampleDatabase:

    def __init__(self, conn: MySQLConnection, fake=Faker, **kwargs):
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
        no_of_rent_records = 1500
        no_of_charging_records = 300
        no_of_repair_records = 80
        no_of_payment_records = 1500
        no_of_plug_properties = 30
        no_of_car_part_properties = 100
        no_of_order_payments = 50

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
        self.tables.append(SampleTable(self, 'charging_records', no_of_charging_records, ChargingRecord,
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
        self.tables.append(SampleTable(self, 'order_payments', no_of_order_payments, OrderPayment,
                                       context={'deposit': 'deposits',
                                                'provider': 'providers',
                                                'order': 'orders'}))
        # create data for tables
        for table in self.tables:
            table.create_data()
            print("Data created: " + table.name)

    def upload(self):
        for table in self.tables:
            table.upload()
            print("Data uploaded: " + table.name)


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
            unique_find_attempts = 10
            while unique_find_attempts:
                try:
                    if self.context is not None:
                        attributes = self.__create_attr_dict()
                        record = self.entity_model(**attributes, fake=self.database.fake)
                    else:
                        record = self.entity_model(fake=self.database.fake)
                    if not record.is_unique(self.database.conn) and self.__not_in_records(record):
                        raise IntegrityError("Duplicate entry")
                except IntegrityError as e:
                    if unique_find_attempts > 1:
                        unique_find_attempts -= 1
                    else:
                        raise IntegrityError("Cannot find unique sample data to insert to table\n" + e.__str__())
                    continue
                else:
                    break
            self.records.append(record)

    def __not_in_records(self, record):
        for other in self.records:
            if other == record:
                return False
        return True

    def __create_attr_dict(self):
        attributes = dict()
        for key, val in self.context.items():
            try:
                ref_table = [table for table in self.database.tables if table.name == val][0]
            except IndexError as e:
                raise KeyError("The key reference to the table does not exist!\n" + e.__str__())
            attributes[key] = choice(ref_table.records)
        return attributes

    def upload(self):
        for record in self.records:
            record.save(self.database.conn)
