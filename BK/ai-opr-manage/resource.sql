/*
Navicat MySQL Data Transfer

Source Server         : ssssss
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : resource

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2021-03-23 17:31:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `base_soft_data`
-- ----------------------------
DROP TABLE IF EXISTS `base_soft_data`;
CREATE TABLE `base_soft_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sJorgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `sJsoftType` tinyint(1) unsigned NOT NULL DEFAULT '9' COMMENT '软件类型1.数据库；2.中间件；9.其他',
  `sJsoftName` varchar(50) NOT NULL DEFAULT '' COMMENT '软件名称',
  `sJsoftVersion` varchar(128) NOT NULL DEFAULT '' COMMENT '软件版本',
  `sJsoftIp` varchar(50) NOT NULL DEFAULT '' COMMENT '部署IP地址',
  `sJsoftPort` varchar(50) NOT NULL DEFAULT '' COMMENT '端口',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='基础软件实例';

-- ----------------------------
-- Records of base_soft_data
-- ----------------------------

-- ----------------------------
-- Table structure for `cloud_data_all`
-- ----------------------------
DROP TABLE IF EXISTS `cloud_data_all`;
CREATE TABLE `cloud_data_all` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sJorgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `sJvmPlatCode` varchar(200) NOT NULL DEFAULT '' COMMENT '云平台唯一标识代码',
  `sJcloudBrand` varchar(200) NOT NULL DEFAULT '' COMMENT '云平台厂家品牌',
  `sJcloudScale` int(7) unsigned NOT NULL DEFAULT '0' COMMENT '建设规模,上报服务器数量',
  `sJcloudServCount` int(4) unsigned NOT NULL DEFAULT '0' COMMENT '云服务包含的服务类型的总数',
  `sJcloudServTypes` varchar(255) NOT NULL DEFAULT '' COMMENT '上报云平台包含的服务类型编码集，以半角逗号（“,”）分开，如：ECS,OSS',
  `sJcloudAppCount` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '云上应用数量',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='云平台总体建设';

-- ----------------------------
-- Records of cloud_data_all
-- ----------------------------

-- ----------------------------
-- Table structure for `cloud_serve_type`
-- ----------------------------
DROP TABLE IF EXISTS `cloud_serve_type`;
CREATE TABLE `cloud_serve_type` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sJorgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `sJcloudServType` varchar(50) NOT NULL DEFAULT '' COMMENT '云平台服务类型的编号',
  `sJcloudServName` varchar(200) NOT NULL DEFAULT '' COMMENT '云服务的名称，分局自定义',
  `sJcloudServCode` varchar(100) NOT NULL DEFAULT '' COMMENT '服务的唯一识别号，分局自定义',
  `sJcloudcount` int(7) unsigned NOT NULL DEFAULT '0' COMMENT '单项云服务的服务器设备数量',
  `sJcloudBrandCpu` int(7) unsigned NOT NULL DEFAULT '0' COMMENT 'CPU单位核',
  `sJcloudBrandMem` int(7) unsigned NOT NULL DEFAULT '0' COMMENT '内存单位G',
  `sJcloudBrandStore` int(7) unsigned NOT NULL DEFAULT '0' COMMENT '存储单位G',
  `sJcloudBrandBand` int(7) unsigned NOT NULL DEFAULT '0' COMMENT '带宽单位M',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='云平台分服务类型建设';

-- ----------------------------
-- Records of cloud_serve_type
-- ----------------------------

-- ----------------------------
-- Table structure for `org_code`
-- ----------------------------
DROP TABLE IF EXISTS `org_code`;
CREATE TABLE `org_code` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '名称',
  `code` char(12) NOT NULL DEFAULT '' COMMENT '机构代码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COMMENT='公安机构代码';

-- ----------------------------
-- Records of org_code
-- ----------------------------
INSERT INTO `org_code` VALUES ('1', '浦东分局', '310115000000');
INSERT INTO `org_code` VALUES ('2', '黄浦分局', '310101000000');
INSERT INTO `org_code` VALUES ('3', '徐汇分局', '310104000000');
INSERT INTO `org_code` VALUES ('4', '长宁分局', '310105000000');
INSERT INTO `org_code` VALUES ('5', '静安分局', '310106000000');
INSERT INTO `org_code` VALUES ('6', '普陀分局', '310107000000');
INSERT INTO `org_code` VALUES ('7', '虹口分局', '310109000000');
INSERT INTO `org_code` VALUES ('8', '杨浦分局', '310110000000');
INSERT INTO `org_code` VALUES ('9', '闵行分局', '310112000000');
INSERT INTO `org_code` VALUES ('10', '宝山分局', '310113000000');
INSERT INTO `org_code` VALUES ('11', '嘉定分局', '310114000000');
INSERT INTO `org_code` VALUES ('12', '松江分局', '310117000000');
INSERT INTO `org_code` VALUES ('13', '金山分局', '310116000000');
INSERT INTO `org_code` VALUES ('14', '青浦分局', '310118000000');
INSERT INTO `org_code` VALUES ('15', '奉贤分局', '310120000000');
INSERT INTO `org_code` VALUES ('16', '崇明分局', '310130000000');

-- ----------------------------
-- Table structure for `pc_room_data`
-- ----------------------------
DROP TABLE IF EXISTS `pc_room_data`;
CREATE TABLE `pc_room_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `rmCode` char(12) NOT NULL DEFAULT '' COMMENT '分局机房的编码',
  `envHealthValue` varchar(50) NOT NULL DEFAULT '' COMMENT '机房环境健康度',
  `powerHealthValue` varchar(50) NOT NULL DEFAULT '' COMMENT '机房动力系统健康度',
  `electrRealPower` varchar(50) NOT NULL DEFAULT '' COMMENT '市电使用实时功率，单位KW',
  `upsRealPower` varchar(50) NOT NULL DEFAULT '' COMMENT 'UPS使用实时功率，单位KW',
  `roomAverTemp` varchar(50) NOT NULL DEFAULT '' COMMENT '机房平均温度',
  `roomAverHum` varchar(50) NOT NULL DEFAULT '' COMMENT '机房平均湿度',
  `waterLeakStatus` varchar(50) NOT NULL DEFAULT '' COMMENT '漏水状态，上报状态值，10：正常，20：报警',
  `fireStatus` varchar(50) NOT NULL DEFAULT '' COMMENT '消防状态，上报状态值，10：正常，20：报警',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='机房环境运行指标数据';

-- ----------------------------
-- Records of pc_room_data
-- ----------------------------

-- ----------------------------
-- Table structure for `police_wechat_data`
-- ----------------------------
DROP TABLE IF EXISTS `police_wechat_data`;
CREATE TABLE `police_wechat_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `agentid` varchar(50) NOT NULL DEFAULT '' COMMENT '警务微信应用ID，管理端可查看',
  `appName` varchar(50) NOT NULL DEFAULT '' COMMENT '应用名',
  `checkTime` varchar(50) NOT NULL DEFAULT '' COMMENT '时间',
  `result` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '自检结果 0,1',
  `expdesc` varchar(255) DEFAULT '' COMMENT '异常说明',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='警务微信轻应用运行监控指标';

-- ----------------------------
-- Records of police_wechat_data
-- ----------------------------

-- ----------------------------
-- Table structure for `report_log`
-- ----------------------------
DROP TABLE IF EXISTS `report_log`;
CREATE TABLE `report_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `reportType` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '1资源配置2指标数据3故障告警数据4故障工单处理数据',
  `requestData` text COMMENT '请求数据',
  `resultData` text COMMENT '结果数据',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='上报记录';

-- ----------------------------
-- Records of report_log
-- ----------------------------

-- ----------------------------
-- Table structure for `server_data`
-- ----------------------------
DROP TABLE IF EXISTS `server_data`;
CREATE TABLE `server_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `ciId` varchar(50) NOT NULL DEFAULT '' COMMENT '性能指标对应的服务器设备资源的唯一标识，和资产上报中的编码一致',
  `devOnlineState` varchar(50) NOT NULL DEFAULT '' COMMENT '设备在线状态，上报状态值，10：在线，20：离线',
  `devResponseTime` int(4) unsigned NOT NULL DEFAULT '0' COMMENT '设备响应时间，单位ms',
  `devAlertLevel` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '设备故障告警等级，上报状态值，等级包括： 3：关键的，2：错误，1：警告，0：正常',
  `devCpuRate` varchar(50) NOT NULL DEFAULT '' COMMENT '设备CPU利用率',
  `devMemRate` varchar(50) NOT NULL DEFAULT '' COMMENT '设备CPU利用率',
  `devDiskRate` varchar(50) NOT NULL DEFAULT '' COMMENT '设备磁盘使用率，整体磁盘空间比',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='服务器监测指标';

-- ----------------------------
-- Records of server_data
-- ----------------------------

-- ----------------------------
-- Table structure for `server_data_all`
-- ----------------------------
DROP TABLE IF EXISTS `server_data_all`;
CREATE TABLE `server_data_all` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `devHealthValue` varchar(50) NOT NULL DEFAULT '' COMMENT '设备健康指数分局所有服务器设备的健康度评价分值',
  `devOnlineRate` varchar(50) NOT NULL DEFAULT '' COMMENT '分局服务器设备的在线率',
  `devAverCpuRate` varchar(50) NOT NULL DEFAULT '' COMMENT '分局服务器设备的平均CPU负载率',
  `devAverMemRate` varchar(50) NOT NULL DEFAULT '' COMMENT '分局服务器设备的平均内存负载率',
  `devAverDiskRate` varchar(50) NOT NULL DEFAULT '' COMMENT '分局服务器设备的平均磁盘使用率（所有磁盘汇总）',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='服务器监测总体情况';

-- ----------------------------
-- Records of server_data_all
-- ----------------------------

-- ----------------------------
-- Table structure for `soft_data`
-- ----------------------------
DROP TABLE IF EXISTS `soft_data`;
CREATE TABLE `soft_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgCode` char(12) NOT NULL DEFAULT '' COMMENT '公安机关机构代码',
  `ciId` varchar(50) NOT NULL DEFAULT '' COMMENT '性能指标对应的服务器设备资源的唯一标识，和资产上报中的编码一致',
  `runningState` varchar(50) NOT NULL DEFAULT '' COMMENT '通过进程或服务端口状态判断的软件运行状态，上报状态值，10：正常，20：异常',
  `tcpState` varchar(50) NOT NULL DEFAULT '' COMMENT '软件服务端口状态，上报状态值，10：正常，20：异常',
  `webResponseTime` int(4) unsigned NOT NULL DEFAULT '0' COMMENT '软件web服务响应时间，单位ms',
  `isReported` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否已上报,0:未上报,1已上报',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0 未删除 1已删除',
  `createdTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updatedTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `isReported` (`isReported`),
  KEY `isDeleted` (`isDeleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='软件实例运行指标';

-- ----------------------------
-- Records of soft_data
-- ----------------------------
