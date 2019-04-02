/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50626
Source Host           : localhost:3306
Source Database       : weather_info

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2019-01-16 10:04:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `new_inf_weather`
-- ----------------------------
DROP TABLE IF EXISTS `new_inf_weather`;
CREATE TABLE `new_inf_weather` (
  `cityCode` varchar(255) NOT NULL DEFAULT '',
  `publish_time` varchar(255) NOT NULL DEFAULT '',
  `city` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT '',
  `temperature` varchar(255) DEFAULT NULL,
  `airpressure` varchar(255) DEFAULT NULL,
  `humidity` varchar(255) DEFAULT NULL,
  `rcomfort` varchar(255) DEFAULT NULL,
  `icomfort` varchar(255) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `feelst` varchar(255) DEFAULT NULL,
  `direct` varchar(255) DEFAULT NULL,
  `power` varchar(255) DEFAULT NULL,
  `speed` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cityCode`,`publish_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of new_inf_weather
-- ----------------------------
