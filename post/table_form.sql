-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- --------------------------------------------------------

--
-- Structure of table: `table_form`
--

CREATE TABLE `table_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date`  DATE NOT NULL DEFAULT CURRENT_DATE,
  `time` TIME NOT NULL DEFAULT CURRENT_TIME,
  `temperature` FLOAT NOT NULL,
  `humidity` FLOAT NOT NULL,
  `tvoc` INT NOT NULL,
  `eco2` INT NOT NULL,
  `soil_moisture` FLOAT NOT NULL,
  `light` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;
