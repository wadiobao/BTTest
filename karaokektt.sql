-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: karaokeltt
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `chi_tiet_su_dung_dv`
--

DROP TABLE IF EXISTS `chi_tiet_su_dung_dv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_su_dung_dv` (
  `MaDatPhong` char(10) NOT NULL,
  `MaDV` char(10) NOT NULL,
  `SoLuong` int DEFAULT NULL,
  PRIMARY KEY (`MaDatPhong`,`MaDV`),
  KEY `fk_MaDV_idx` (`MaDV`),
  CONSTRAINT `fk_MaDatPhong` FOREIGN KEY (`MaDatPhong`) REFERENCES `dat_phong` (`MaDatPhong`),
  CONSTRAINT `fk_MaDV` FOREIGN KEY (`MaDV`) REFERENCES `dich_vu_di_kem` (`MaDV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_su_dung_dv`
--

LOCK TABLES `chi_tiet_su_dung_dv` WRITE;
/*!40000 ALTER TABLE `chi_tiet_su_dung_dv` DISABLE KEYS */;
INSERT INTO `chi_tiet_su_dung_dv` VALUES ('DP0001','DV001',20),('DP0001','DV002',10),('DP0001','DV003',3),('DP0002','DV002',10),('DP0002','DV003',1),('DP0003','DV003',2),('DP0003','DV004',10);
/*!40000 ALTER TABLE `chi_tiet_su_dung_dv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dat_phong`
--

DROP TABLE IF EXISTS `dat_phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dat_phong` (
  `MaDatPhong` char(10) NOT NULL,
  `MaPhong` char(10) NOT NULL,
  `MaKH` char(10) NOT NULL,
  `NgayDat` date DEFAULT NULL,
  `GioBatDau` time DEFAULT NULL,
  `GioKetThuc` time DEFAULT NULL,
  `TienDatCoc` int DEFAULT NULL,
  `GhiChu` varchar(45) DEFAULT NULL,
  `TrangThaiDat` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`MaDatPhong`),
  KEY `MaKH_idx` (`MaKH`),
  KEY `MaPhong_idx` (`MaPhong`),
  CONSTRAINT `fk_MaKH` FOREIGN KEY (`MaKH`) REFERENCES `khach_hang` (`MaKH`),
  CONSTRAINT `fk_MaPhong` FOREIGN KEY (`MaPhong`) REFERENCES `phong` (`MaPhong`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dat_phong`
--

LOCK TABLES `dat_phong` WRITE;
/*!40000 ALTER TABLE `dat_phong` DISABLE KEYS */;
INSERT INTO `dat_phong` VALUES ('DP0001','P0001','KH0002','2018-03-26','11:00:00','13:30:00',100000,'','Da dat'),('DP0002','P0001','KH0003','2018-03-27','17:15:00','19:15:00',50000,NULL,'Da huy'),('DP0003','P0002','KH0002','2018-03-26','20:30:00','22:15:00',100000,'','Da dat'),('DP0004','P0004','KH0001','2018-04-01','19:30:00','21:15:00',200000,'','Da dat');
/*!40000 ALTER TABLE `dat_phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dich_vu_di_kem`
--

DROP TABLE IF EXISTS `dich_vu_di_kem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dich_vu_di_kem` (
  `MaDV` char(10) NOT NULL,
  `TenDV` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DonViTinh` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DonGia` int DEFAULT NULL,
  PRIMARY KEY (`MaDV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dich_vu_di_kem`
--

LOCK TABLES `dich_vu_di_kem` WRITE;
/*!40000 ALTER TABLE `dich_vu_di_kem` DISABLE KEYS */;
INSERT INTO `dich_vu_di_kem` VALUES ('DV001','Beer','lon',10000),('DV002','Nuoc ngot','lon',8000),('DV003','Trai cay','dia',35000),('DV004','Khan uot','cai',2000);
/*!40000 ALTER TABLE `dich_vu_di_kem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khach_hang`
--

DROP TABLE IF EXISTS `khach_hang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khach_hang` (
  `MaKH` char(10) NOT NULL,
  `TenKH` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `DiaChi` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SoDT` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`MaKH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khach_hang`
--

LOCK TABLES `khach_hang` WRITE;
/*!40000 ALTER TABLE `khach_hang` DISABLE KEYS */;
INSERT INTO `khach_hang` VALUES ('KH0001','Nguyen Van A','Hoa xuan','1111111111'),('KH0002','Nguyen Van B','Hoa hai','1111111112'),('KH0003','Phan Van A','Cam Le','1111111113'),('KH0004','Pham Van B','Hoa xuan','1111111114');
/*!40000 ALTER TABLE `khach_hang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phong`
--

DROP TABLE IF EXISTS `phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phong` (
  `MaPhong` char(10) NOT NULL,
  `LoaiPhong` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `SoKhachToiDa` int DEFAULT NULL,
  `GiaPhong` int DEFAULT NULL,
  `MoTa` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`MaPhong`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong`
--

LOCK TABLES `phong` WRITE;
/*!40000 ALTER TABLE `phong` DISABLE KEYS */;
INSERT INTO `phong` VALUES ('P0001','Loai 1',20,60000,''),('P0002','Loai 1',25,80000,''),('P0003','Loai 2',15,50000,''),('P0004','Loai 3',20,50000,'');
/*!40000 ALTER TABLE `phong` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-22 22:19:21
