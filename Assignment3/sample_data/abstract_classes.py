"""
This module contains an abstract class of Entity for the database

File name: abstract_classes.py
Author: Temur Kholmatov
Email: t.holmatov@innopolis.ru
Course: Data Modeling and Databases
Python Version: 3.5

"""
from abc import ABC, abstractmethod
from mysql.connector import MySQLConnection


class Entity(ABC):
    @abstractmethod
    def save(self, conn: MySQLConnection):
        pass

    @abstractmethod
    def duplicates(self, other):
        pass
