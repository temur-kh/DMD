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
-- Table structure for table `Car`
--

DROP TABLE IF EXISTS `Car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Car` (
  `plate` varchar(30) NOT NULL,
  `cmodel` varchar(30) NOT NULL,
  `color` varchar(30) NOT NULL,
  PRIMARY KEY (`plate`),
  KEY `cmodel` (`cmodel`),
  CONSTRAINT `Car_ibfk_1` FOREIGN KEY (`cmodel`) REFERENCES `Car_Model` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car`
--

LOCK TABLES `Car` WRITE;
/*!40000 ALTER TABLE `Car` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Car_Model`
--

DROP TABLE IF EXISTS `Car_Model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Car_Model` (
  `model` varchar(30) NOT NULL,
  `rent_price` int(11) NOT NULL,
  `charging_capacity` int(11) NOT NULL,
  PRIMARY KEY (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car_Model`
--

LOCK TABLES `Car_Model` WRITE;
/*!40000 ALTER TABLE `Car_Model` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car_Model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Car_Part`
--

DROP TABLE IF EXISTS `Car_Part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Car_Part` (
  `trade_name` varchar(30) NOT NULL,
  `type` varchar(30) NOT NULL,
  `car_model` varchar(30) NOT NULL,
  PRIMARY KEY (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car_Part`
--

LOCK TABLES `Car_Part` WRITE;
/*!40000 ALTER TABLE `Car_Part` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car_Part` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Car_Part_Price`
--

DROP TABLE IF EXISTS `Car_Part_Price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Car_Part_Price` (
  `trade_name` varchar(30) NOT NULL,
  `pid` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`trade_name`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `Car_Part_Price_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `Provider` (`id`),
  CONSTRAINT `Car_Part_Price_ibfk_2` FOREIGN KEY (`trade_name`) REFERENCES `Car_Part` (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car_Part_Price`
--

LOCK TABLES `Car_Part_Price` WRITE;
/*!40000 ALTER TABLE `Car_Part_Price` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car_Part_Price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Car_Plug`
--

DROP TABLE IF EXISTS `Car_Plug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Car_Plug` (
  `cplate` varchar(30) NOT NULL,
  `pmodel` varchar(30) NOT NULL,
  PRIMARY KEY (`cplate`,`pmodel`),
  KEY `pmodel` (`pmodel`),
  CONSTRAINT `Car_Plug_ibfk_1` FOREIGN KEY (`cplate`) REFERENCES `Car` (`plate`),
  CONSTRAINT `Car_Plug_ibfk_2` FOREIGN KEY (`pmodel`) REFERENCES `Plug` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Car_Plug`
--

LOCK TABLES `Car_Plug` WRITE;
/*!40000 ALTER TABLE `Car_Plug` DISABLE KEYS */;
/*!40000 ALTER TABLE `Car_Plug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Charge_Record`
--

DROP TABLE IF EXISTS `Charge_Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Charge_Record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `sid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `price` int(11) NOT NULL DEFAULT '1000',
  PRIMARY KEY (`id`),
  KEY `sid` (`sid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `Charge_Record_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `Charging_Station` (`id`),
  CONSTRAINT `Charge_Record_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `Car` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Charge_Record`
--

LOCK TABLES `Charge_Record` WRITE;
/*!40000 ALTER TABLE `Charge_Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Charge_Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Charging_Station`
--

DROP TABLE IF EXISTS `Charging_Station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Charging_Station` (
  `id` int(11) NOT NULL,
  `GPS_location` varchar(30) NOT NULL,
  `price_per_charge` int(11) NOT NULL,
  `no_available_sockets` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Charging_Station`
--

LOCK TABLES `Charging_Station` WRITE;
/*!40000 ALTER TABLE `Charging_Station` DISABLE KEYS */;
/*!40000 ALTER TABLE `Charging_Station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Customer` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `full_name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `bank_account` int(11) NOT NULL,
  `GPS_Location` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `sid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sid` (`sid`),
  CONSTRAINT `Customer_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `Charging_Station` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Deposit`
--

DROP TABLE IF EXISTS `Deposit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Deposit` (
  `id` int(11) NOT NULL,
  `bank_account` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Deposit`
--

LOCK TABLES `Deposit` WRITE;
/*!40000 ALTER TABLE `Deposit` DISABLE KEYS */;
/*!40000 ALTER TABLE `Deposit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order`
--

DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `trade_name` varchar(30) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '1',
  `wid` int(11) NOT NULL,
  `no_of_transaction` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trade_name` (`trade_name`),
  KEY `wid` (`wid`),
  KEY `pid` (`pid`),
  CONSTRAINT `Order_ibfk_1` FOREIGN KEY (`trade_name`) REFERENCES `Car_Part` (`trade_name`),
  CONSTRAINT `Order_ibfk_2` FOREIGN KEY (`wid`) REFERENCES `Workshop` (`id`),
  CONSTRAINT `Order_ibfk_3` FOREIGN KEY (`pid`) REFERENCES `Provider` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order`
--

LOCK TABLES `Order` WRITE;
/*!40000 ALTER TABLE `Order` DISABLE KEYS */;
/*!40000 ALTER TABLE `Order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_Payment_Record`
--

DROP TABLE IF EXISTS `Order_Payment_Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Order_Payment_Record` (
  `no_of_transaction` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `pid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  `price` int(11) NOT NULL DEFAULT '5000',
  PRIMARY KEY (`no_of_transaction`),
  KEY `pid` (`pid`),
  KEY `did` (`did`),
  CONSTRAINT `Order_Payment_Record_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `Provider` (`id`),
  CONSTRAINT `Order_Payment_Record_ibfk_2` FOREIGN KEY (`did`) REFERENCES `Deposit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_Payment_Record`
--

LOCK TABLES `Order_Payment_Record` WRITE;
/*!40000 ALTER TABLE `Order_Payment_Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Order_Payment_Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Payment_Record`
--

DROP TABLE IF EXISTS `Payment_Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Payment_Record` (
  `no_of_transaction` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `cid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  `price` int(11) NOT NULL DEFAULT '200',
  PRIMARY KEY (`no_of_transaction`),
  KEY `cid` (`cid`),
  KEY `did` (`did`),
  CONSTRAINT `Payment_Record_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `Customer` (`id`),
  CONSTRAINT `Payment_Record_ibfk_2` FOREIGN KEY (`did`) REFERENCES `Deposit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Payment_Record`
--

LOCK TABLES `Payment_Record` WRITE;
/*!40000 ALTER TABLE `Payment_Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Payment_Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Plug`
--

DROP TABLE IF EXISTS `Plug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Plug` (
  `model` varchar(30) NOT NULL,
  `shape` varchar(30) NOT NULL,
  `size` int(11) NOT NULL,
  `charging_speed` int(11) NOT NULL,
  PRIMARY KEY (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Plug`
--

LOCK TABLES `Plug` WRITE;
/*!40000 ALTER TABLE `Plug` DISABLE KEYS */;
/*!40000 ALTER TABLE `Plug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Provider`
--

DROP TABLE IF EXISTS `Provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Provider` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `address` varchar(30) DEFAULT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `bank_account` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Provider`
--

LOCK TABLES `Provider` WRITE;
/*!40000 ALTER TABLE `Provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `Provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rent_Record`
--

DROP TABLE IF EXISTS `Rent_Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Rent_Record` (
  `id` int(11) NOT NULL,
  `date_from` timestamp NOT NULL,
  `date_to` timestamp NOT NULL,
  `cid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `distance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cid` (`cid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `Rent_Record_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `Customer` (`id`),
  CONSTRAINT `Rent_Record_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `Car` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rent_Record`
--

LOCK TABLES `Rent_Record` WRITE;
/*!40000 ALTER TABLE `Rent_Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Rent_Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Repair_Record`
--

DROP TABLE IF EXISTS `Repair_Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Repair_Record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` timestamp NOT NULL,
  `wid` int(11) NOT NULL,
  `cplate` varchar(30) NOT NULL,
  `cost` int(11) NOT NULL DEFAULT '1000',
  PRIMARY KEY (`id`),
  KEY `wid` (`wid`),
  KEY `cplate` (`cplate`),
  CONSTRAINT `Repair_Record_ibfk_1` FOREIGN KEY (`wid`) REFERENCES `Workshop` (`id`),
  CONSTRAINT `Repair_Record_ibfk_2` FOREIGN KEY (`cplate`) REFERENCES `Car` (`plate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Repair_Record`
--

LOCK TABLES `Repair_Record` WRITE;
/*!40000 ALTER TABLE `Repair_Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Repair_Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Workshop`
--

DROP TABLE IF EXISTS `Workshop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Workshop` (
  `id` int(11) NOT NULL,
  `location` varchar(30) NOT NULL,
  `available_timing` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Workshop`
--

LOCK TABLES `Workshop` WRITE;
/*!40000 ALTER TABLE `Workshop` DISABLE KEYS */;
/*!40000 ALTER TABLE `Workshop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `has_car_part`
--

DROP TABLE IF EXISTS `has_car_part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `has_car_part` (
  `wid` int(11) NOT NULL,
  `trade_name` varchar(30) NOT NULL,
  `amount` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`wid`,`trade_name`),
  KEY `trade_name` (`trade_name`),
  CONSTRAINT `has_car_part_ibfk_1` FOREIGN KEY (`wid`) REFERENCES `Workshop` (`id`),
  CONSTRAINT `has_car_part_ibfk_2` FOREIGN KEY (`trade_name`) REFERENCES `Car_Part` (`trade_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `has_car_part`
--

LOCK TABLES `has_car_part` WRITE;
/*!40000 ALTER TABLE `has_car_part` DISABLE KEYS */;
/*!40000 ALTER TABLE `has_car_part` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `has_plug`
--

DROP TABLE IF EXISTS `has_plug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `has_plug` (
  `sid` int(11) NOT NULL,
  `pmodel` varchar(30) NOT NULL,
  PRIMARY KEY (`sid`,`pmodel`),
  KEY `pmodel` (`pmodel`),
  CONSTRAINT `has_plug_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `Charging_Station` (`id`),
  CONSTRAINT `has_plug_ibfk_2` FOREIGN KEY (`pmodel`) REFERENCES `Plug` (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `has_plug`
--

LOCK TABLES `has_plug` WRITE;
/*!40000 ALTER TABLE `has_plug` DISABLE KEYS */;
/*!40000 ALTER TABLE `has_plug` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-12 22:16:22
