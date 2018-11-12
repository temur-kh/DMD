import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test",
    database="company"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `Car_Model`(" # Car_Model table 
               "`model` VARCHAR(30) NOT NULL, "
               "`rent_price` INTEGER NOT NULL,"
               "`charging_capacity` INTEGER NOT NULL, "
               "PRIMARY KEY (`model`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Car`("
               "`plate` VARCHAR(30) NOT NULL, "
               "`cmodel` VARCHAR(30) NOT NULL, "
               "`color` VARCHAR(30) NOT NULL, "
               "PRIMARY KEY (`plate`),"
               "FOREIGN KEY (`cmodel`) REFERENCES `Car_Model`(`model`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Car_Part`("
               "`trade_name` VARCHAR(30) NOT NULL, "
               "`type` VARCHAR(30) NOT NULL, "
               "`car_model` VARCHAR(30) NOT NULL, "
               "PRIMARY KEY (`trade_name`))");

cursor.execute("CREATE TABLE IF NOT EXISTS `Provider`("
               "`id` INTEGER NOT NULL, "
               "`name` VARCHAR(30) NOT NULL, "
               "`address` VARCHAR(30), "
               "`phone_number` VARCHAR(10),"
               "`bank_account` INTEGER NOT NULL,"
               "PRIMARY KEY (`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Car_Part_Price`("
               "`trade_name` VARCHAR(30) NOT NULL, "
               "`pid` INTEGER NOT NULL, "
               "`price` INTEGER NOT NULL, "
               "PRIMARY KEY (`trade_name`, `pid`),"
               "FOREIGN KEY (`pid`) REFERENCES `Provider`(`id`),"
               "FOREIGN KEY (`trade_name`) REFERENCES `Car_Part`(`trade_name`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Deposit`("
               "`id` INTEGER NOT NULL, "
               "`bank_account`INTEGER NOT NULL, "
               "PRIMARY KEY (`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Charging_Station`("
               "`id` INTEGER NOT NULL, "
               "`GPS_location` VARCHAR(30) NOT NULL, "
               "`price_per_charge` INTEGER NOT NULL, "
               "`no_available_sockets` INTEGER NOT NULL,"
               "PRIMARY KEY (`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Customer`("
               "`id` INTEGER NOT NULL, "
               "`username` VARCHAR(30) NOT NULL, "
               "`full_name` VARCHAR(30) NOT NULL,"
               "`email` VARCHAR(30) NOT NULL, "
               "`phone_number` VARCHAR(10),"
               "`bank_account` INTEGER NOT NULL,"
               "`GPS_Location` VARCHAR(30) NOT NULL,"
               "`address` VARCHAR(50) NOT NULL,"
               "`sid` INTEGER,"
               "PRIMARY KEY (`id`),"
               "FOREIGN KEY (`sid`) REFERENCES `Charging_Station`(`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Workshop`("
               "`id` INTEGER NOT NULL, "
               "`location` VARCHAR(30) NOT NULL, "
               "`available_timing` VARCHAR(30) NOT NULL, "                       #-----------------??????????
               "PRIMARY KEY (`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Plug`("
               "`model` VARCHAR(30) NOT NULL, "
               "`shape` VARCHAR(30) NOT NULL, "
               "`size` INTEGER NOT NULL,"
               "`charging_speed` INTEGER NOT NULL, "
               "PRIMARY KEY (`model`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Car_Plug`("
               "`cplate` VARCHAR(30) NOT NULL, "
               "`pmodel` VARCHAR(30) NOT NULL, "
               "PRIMARY KEY (`cplate`, `pmodel`),"
               "FOREIGN KEY (`cplate`) REFERENCES `Car`(`plate`),"
               "FOREIGN KEY (`pmodel`) REFERENCES `Plug`(`model`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Rent_Record`("
               "`id` INTEGER NOT NULL, "
               "`date_from` TIMESTAMP NOT NULL, "
               "`date_to` TIMESTAMP NOT NULL, "
               "`cid` INTEGER NOT NULL,"
               "`cplate` VARCHAR(30) NOT NULL,"
               "`distance` INTEGER NOT NULL,"
               "PRIMARY KEY (`id`),"
               "FOREIGN KEY (`cid`) REFERENCES `Customer`(`id`),"
               "FOREIGN KEY (`cplate`) REFERENCES `Car`(`plate`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `has_plug`("
               "`sid` INTEGER NOT NULL, "
               "`pmodel` VARCHAR(30) NOT NULL, "
               "PRIMARY KEY (`sid`, `pmodel`),"
               "FOREIGN KEY (`sid`) REFERENCES `Charging_Station`(`id`),"
               "FOREIGN KEY (`pmodel`) REFERENCES `Plug`(`model`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `has_car_part`("
               "`wid` INTEGER NOT NULL, "
               "`trade_name` VARCHAR(30) NOT NULL, "
               "`amount` INTEGER NOT NULL DEFAULT 1, "
               "PRIMARY KEY (`wid`, `trade_name`),"
               "FOREIGN KEY (`wid`) REFERENCES `Workshop`(`id`),"
               "FOREIGN KEY (`trade_name`) REFERENCES `Car_Part`(`trade_name`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Order`("
               "`id` INTEGER NOT NULL AUTO_INCREMENT, "
               "`date_time` TIMESTAMP NOT NULL, "
               "`trade_name` VARCHAR(30) NOT NULL, "
               "`amount` INTEGER NOT NULL DEFAULT 1,"
               "`wid` INTEGER NOT NULL,"
               "`no_of_transaction` INTEGER NOT NULL,"
               "`pid` INTEGER NOT NULL,"
               "PRIMARY KEY (`id`),"
               "FOREIGN KEY (`trade_name`) REFERENCES `Car_Part`(`trade_name`),"
               "FOREIGN KEY (`wid`) REFERENCES `Workshop`(`id`),"
               "FOREIGN KEY (`pid`) REFERENCES `Provider`(`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Repair_Record`("
               "`id` INTEGER NOT NULL AUTO_INCREMENT, "
               "`date_time` TIMESTAMP NOT NULL, "
               "`wid` INTEGER NOT NULL,"
               "`cplate` VARCHAR(30) NOT NULL,"
               "`cost` INTEGER NOT NULL DEFAULT 1000, "
               "PRIMARY KEY (`id`),"
               "FOREIGN KEY (`wid`) REFERENCES `Workshop`(`id`),"
               "FOREIGN KEY (`cplate`) REFERENCES `Car`(`plate`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Charge_Record`("
               "`id` INTEGER NOT NULL AUTO_INCREMENT, "
               "`date_time` TIMESTAMP NOT NULL, "
               "`sid` INTEGER NOT NULL,"
               "`cplate` VARCHAR(30) NOT NULL,"
               "`price` INTEGER NOT NULL DEFAULT 1000, "
               "PRIMARY KEY (`id`),"
               "FOREIGN KEY (`sid`) REFERENCES `Charging_Station`(`id`),"
               "FOREIGN KEY (`cplate`) REFERENCES `Car`(`plate`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Payment_Record`("
               "`no_of_transaction` INTEGER NOT NULL AUTO_INCREMENT, "
               "`date_time` TIMESTAMP NOT NULL, "
               "`cid` INTEGER NOT NULL,"
               "`did` INTEGER NOT NULL,"
               "`price` INTEGER NOT NULL DEFAULT 200, "
               "PRIMARY KEY (`no_of_transaction`),"
               "FOREIGN KEY (`cid`) REFERENCES `Customer`(`id`),"
               "FOREIGN KEY (`did`) REFERENCES `Deposit`(`id`))")

cursor.execute("CREATE TABLE IF NOT EXISTS `Order_Payment_Record`("
               "`no_of_transaction` INTEGER NOT NULL AUTO_INCREMENT, "
               "`date_time` TIMESTAMP NOT NULL, "
               "`pid` INTEGER NOT NULL,"
               "`did` INTEGER NOT NULL,"
               "`price` INTEGER NOT NULL DEFAULT 5000, "
               "PRIMARY KEY (`no_of_transaction`),"
               "FOREIGN KEY (`pid`) REFERENCES `Provider`(`id`),"
               "FOREIGN KEY (`did`) REFERENCES `Deposit`(`id`))")



cursor.execute("SHOW TABLES");