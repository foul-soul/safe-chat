SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
-- Table structure for table `messages`-----------------------------------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` LONGBLOB NOT NULL,
  `msg_by` int(11) NOT NULL,
  `msg_to` int(11) NOT NULL,
  `msg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET= utf8mb3;
-- Table structure of rsa keys -------------------------------------------------------------
DROP TABLE IF EXISTS `rsa`;
CREATE TABLE IF NOT EXISTS `rsa`(
`id` int(11) NOT NULL,
`ppbk` int(11) NOT NULL,
`ppvk` int(11) NOT NULL,
PRIMARY KEY (`id`)
)
-- table for secret keys -------------------------------------------------------------------
DROP TABLE IF EXISTS `skey`;
CREATE TABLE IF NOT EXISTS `skey`(
`skid` int(11) NOT NULL,
`sk` int(11) NOT NULL,
PRIMARY KEY (`skid`)
)
-- Table structure for table `users`--------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(100) NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET= ascii;
--------------------------------------------------------------------------------------------------