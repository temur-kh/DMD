from faker import Faker
from datetime import datetime


def get_car_part_names():
    with open('sample_data/car_part_names.txt', 'r') as file:
        names = file.readlines()
    return names


def get_fake_date_time(fake=Faker(), start=datetime(2018, 1, 1, 0, 0, 0), end=datetime(2018, 12, 31, 23, 59, 59)):
    return fake.date_time_between_dates(
        datetime_start=start,
        datetime_end=end
    )


def getstr(date_time):
    return str(date_time.isoformat())
