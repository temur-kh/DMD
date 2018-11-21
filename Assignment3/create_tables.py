def create_database(db):
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `company`")
    cursor.execute("USE `company`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `plugs`("
                   "`model` VARCHAR(30) NOT NULL, "
                   "`shape` VARCHAR(30) NOT NULL, "
                   "`size` INTEGER NOT NULL,"
                   "`charging_speed` INTEGER NOT NULL, "
                   "PRIMARY KEY (`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_models`("
                   "`model` VARCHAR(30) NOT NULL, "
                   "`rent_price` INTEGER NOT NULL,"
                   "`charging_capacity` INTEGER NOT NULL, "
                   "`pmodel` VARCHAR(30) NOT NULL,"
                   "PRIMARY KEY (`model`),"
                   "FOREIGN KEY (`pmodel`) REFERENCES `plugs`(`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `cars`("
                   "`plate` VARCHAR(30) NOT NULL, "
                   "`cmodel` VARCHAR(30) NOT NULL, "
                   "`color` VARCHAR(30) NOT NULL, "
                   "PRIMARY KEY (`plate`),"
                   "FOREIGN KEY (`cmodel`) REFERENCES `car_models`(`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_parts`("
                   "`trade_name` VARCHAR(30) NOT NULL, "
                   "`type` VARCHAR(30) NOT NULL, "
                   "`car_model` VARCHAR(30) NOT NULL, "
                   "PRIMARY KEY (`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `providers`("
                   "`id` INTEGER NOT NULL, "
                   "`name` VARCHAR(30) NOT NULL, "
                   "`address` VARCHAR(30), "
                   "`phone_number` VARCHAR(10),"
                   "`bank_account` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_part_prices`("
                   "`trade_name` VARCHAR(30) NOT NULL, "
                   "`pid` INTEGER NOT NULL, "
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`trade_name`, `pid`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`),"
                   "FOREIGN KEY (`trade_name`) REFERENCES `car_parts`(`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `deposits`("
                   "`id` INTEGER NOT NULL, "
                   "`bank_account`INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charging_stations`("
                   "`id` INTEGER NOT NULL, "
                   "`gps_location` VARCHAR(30) NOT NULL, "  # not sure it 30 will be enough, need to check it
                   "`price_per_charge` INTEGER NOT NULL, "
                   "`total_no_of_sockets` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charging_station_sockets`("
                   "`station_id` INTEGER NOT NULL,"
                   "`no_of_available_sockets` INTEGER NOT NULL,"
                   "`date_time` TIMESTAMP NOT NULL,"
                   "PRIMARY KEY (`station_id`),"
                   "FOREIGN KEY (`station_id`) REFERENCES `charging_stations`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `customers`("
                   "`id` INTEGER NOT NULL, "
                   "`username` VARCHAR(30) NOT NULL, "
                   "`full_name` VARCHAR(30) NOT NULL,"
                   "`email` VARCHAR(30) NOT NULL, "
                   "`phone_number` VARCHAR(10),"
                   "`bank_account` INTEGER NOT NULL,"
                   "`gps_location` VARCHAR(30) NOT NULL,"  # ?
                   "`address` VARCHAR(50) NOT NULL,"
                   "`nearest_station` INTEGER,"
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`nearest_station`) REFERENCES `charging_stations`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `workshops`("
                   "`id` INTEGER NOT NULL, "
                   "`location` VARCHAR(30) NOT NULL, "
                   "`available_timing` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `rent_records`("
                   "`id` INTEGER NOT NULL,"
                   "`date_from` TIMESTAMP NOT NULL,"
                   "`date_to` TIMESTAMP NOT NULL,"
                   "`cid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`distance` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`cid`) REFERENCES `customers`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `plug_properties`("
                   "`sid` INTEGER NOT NULL, "
                   "`pmodel` VARCHAR(30) NOT NULL, "
                   "PRIMARY KEY (`sid`, `pmodel`),"
                   "FOREIGN KEY (`sid`) REFERENCES `charging_stations`(`id`),"
                   "FOREIGN KEY (`pmodel`) REFERENCES `plugs`(`model`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `car_part_properties`("
                   "`wid` INTEGER NOT NULL, "
                   "`trade_name` VARCHAR(30) NOT NULL, "
                   "`amount` INTEGER NOT NULL DEFAULT 1, "
                   "PRIMARY KEY (`wid`, `trade_name`),"
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`trade_name`) REFERENCES `car_parts`(`trade_name`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `orders`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` TIMESTAMP NOT NULL, "
                   "`wid` INTEGER NOT NULL,"
                   "`no_of_transaction` INTEGER NOT NULL,"
                   "`pid` INTEGER NOT NULL,"
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `order_details`("
                   "`order_id` INTEGER NOT NULL, "
                   "`trade_name` VARCHAR(30) NOT NULL, "
                   "`amount` INTEGER NOT NULL DEFAULT 1,"
                   "PRIMARY KEY (`order_id`, `trade_name`),"
                   "FOREIGN KEY (`trade_name`) REFERENCES `car_parts`(`trade_name`),"
                   "FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `repair_records`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` TIMESTAMP NOT NULL, "
                   "`wid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`cost` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`wid`) REFERENCES `workshops`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `charge_records`("
                   "`id` INTEGER NOT NULL AUTO_INCREMENT, "
                   "`date_time` TIMESTAMP NOT NULL, "
                   "`sid` INTEGER NOT NULL,"
                   "`cplate` VARCHAR(30) NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`id`),"
                   "FOREIGN KEY (`sid`) REFERENCES `charging_stations`(`id`),"
                   "FOREIGN KEY (`cplate`) REFERENCES `cars`(`plate`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `payment_records`("
                   "`no_of_transaction` INTEGER NOT NULL, "
                   "`date_time` TIMESTAMP NOT NULL, "
                   "`cid` INTEGER NOT NULL,"
                   "`did` INTEGER NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`no_of_transaction`),"
                   "FOREIGN KEY (`cid`) REFERENCES `customers`(`id`),"
                   "FOREIGN KEY (`did`) REFERENCES `deposits`(`id`))")

    cursor.execute("CREATE TABLE IF NOT EXISTS `order_payment_records`("
                   "`no_of_transaction` INTEGER NOT NULL, "
                   "`date_time` TIMESTAMP NOT NULL, "
                   "`pid` INTEGER NOT NULL,"
                   "`did` INTEGER NOT NULL,"
                   "`price` INTEGER NOT NULL, "
                   "PRIMARY KEY (`no_of_transaction`),"
                   "FOREIGN KEY (`pid`) REFERENCES `providers`(`id`),"
                   "FOREIGN KEY (`did`) REFERENCES `deposits`(`id`))")
    cursor.close()
