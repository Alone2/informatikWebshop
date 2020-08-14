-- MySQL Script generated by MySQL Workbench
-- Fri 14 Aug 2020 02:00:20 PM CEST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Webshop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Webshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Webshop` ;
-- -----------------------------------------------------
-- Schema WebshopEasy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema WebshopEasy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `WebshopEasy` ;
USE `Webshop` ;

-- -----------------------------------------------------
-- Table `Webshop`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(100) NOT NULL,
  `username` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Webshop`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(70) NOT NULL,
  `description` VARCHAR(240) NULL,
  `price` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Webshop`.`image2item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`image2item` (
  `imageId` INT NOT NULL,
  `itemId` INT NOT NULL,
  INDEX `itemId_idx` (`itemId` ASC) VISIBLE,
  PRIMARY KEY (`imageId`, `itemId`),
  CONSTRAINT `itemId`
    FOREIGN KEY (`itemId`)
    REFERENCES `Webshop`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Webshop`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(120) NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Webshop`.`cartItem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`cartItem` (
  `itemId` INT NOT NULL,
  `userId` INT NOT NULL,
  `count` INT NOT NULL,
  PRIMARY KEY (`itemId`, `userId`),
  INDEX `userId_idx` (`userId` ASC) VISIBLE,
  CONSTRAINT `itemId`
    FOREIGN KEY (`itemId`)
    REFERENCES `Webshop`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `userId`
    FOREIGN KEY (`userId`)
    REFERENCES `Webshop`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(70) NOT NULL,
  `description` VARCHAR(240) NULL,
  `price` FLOAT NULL,
  `alkoholAmount` FLOAT NULL,
  `volume` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(120) NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Webshop`.`category2item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Webshop`.`category2item` (
  `itemId` INT NOT NULL,
  `categoryId` INT NOT NULL,
  PRIMARY KEY (`itemId`, `categoryId`),
  INDEX `categoryId_idx` (`categoryId` ASC) VISIBLE,
  CONSTRAINT `itemId`
    FOREIGN KEY (`itemId`)
    REFERENCES `WebshopEasy`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `categoryId`
    FOREIGN KEY (`categoryId`)
    REFERENCES `WebshopEasy`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `WebshopEasy` ;

-- -----------------------------------------------------
-- Table `WebshopEasy`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(100) NOT NULL,
  `username` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`image` (
  `id` INT NOT NULL,
  `png` BLOB NOT NULL,
  `itemId` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `item_idx` (`itemId` ASC) VISIBLE,
  CONSTRAINT `item`
    FOREIGN KEY (`itemId`)
    REFERENCES `WebshopEasy`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`category2item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`category2item` (
  `itemId` INT NOT NULL,
  `categoryId` INT NOT NULL,
  PRIMARY KEY (`itemId`, `categoryId`),
  CONSTRAINT `itemId`
    FOREIGN KEY (`itemId` , `categoryId`)
    REFERENCES `WebshopEasy`.`item` (`id` , `id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `categoryId`
    FOREIGN KEY ()
    REFERENCES `WebshopEasy`.`category` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `userId` INT NOT NULL,
  `isPlaced` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  INDEX `userID_idx` (`userId` ASC) VISIBLE,
  CONSTRAINT `userID`
    FOREIGN KEY (`userId`)
    REFERENCES `WebshopEasy`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `WebshopEasy`.`item2order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `WebshopEasy`.`item2order` (
  `itemId` INT NOT NULL,
  `oderId` INT NOT NULL,
  `count` INT NULL,
  PRIMARY KEY (`itemId`, `oderId`),
  INDEX `orderID_idx` (`oderId` ASC) VISIBLE,
  CONSTRAINT `orderID`
    FOREIGN KEY (`oderId`)
    REFERENCES `WebshopEasy`.`order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `itemId`
    FOREIGN KEY (`itemId`)
    REFERENCES `WebshopEasy`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
