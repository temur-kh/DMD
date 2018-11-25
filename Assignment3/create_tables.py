from mysql.connector import MySQLConnection
import subprocess


def create_database(db):
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `company`")
    cursor.execute("USE `company`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `plugs`("
                   "`model` VARCHAR(50) NOT NULL, "
                   "`shape` VARCHAR(30) NOT NULL, "
                   "`size` INTEGER NOT NULL,"
                   "`charging_speed` INTEGER NOT NULL, "
                   "PRIMARY KEY (`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_models`("
                   "`model` VARCHAR(50) NOT NULL, "
                   "`rent_price` INTEGER NOT NULL,"
                   "`charging_capacity` INTEGER NOT NULL, "
                   "`pmodel` VARCHAR(50) NOT NULL,"
                   "PRIMARY KEY (`model`),"
                   "FOREIGN KEY (`pmodel`) REFERENCES `plugs`(`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `cars`("
                   "`plate` VARCHAR(30) NOT NULL, "
                   "`cmodel` VARCHAR(50) NOT NULL, "
                   "`color` VARCHAR(30) NOT NULL, "
                   "PRIMARY KEY (`plate`),"
                   "FOREIGN KEY (`cmodel`) REFERENCES `car_models`(`model`))")

    # cursor.execute("CREATE TABLE IF NOT EXISTS `car_parts`("
    #                "`trade_name` VARCHAR(30) NOT NULL, "
    #                "`type` VARCHAR(30) NOT NULL, "
    #                "`car_model` VARCHAR(30) NOT NULL, "
    #                "PRIMARY KEY (`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `providers`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`name` VARCHAR(50) NOT NULL, "
                   "`address` VARCHAR(100), "
                   "`phone_number` VARCHAR(20),"
                   "`bank_account` VARCHAR(50) NOT NULL,"
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_parts`("
                   "`trade_name` VARCHAR(50) NOT NULL, "
                   "`pid` INTEGER NOT NULL, "
                   "`type` VARCHAR(30) NOT NULL, "
                   # "`car_model` VARCHAR(30) NOT NULL, "
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`trade_name`, `pid`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`) ON DELETE CASCADE "
                   "ON UPDATE CASCADE)")

    # cursor.execute("CREATE TABLE IF NOT EXISTS `car_part_prices`("
    #                "`trade_name` VARCHAR(30) NOT NULL, "
    #                "`pid` INTEGER NOT NULL, "
    #                "`price` INTEGER NOT NULL, "
    #                "PRIMARY KEY (`trade_name`, `pid`),"
    #                "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`),"
    #                "FOREIGN KEY (`trade_name`) REFERENCES `car_parts`(`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `deposits`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`bank_account` VARCHAR(50) NOT NULL, "
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charging_stations`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`gps_location` VARCHAR(30) NOT NULL, "
                   "`price_per_amount` INTEGER NOT NULL, "
                   "`total_no_of_sockets` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charging_station_sockets`("
                   "`station_id` INTEGER NOT NULL,"
                   "`no_of_available_sockets` INTEGER NOT NULL,"
                   "`date_time` DATETIME NOT NULL,"
                   "PRIMARY KEY (`station_id`, `date_time`),"
                   "FOREIGN KEY (`station_id`) REFERENCES `charging_stations`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `customers`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`username` VARCHAR(50) NOT NULL, "
                   "`full_name` VARCHAR(50) NOT NULL,"
                   "`email` VARCHAR(50) NOT NULL, "
                   "`phone_number` VARCHAR(20),"
                   "`bank_account` VARCHAR(50) NOT NULL,"
                   "`gps_location` VARCHAR(30) NOT NULL,"
                   "`address` VARCHAR(100) NOT NULL,"
                   "`nearest_station` INTEGER,"
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`nearest_station`) REFERENCES `charging_stations`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `workshops`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`location` VARCHAR(100) NOT NULL, "
                   "`available_timing` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `rent_records`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT,"
                   "`date_from` DATETIME NOT NULL,"
                   "`date_to` DATETIME NOT NULL,"
                   "`cid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`distance` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`cid`) REFERENCES `customers`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `plug_properties`("
                   "`sid` INTEGER NOT NULL, "
                   "`pmodel` VARCHAR(50) NOT NULL, "
                   "`amount` INTEGER NOT NULL, "
                   "PRIMARY KEY (`sid`, `pmodel`),"
                   "FOREIGN KEY (`sid`) REFERENCES `charging_stations`(`id`),"
                   "FOREIGN KEY (`pmodel`) REFERENCES `plugs`(`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_part_properties`("
                   "`wid` INTEGER NOT NULL, "
                   "`trade_name` VARCHAR(50) NOT NULL, "
                   "`pid` INTEGER NOT NULL, "
                   "`amount` INTEGER NOT NULL DEFAULT 1, "
                   "PRIMARY KEY (`wid`, `trade_name`, `pid`),"
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`trade_name`, `pid`) REFERENCES `car_parts`(`trade_name`, `pid`))")

    # cursor.execute("CREATE TABLE IF NOT EXISTS `car_part_properties`("
    #                "`wid` INTEGER NOT NULL, "
    #                "`trade_name` VARCHAR(30) NOT NULL, "
    #                "`amount` INTEGER NOT NULL DEFAULT 1, "
    #                "PRIMARY KEY (`wid`, `trade_name`),"
    #                "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
    #                "FOREIGN KEY (`trade_name`) REFERENCES `car_parts`(`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `orders`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` DATETIME NOT NULL, "
                   "`wid` INTEGER NOT NULL, "
                   "`pid` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`), "
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `order_payment_records`("
                   "`no_of_transaction` INTEGER NOT NULL, "
                   "`date_time` DATETIME NOT NULL, "
                   "`pid` INTEGER NOT NULL,"
                   "`did` INTEGER NOT NULL,"
                   "`oid` INTEGER NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`no_of_transaction`),"
                   "UNIQUE (`oid`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`),"
                   "FOREIGN KEY (`oid`) REFERENCES `orders`(`id`),"
                   "FOREIGN KEY (`did`) REFERENCES `deposits`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `order_details`("
                   "`order_id` INTEGER NOT NULL, "
                   "`trade_name` VARCHAR(50) NOT NULL, "
                   "`pid` INTEGER NOT NULL, "
                   "`amount` INTEGER NOT NULL DEFAULT 1,"
                   "PRIMARY KEY (`order_id`, `trade_name`, `pid`),"
                   "FOREIGN KEY (`trade_name`, `pid`) REFERENCES `car_parts`(`trade_name`, `pid`),"
                   "FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `repair_records`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` DATETIME NOT NULL, "
                   "`wid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charge_records`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` DATETIME NOT NULL, "
                   "`sid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`sid`) REFERENCES `charging_stations`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `payment_records`("
                   "`no_of_transaction` INTEGER NOT NULL, "
                   "`date_time` DATETIME NOT NULL, "
                   "`cid` INTEGER NOT NULL,"
                   "`did` INTEGER NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`no_of_transaction`),"
                   "FOREIGN KEY (`cid`) REFERENCES `customers`(`id`),"
                   "FOREIGN KEY (`did`) REFERENCES `deposits`(`id`))")
    cursor.close()


def load_backup(conn: MySQLConnection):
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE company")
    conn.commit()
    subprocess.call(['./restore_db.sh'])
