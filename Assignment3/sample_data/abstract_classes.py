from abc import ABC, abstractmethod
from mysql.connector import MySQLConnection


class Entity(ABC):
    @abstractmethod
    def save(self, conn: MySQLConnection):
        pass

    @abstractmethod
    def duplicates(self, other):
        pass
