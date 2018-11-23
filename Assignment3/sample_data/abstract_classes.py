from abc import ABC, abstractmethod
from mysql.connector import MySQLConnection


class Entity(ABC):
    # @abstractmethod
    # @property
    # def primary_keys(self):
    #     pass

    @abstractmethod
    def is_unique(self, conn: MySQLConnection):
        pass

    @abstractmethod
    def save(self, conn: MySQLConnection):
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
