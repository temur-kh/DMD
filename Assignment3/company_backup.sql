-- MySQL dump 10.13  Distrib 8.0.13, for Linux (x86_64)
--
-- Host: localhost    Database: company
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `car_models`
--

DROP TABLE IF EXISTS `car_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `car_models` (
  `model` varchar(30) NOT NULL,
  `rent_price` int(11) NOT NULL,
  `charging_capacity` int(11) NOT NULL,
  `pmodel` varchar(30) NOT NULL,
  PRIMARY KEY (`model`),
  KEY `pmodel` (`pmodel`),
  CONSTRAINT `car_models_ibfk_1` FOREIGN KEY (`pmodel`) REFERENCES `plugs` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_models`
--

LOCK TABLES `car_models` WRITE;
/*!40000 ALTER TABLE `car_models` DISABLE KEYS */;
/*!40000 ALTER TABLE `car_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_part_prices`
--

DROP TABLE IF EXISTS `car_part_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `car_part_prices` (
  `trade_name` varchar(30) NOT NULL,
  `pid` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`trade_name`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `car_part_prices_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `providers` (`id`),
  CONSTRAINT `car_part_prices_ibfk_2` FOREIGN KEY (`trade_name`) REFERENCES `car_parts` (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_part_prices`
--

LOCK TABLES `car_part_prices` WRITE;
/*!40000 ALTER TABLE `car_part_prices` DISABLE KEYS */;
/*!40000 ALTER TABLE `car_part_prices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_part_properties`
--

DROP TABLE IF EXISTS `car_part_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `car_part_properties` (
  `wid` int(11) NOT NULL,
  `trade_name` varchar(30) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`wid`,`trade_name`),
  KEY `trade_name` (`trade_name`),
  CONSTRAINT `car_part_properties_ibfk_1` FOREIGN KEY (`wid`) REFERENCES `workshops` (`id`),
  CONSTRAINT `car_part_properties_ibfk_2` FOREIGN KEY (`trade_name`) REFERENCES `car_parts` (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_part_properties`
--

LOCK TABLES `car_part_properties` WRITE;
/*!40000 ALTER TABLE `car_part_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `car_part_properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_parts`
--

DROP TABLE IF EXISTS `car_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `car_parts` (
  `trade_name` varchar(30) NOT NULL,
  `type` varchar(30) NOT NULL,
  `car_model` varchar(30) NOT NULL,
  PRIMARY KEY (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_parts`
--

LOCK TABLES `car_parts` WRITE;
/*!40000 ALTER TABLE `car_parts` DISABLE KEYS */;
/*!40000 ALTER TABLE `car_parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `cars` (
  `plate` varchar(30) NOT NULL,
  `cmodel` varchar(30) NOT NULL,
  `color` varchar(30) NOT NULL,
  PRIMARY KEY (`plate`),
  KEY `cmodel` (`cmodel`),
  CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`cmodel`) REFERENCES `car_models` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charge_records`
--

DROP TABLE IF EXISTS `charge_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charge_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `sid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sid` (`sid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `charge_records_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `charging_stations` (`id`),
  CONSTRAINT `charge_records_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `cars` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charge_records`
--

LOCK TABLES `charge_records` WRITE;
/*!40000 ALTER TABLE `charge_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `charge_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charging_station_sockets`
--

DROP TABLE IF EXISTS `charging_station_sockets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charging_station_sockets` (
  `station_id` int(11) NOT NULL,
  `no_of_available_sockets` int(11) NOT NULL,
  `date_time` timestamp NOT NULL,
  PRIMARY KEY (`station_id`),
  CONSTRAINT `charging_station_sockets_ibfk_1` FOREIGN KEY (`station_id`) REFERENCES `charging_stations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_station_sockets`
--

LOCK TABLES `charging_station_sockets` WRITE;
/*!40000 ALTER TABLE `charging_station_sockets` DISABLE KEYS */;
/*!40000 ALTER TABLE `charging_station_sockets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charging_stations`
--

DROP TABLE IF EXISTS `charging_stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charging_stations` (
  `id` int(11) NOT NULL,
  `GPS_location` varchar(30) NOT NULL,
  `price_per_charge` int(11) NOT NULL,
  `total_no_of_sockets` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_stations`
--

LOCK TABLES `charging_stations` WRITE;
/*!40000 ALTER TABLE `charging_stations` DISABLE KEYS */;
/*!40000 ALTER TABLE `charging_stations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `full_name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `bank_account` int(11) NOT NULL,
  `GPS_Location` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `nearest_station` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `nearest_station` (`nearest_station`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`nearest_station`) REFERENCES `charging_stations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deposits`
--

DROP TABLE IF EXISTS `deposits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `deposits` (
  `id` int(11) NOT NULL,
  `bank_account` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deposits`
--

LOCK TABLES `deposits` WRITE;
/*!40000 ALTER TABLE `deposits` DISABLE KEYS */;
/*!40000 ALTER TABLE `deposits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `order_details` (
  `order_id` int(11) NOT NULL,
  `trade_name` varchar(30) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`order_id`,`trade_name`),
  KEY `trade_name` (`trade_name`),
  CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`trade_name`) REFERENCES `car_parts` (`trade_name`),
  CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_payment_records`
--

DROP TABLE IF EXISTS `order_payment_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `order_payment_records` (
  `no_of_transaction` int(11) NOT NULL,
  `date_time` timestamp NOT NULL,
  `pid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`no_of_transaction`),
  KEY `pid` (`pid`),
  KEY `did` (`did`),
  CONSTRAINT `order_payment_records_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `providers` (`id`),
  CONSTRAINT `order_payment_records_ibfk_2` FOREIGN KEY (`did`) REFERENCES `deposits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_payment_records`
--

LOCK TABLES `order_payment_records` WRITE;
/*!40000 ALTER TABLE `order_payment_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_payment_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `wid` int(11) NOT NULL,
  `no_of_transaction` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wid` (`wid`),
  KEY `pid` (`pid`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`wid`) REFERENCES `workshops` (`id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `providers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_records`
--

DROP TABLE IF EXISTS `payment_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `payment_records` (
  `no_of_transaction` int(11) NOT NULL,
  `date_time` timestamp NOT NULL,
  `cid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`no_of_transaction`),
  KEY `cid` (`cid`),
  KEY `did` (`did`),
  CONSTRAINT `payment_records_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customers` (`id`),
  CONSTRAINT `payment_records_ibfk_2` FOREIGN KEY (`did`) REFERENCES `deposits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_records`
--

LOCK TABLES `payment_records` WRITE;
/*!40000 ALTER TABLE `payment_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plug_properties`
--

DROP TABLE IF EXISTS `plug_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `plug_properties` (
  `sid` int(11) NOT NULL,
  `pmodel` varchar(30) NOT NULL,
  PRIMARY KEY (`sid`,`pmodel`),
  KEY `pmodel` (`pmodel`),
  CONSTRAINT `plug_properties_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `charging_stations` (`id`),
  CONSTRAINT `plug_properties_ibfk_2` FOREIGN KEY (`pmodel`) REFERENCES `plugs` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plug_properties`
--

LOCK TABLES `plug_properties` WRITE;
/*!40000 ALTER TABLE `plug_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `plug_properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plugs`
--

DROP TABLE IF EXISTS `plugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `plugs` (
  `model` varchar(30) NOT NULL,
  `shape` varchar(30) NOT NULL,
  `size` int(11) NOT NULL,
  `charging_speed` int(11) NOT NULL,
  PRIMARY KEY (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plugs`
--

LOCK TABLES `plugs` WRITE;
/*!40000 ALTER TABLE `plugs` DISABLE KEYS */;
/*!40000 ALTER TABLE `plugs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `providers`
--

DROP TABLE IF EXISTS `providers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `providers` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `address` varchar(30) DEFAULT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `bank_account` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `providers`
--

LOCK TABLES `providers` WRITE;
/*!40000 ALTER TABLE `providers` DISABLE KEYS */;
/*!40000 ALTER TABLE `providers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rent_records`
--

DROP TABLE IF EXISTS `rent_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rent_records` (
  `id` int(11) NOT NULL,
  `date_from` timestamp NOT NULL,
  `date_to` timestamp NOT NULL,
  `cid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `distance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cid` (`cid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `rent_records_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customers` (`id`),
  CONSTRAINT `rent_records_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `cars` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rent_records`
--

LOCK TABLES `rent_records` WRITE;
/*!40000 ALTER TABLE `rent_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `rent_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_records`
--

DROP TABLE IF EXISTS `repair_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `repair_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `wid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `cost` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wid` (`wid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `repair_records_ibfk_1` FOREIGN KEY (`wid`) REFERENCES `workshops` (`id`),
  CONSTRAINT `repair_records_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `cars` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_records`
--

LOCK TABLES `repair_records` WRITE;
/*!40000 ALTER TABLE `repair_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshops`
--

DROP TABLE IF EXISTS `workshops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `workshops` (
  `id` int(11) NOT NULL,
  `location` varchar(30) NOT NULL,
  `available_timing` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshops`
--

LOCK TABLES `workshops` WRITE;
/*!40000 ALTER TABLE `workshops` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshops` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-13 18:33:13
