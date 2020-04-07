/*
SQLyog Enterprise - MySQL GUI v8.18 
MySQL - 5.7.17 : Database - my_rtc
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`my_rtc` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `my_rtc`;

/*Table structure for table `lim_dict` */

DROP TABLE IF EXISTS `lim_dict`;

CREATE TABLE `lim_dict` (
  `dictionaryid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Sampling_Shop` varchar(50) COLLATE utf8_bin NOT NULL,
  `Sample_Name` varchar(50) COLLATE utf8_bin NOT NULL,
  `Sampling_Area` varchar(50) COLLATE utf8_bin NOT NULL,
  `Sample_ItemAliasName` varchar(50) COLLATE utf8_bin NOT NULL,
  `test_code` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`dictionaryid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `lims_data` */

DROP TABLE IF EXISTS `lims_data`;

CREATE TABLE `lims_data` (
  `dataid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `DICTIONARYID` int(10) unsigned DEFAULT NULL,
  `Sampling_Date` datetime DEFAULT NULL,
  `Sample_TestResult` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`dataid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
