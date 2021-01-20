/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE DATABASE /*!32312 IF NOT EXISTS*/ `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `mydb`;
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) NOT NULL,
  `Password` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Surname` varchar(45) NOT NULL,
  `RoleID` int NOT NULL,
  `BranchID` int NOT NULL,
  `TeamID` int DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserID_UNIQUE` (`UserID`),
  UNIQUE KEY `UserName_UNIQUE` (`UserName`),
  KEY `BranchID_idx` (`BranchID`),
  KEY `RoleID_idx` (`RoleID`),
  CONSTRAINT `BranchID` FOREIGN KEY (`BranchID`) REFERENCES `branches` (`BranchID`),
  CONSTRAINT `RoleID` FOREIGN KEY (`RoleID`) REFERENCES `roles` (`RoleID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `branches`;
CREATE TABLE `branches` (
  `BranchID` int NOT NULL AUTO_INCREMENT,
  `BranchName` varchar(45) NOT NULL,
  PRIMARY KEY (`BranchID`),
  UNIQUE KEY `BranchID_UNIQUE` (`BranchID`),
  UNIQUE KEY `BranchName_UNIQUE` (`BranchName`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `feats`;
CREATE TABLE `feats` (
  `FeatID` int NOT NULL AUTO_INCREMENT,
  `FeatName` varchar(45) NOT NULL,
  `Value` int NOT NULL,
  `Repetiton` int NOT NULL,
  `SessionID` int NOT NULL,
  PRIMARY KEY (`FeatID`),
  UNIQUE KEY `FeatID_UNIQUE` (`FeatID`),
  KEY `SessionID_idx` (`SessionID`),
  CONSTRAINT `SessionID` FOREIGN KEY (`SessionID`) REFERENCES `sessions` (`SessionID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `physicalstats`;
CREATE TABLE `physicalstats` (
  `UserID` int NOT NULL,
  `StatDate` datetime NOT NULL,
  `Height` int NOT NULL,
  `Weight` int NOT NULL,
  `FatPercantage` int NOT NULL,
  `CaloricIntake` int NOT NULL,
  `Comment` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`UserID`,`StatDate`),
  CONSTRAINT `UserID3` FOREIGN KEY (`UserID`) REFERENCES `account` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `RoleID` int NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(45) NOT NULL,
  PRIMARY KEY (`RoleID`),
  UNIQUE KEY `RoleID_UNIQUE` (`RoleID`),
  UNIQUE KEY `RoleName_UNIQUE` (`RoleName`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `SessionID` int NOT NULL AUTO_INCREMENT,
  `SessionDate` datetime NOT NULL,
  `Length` int NOT NULL,
  `ProgressPhoto` varchar(150) DEFAULT NULL,
  `Comment` varchar(500) DEFAULT NULL,
  `UserID` int NOT NULL,
  PRIMARY KEY (`SessionID`),
  UNIQUE KEY `SessionID_UNIQUE` (`SessionID`),
  KEY `UserID_idx` (`UserID`),
  CONSTRAINT `UserID2` FOREIGN KEY (`UserID`) REFERENCES `account` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `subteammembers`;
CREATE TABLE `subteammembers` (
  `SubteamID` int NOT NULL,
  `UserID` int NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserID_UNIQUE` (`UserID`),
  KEY `SubteamID_idx` (`SubteamID`),
  KEY `UserID_idx` (`UserID`),
  CONSTRAINT `SubteamID` FOREIGN KEY (`SubteamID`) REFERENCES `subteams` (`SubteamID`),
  CONSTRAINT `UserID` FOREIGN KEY (`UserID`) REFERENCES `account` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `subteams`;
CREATE TABLE `subteams` (
  `SubteamID` int NOT NULL AUTO_INCREMENT,
  `SubteamName` varchar(45) NOT NULL,
  `TeamID` int NOT NULL,
  PRIMARY KEY (`SubteamID`),
  UNIQUE KEY `SubteamID_UNIQUE` (`SubteamID`),
  UNIQUE KEY `SubteamName_UNIQUE` (`SubteamName`),
  KEY `TeamID_idx` (`TeamID`),
  CONSTRAINT `TeamID` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`TeamID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
  `TeamID` int NOT NULL AUTO_INCREMENT,
  `TeamName` varchar(45) NOT NULL,
  `BranchID` int NOT NULL,
  PRIMARY KEY (`TeamID`),
  UNIQUE KEY `TeamName_UNIQUE` (`TeamName`),
  UNIQUE KEY `TeamID_UNIQUE` (`TeamID`),
  KEY `BranchID_idx` (`BranchID`),
  CONSTRAINT `BranchID2` FOREIGN KEY (`BranchID`) REFERENCES `branches` (`BranchID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
