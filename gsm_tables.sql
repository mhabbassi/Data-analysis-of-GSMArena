-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: gsm
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `battery`
--

DROP TABLE IF EXISTS `battery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `battery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL,
  `capacity` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand_id` int DEFAULT NULL,
  `os_id` int DEFAULT NULL,
  `battery_id` int DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `network_technology` varchar(8) DEFAULT NULL,
  `network_types` varchar(256) DEFAULT NULL,
  `sensors_count` varchar(8) DEFAULT NULL,
  `sensors_types` varchar(512) DEFAULT NULL,
  `length` varchar(16) DEFAULT NULL,
  `width` varchar(16) DEFAULT NULL,
  `height` varchar(16) DEFAULT NULL,
  `weight` varchar(16) DEFAULT NULL,
  `resolution_l` varchar(16) DEFAULT NULL,
  `resolution_w` varchar(16) DEFAULT NULL,
  `screen_body_ratio` varchar(16) DEFAULT NULL,
  `screen_size` varchar(16) DEFAULT NULL,
  `ppi` varchar(16) DEFAULT NULL,
  `sim_type` varchar(16) DEFAULT NULL,
  `sim_count` int DEFAULT NULL,
  `released_date` varchar(16) DEFAULT NULL,
  `cpu_core` varchar(16) DEFAULT NULL,
  `fan_count` varchar(16) DEFAULT NULL,
  `view_count` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_device_brand_id` (`brand_id`),
  KEY `fk_device_os_id` (`os_id`),
  KEY `fk_device_battery_id` (`battery_id`),
  CONSTRAINT `fk_device_battery_id` FOREIGN KEY (`battery_id`) REFERENCES `battery` (`id`),
  CONSTRAINT `fk_device_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  CONSTRAINT `fk_device_os_id` FOREIGN KEY (`os_id`) REFERENCES `os` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=410 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device_memory_price`
--

DROP TABLE IF EXISTS `device_memory_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_memory_price` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` int DEFAULT NULL,
  `ram` varchar(16) DEFAULT NULL,
  `internal_storage` varchar(16) DEFAULT NULL,
  `price` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_dmp_device_id` (`device_id`),
  CONSTRAINT `fk_dmp_device_id` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=386 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device_temp`
--

DROP TABLE IF EXISTS `device_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_temp` (
  `id` int NOT NULL DEFAULT '0',
  `brand` varchar(16) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `network_technology` varchar(8) DEFAULT NULL,
  `length` varchar(16) DEFAULT NULL,
  `width` varchar(16) DEFAULT NULL,
  `height` varchar(16) DEFAULT NULL,
  `weight` varchar(16) DEFAULT NULL,
  `resolution_l` varchar(16) DEFAULT NULL,
  `resolution_w` varchar(16) DEFAULT NULL,
  `screen_body_ratio` varchar(16) DEFAULT NULL,
  `screen_size` varchar(16) DEFAULT NULL,
  `ppi` varchar(16) DEFAULT NULL,
  `battery_type` varchar(32) DEFAULT NULL,
  `battery_capacity` varchar(16) DEFAULT NULL,
  `sim_type` varchar(16) DEFAULT NULL,
  `sim_count` int DEFAULT NULL,
  `os_type` varchar(128) DEFAULT NULL,
  `os_version` varchar(16) DEFAULT NULL,
  `price` varchar(128) DEFAULT NULL,
  `released_date` varchar(16) DEFAULT NULL,
  `cpu_core` varchar(16) DEFAULT NULL,
  `ram` varchar(16) DEFAULT NULL,
  `internal_storage` varchar(16) DEFAULT NULL,
  `fan_count` varchar(16) DEFAULT NULL,
  `view_count` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `link_status`
--

DROP TABLE IF EXISTS `link_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `link_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(128) DEFAULT NULL,
  `type` varchar(16) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_link_status_url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=6033 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `os`
--

DROP TABLE IF EXISTS `os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `os` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(128) DEFAULT NULL,
  `version` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `raw_content`
--

DROP TABLE IF EXISTS `raw_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand` varchar(128) DEFAULT NULL,
  `type` varchar(16) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `content` longtext,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_raw_content_url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=5907 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-18 20:42:26
