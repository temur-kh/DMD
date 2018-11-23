from mysql.connector.connection import MySQLConnection


def query1(conn: MySQLConnection):
    def preload_data():
        pass  # TODO
    preload_data()
    cursor = conn.cursor()
    sql = str  # TODO
    val = tuple  # TODO
    cursor.execute(sql, val)
    return cursor.fetchall(), [i[0] for i in cursor.description]


