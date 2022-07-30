/*
 Navicat MySQL Data Transfer

 Source Server         : my
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : localhost:3306
 Source Schema         : lty

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 30/07/2022 16:43:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for blog_data
-- ----------------------------
DROP TABLE IF EXISTS `blog_data`;
CREATE TABLE `blog_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `blog_id` int NULL DEFAULT NULL COMMENT '文章id',
  `page_view` int NULL DEFAULT NULL COMMENT '浏览量',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blog_data
-- ----------------------------
INSERT INTO `blog_data` VALUES (2, 2, 141);
INSERT INTO `blog_data` VALUES (4, 5, 0);
INSERT INTO `blog_data` VALUES (5, 6, 3453);
INSERT INTO `blog_data` VALUES (6, 7, 222);
INSERT INTO `blog_data` VALUES (7, 8, 1123);
INSERT INTO `blog_data` VALUES (9, 10, 3);
INSERT INTO `blog_data` VALUES (10, 11, 56);
INSERT INTO `blog_data` VALUES (12, 13, 2);
INSERT INTO `blog_data` VALUES (13, 4, 1);
INSERT INTO `blog_data` VALUES (14, 14, 12);

-- ----------------------------
-- Table structure for blogs
-- ----------------------------
DROP TABLE IF EXISTS `blogs`;
CREATE TABLE `blogs`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '文章id',
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '账号',
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '内容',
  `time` datetime NULL DEFAULT NULL COMMENT '时间',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '标题',
  `brief` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '简要',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `title`(`title`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of blogs
-- ----------------------------
INSERT INTO `blogs` VALUES (2, '22334455', 'html/tt.txt', '2022-02-22 19:52:43', 'pyss', '还好吧2');
INSERT INTO `blogs` VALUES (4, '22334455', 'html/tt.txt', '2022-02-22 20:04:57', 'kjap', '微服务3');
INSERT INTO `blogs` VALUES (5, '22334455', 'html/tt.txt', '2022-02-22 20:05:19', '让人', '为首的4');
INSERT INTO `blogs` VALUES (6, '77889944', 'html/tt.txt', '2022-04-03 18:08:47', '我真的', '关于5');
INSERT INTO `blogs` VALUES (7, '77889944', 'html/tt.txt', '2022-04-03 18:09:22', '威风威风', '哇啊啊啊测试6');
INSERT INTO `blogs` VALUES (8, '11223344', 'html/tt.txt', '2022-04-03 18:09:45', '撒旦飞洒', '娃娃水水7');
INSERT INTO `blogs` VALUES (10, '77889944', 'html/tt.txt', '2022-04-03 18:10:16', '士大夫是v', '强强强强9');
INSERT INTO `blogs` VALUES (11, '77889944', 'html/tt.txt', '2022-04-03 18:10:34', '撒旦发生下', '趣味无穷10');
INSERT INTO `blogs` VALUES (13, '11223344', 'html/55a084358285b214ebdf712074c26b2e.txt', '2022-04-15 14:48:35', '可是当你烦恼吗', 'ef editor():\n    re');
INSERT INTO `blogs` VALUES (14, '11223344', 'html/af1df8bc9d278b7adeb1fee02ad0fda5.txt', '2022-04-21 17:43:30', '这是测试文章', 'ignOr(val) {\n      ');

-- ----------------------------
-- Table structure for code_res
-- ----------------------------
DROP TABLE IF EXISTS `code_res`;
CREATE TABLE `code_res`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` int NULL DEFAULT NULL,
  `state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of code_res
-- ----------------------------
INSERT INTO `code_res` VALUES (1, 0, '正常');
INSERT INTO `code_res` VALUES (2, -1, '执行异常');
INSERT INTO `code_res` VALUES (3, 1, 'not find');
INSERT INTO `code_res` VALUES (4, 110, '数据格式错误');
INSERT INTO `code_res` VALUES (5, 20, '邮箱存在');
INSERT INTO `code_res` VALUES (6, 21, '账号存在');
INSERT INTO `code_res` VALUES (7, 22, '验证码错误');
INSERT INTO `code_res` VALUES (8, 23, '账号或密码错误');
INSERT INTO `code_res` VALUES (9, 24, 'token错误');
INSERT INTO `code_res` VALUES (10, 25, 'session错误');
INSERT INTO `code_res` VALUES (11, 26, '已存在');
INSERT INTO `code_res` VALUES (12, 27, '写入失败');
INSERT INTO `code_res` VALUES (13, 28, '没有标签');
INSERT INTO `code_res` VALUES (14, 29, '关注自己');
INSERT INTO `code_res` VALUES (15, 30, 'xss');
INSERT INTO `code_res` VALUES (16, 31, '标签数量限制');
INSERT INTO `code_res` VALUES (17, 32, '收藏夹数量限制');
INSERT INTO `code_res` VALUES (18, 33, '已收藏');
INSERT INTO `code_res` VALUES (19, 34, 'dos');

-- ----------------------------
-- Table structure for collect
-- ----------------------------
DROP TABLE IF EXISTS `collect`;
CREATE TABLE `collect`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `blog_id` int NULL DEFAULT NULL COMMENT '文章id',
  `folder_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件夹',
  `time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of collect
-- ----------------------------
INSERT INTO `collect` VALUES (3, 1, '2', '2022-03-19 16:13:03');
INSERT INTO `collect` VALUES (6, 4, '3', '2022-04-13 15:53:51');
INSERT INTO `collect` VALUES (8, 2, '3', '2022-04-13 21:30:34');

-- ----------------------------
-- Table structure for collect_folder
-- ----------------------------
DROP TABLE IF EXISTS `collect_folder`;
CREATE TABLE `collect_folder`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `folder` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `account` int NULL DEFAULT NULL,
  `time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of collect_folder
-- ----------------------------
INSERT INTO `collect_folder` VALUES (2, '算法', 11223344, '2022-03-05 20:28:56');
INSERT INTO `collect_folder` VALUES (3, '数据结构', 11223344, '2022-04-12 20:35:40');
INSERT INTO `collect_folder` VALUES (6, '操作系统', 11223344, '2022-04-13 20:55:19');
INSERT INTO `collect_folder` VALUES (7, '王德法', 11223344, '2022-04-13 21:13:24');
INSERT INTO `collect_folder` VALUES (8, '125', 11223344, '2022-05-07 11:12:49');

-- ----------------------------
-- Table structure for del_blog
-- ----------------------------
DROP TABLE IF EXISTS `del_blog`;
CREATE TABLE `del_blog`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `blog` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of del_blog
-- ----------------------------
INSERT INTO `del_blog` VALUES (1, 12);
INSERT INTO `del_blog` VALUES (2, 9);
INSERT INTO `del_blog` VALUES (3, 1);

-- ----------------------------
-- Table structure for fans
-- ----------------------------
DROP TABLE IF EXISTS `fans`;
CREATE TABLE `fans`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `star` int NULL DEFAULT NULL COMMENT '明星',
  `fan` int NULL DEFAULT NULL COMMENT '粉丝',
  `time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fans
-- ----------------------------
INSERT INTO `fans` VALUES (2, 22334455, 77889944, '2022-03-05 18:32:45');
INSERT INTO `fans` VALUES (4, 11223344, 77889944, '2022-04-15 18:03:48');
INSERT INTO `fans` VALUES (5, 77889944, 11223344, '2022-04-15 18:03:46');
INSERT INTO `fans` VALUES (7, 33344498, 11223344, '2022-04-15 18:03:46');

-- ----------------------------
-- Table structure for label
-- ----------------------------
DROP TABLE IF EXISTS `label`;
CREATE TABLE `label`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` int NULL DEFAULT NULL,
  `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of label
-- ----------------------------
INSERT INTO `label` VALUES (1, 11223344, 'py');
INSERT INTO `label` VALUES (3, 11223344, 'python');
INSERT INTO `label` VALUES (12, 11223344, '111');

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reply_id` int NULL DEFAULT NULL COMMENT '文章id',
  `account` int NULL DEFAULT NULL COMMENT '评价账号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of likes
-- ----------------------------
INSERT INTO `likes` VALUES (1, 1, 77889944);
INSERT INTO `likes` VALUES (2, 1, 22334455);
INSERT INTO `likes` VALUES (3, 1, 11223344);
INSERT INTO `likes` VALUES (4, 2, 11223344);
INSERT INTO `likes` VALUES (5, 3, 11223344);

-- ----------------------------
-- Table structure for likes_z
-- ----------------------------
DROP TABLE IF EXISTS `likes_z`;
CREATE TABLE `likes_z`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reply_id` int NULL DEFAULT NULL,
  `account` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of likes_z
-- ----------------------------
INSERT INTO `likes_z` VALUES (1, 2, 11223344);

-- ----------------------------
-- Table structure for reply
-- ----------------------------
DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply`  (
  `ID` int NOT NULL AUTO_INCREMENT,
  `blog_id` int NULL DEFAULT NULL COMMENT '文章id',
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '内容',
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '评论用户',
  `time` datetime NULL DEFAULT NULL COMMENT '时间',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reply
-- ----------------------------
INSERT INTO `reply` VALUES (1, 1, 'wdf', '11223344', '2022-03-19 18:14:22');
INSERT INTO `reply` VALUES (2, 1, 'sdfas', '22334455', '2022-03-19 18:17:05');
INSERT INTO `reply` VALUES (3, 2, '真的吗', '11223344', '2022-04-13 22:37:11');
INSERT INTO `reply` VALUES (5, 14, '我觉得不错', '11223344', '2022-04-21 17:56:22');
INSERT INTO `reply` VALUES (6, 14, 'jjkk', '11223344', '2022-05-07 11:13:20');

-- ----------------------------
-- Table structure for reply_z
-- ----------------------------
DROP TABLE IF EXISTS `reply_z`;
CREATE TABLE `reply_z`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reply_id` int NULL DEFAULT NULL,
  `account` int NULL DEFAULT NULL,
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime NULL DEFAULT NULL,
  `ton` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reply_z
-- ----------------------------
INSERT INTO `reply_z` VALUES (1, 1, 22334455, 'ssss', '2022-03-19 18:24:50', '0');
INSERT INTO `reply_z` VALUES (2, 1, 77889944, 'asdfsdaf', '2022-03-19 18:26:46', '定风波');
INSERT INTO `reply_z` VALUES (3, 2, 77889944, 'wwaa', '2022-03-19 18:46:27', '0');
INSERT INTO `reply_z` VALUES (4, 1, 11223344, '这真的是能说的吗', '2022-04-14 16:50:22', '0');
INSERT INTO `reply_z` VALUES (5, 1, 11223344, 'None', '2022-04-14 19:14:20', 'pool');
INSERT INTO `reply_z` VALUES (6, 5, 11223344, '确实', '2022-04-22 16:46:34', '0');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `ID` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pool' COMMENT '用户名',
  `Email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `loginDate` datetime NULL DEFAULT NULL COMMENT '注册时间',
  `Account` int NULL DEFAULT NULL COMMENT '账号',
  `headP` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'img/qq.jpg' COMMENT '头像',
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `sign` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '懒狗' COMMENT '个性签名',
  `sessioned` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录信息',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (6, '温华pool', '', '2015-09-28 11:51:08', 77889944, 'head/qq.jpg', '123456', '花有重开日', '5de6f3e433dba64b5d545bcf932c1efb');
INSERT INTO `user` VALUES (8, '定风波', '', '2015-09-28 11:55:08', 22334455, 'head/qq.jpg', '123456', '人无再少年', '3495035d8d1e3d022ac38511aaaaef33');
INSERT INTO `user` VALUES (21, 'pool', '1097641954@qq.com', '2022-02-22 17:39:34', 11223344, 'head/5099d6fd277e8d215cae393a388e0f68.jpg', '11111111', '团长我™莱纳 ', '258a94b991afb38771bbcfe1cc3c8bfc');
INSERT INTO `user` VALUES (22, 'pool去东百', NULL, '2022-04-03 21:48:48', 33344498, 'head/qq.jpg', '12345678', '懒狗', '691df75963eeb5ef9b4cfd0541df5a59');

SET FOREIGN_KEY_CHECKS = 1;
