-- ========================================
-- AI专属人设训练APP - 数据库初始化脚本
-- 数据库: ai_personality
-- ========================================

CREATE DATABASE IF NOT EXISTS ai_personality
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE ai_personality;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `phone` VARCHAR(20) NOT NULL UNIQUE,
  `avatar` VARCHAR(255) DEFAULT '',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AI分身表
CREATE TABLE IF NOT EXISTS `user_avatar` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `avatar_name` VARCHAR(50) DEFAULT '我的AI分身',
  `train_type` VARCHAR(30) NOT NULL,
  `birthday` VARCHAR(20) DEFAULT '',
  `constellation` VARCHAR(20) DEFAULT '',
  `status` INT DEFAULT 1,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user_id (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 基础人设表
CREATE TABLE IF NOT EXISTS `personality_base` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL UNIQUE,
  `age` VARCHAR(20) DEFAULT '',
  `identity` VARCHAR(50) DEFAULT '',
  `talk_speed` VARCHAR(20) DEFAULT 'normal',
  `hobby` TEXT,
  `taboo` TEXT,
  `advantage` TEXT,
  `disadvantage` TEXT,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_avatar_id (`avatar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 三观伦理库
CREATE TABLE IF NOT EXISTS `personality_wvw` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `is_init_constellation` INT DEFAULT 0,
  `world_view` TEXT,
  `life_view` TEXT,
  `value_view` TEXT,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_avatar_id (`avatar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 情绪训练表
CREATE TABLE IF NOT EXISTS `personality_emotion` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `emotion_type` VARCHAR(20) NOT NULL,
  `trigger_rule` TEXT,
  `feature` TEXT,
  `intensity` INT DEFAULT 5,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_avatar_emotion (`avatar_id`, `emotion_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 情绪样本表
CREATE TABLE IF NOT EXISTS `emotion_sample` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `emotion_type` VARCHAR(20) NOT NULL,
  `content` TEXT NOT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_avatar_emotion (`avatar_id`, `emotion_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 社交训练表
CREATE TABLE IF NOT EXISTS `social_train` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `social_type` VARCHAR(20) NOT NULL,
  `social_feature` TEXT,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_avatar_social (`avatar_id`, `social_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AI自主训练记录表
CREATE TABLE IF NOT EXISTS `ai_auto_chat` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `emotion_type` VARCHAR(20) DEFAULT '',
  `social_type` VARCHAR(20) DEFAULT '',
  `ai_content` TEXT NOT NULL,
  `user_correct_content` TEXT DEFAULT '',
  `is_correct` INT DEFAULT 0,
  `weight` INT DEFAULT 1,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_avatar_id (`avatar_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 聊天记录表
CREATE TABLE IF NOT EXISTS `chat_history` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `avatar_id` BIGINT NOT NULL,
  `role` VARCHAR(10) NOT NULL,
  `content` TEXT NOT NULL,
  `emotion_type` VARCHAR(20) DEFAULT '',
  `social_type` VARCHAR(20) DEFAULT '',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_avatar_id (`avatar_id`),
  INDEX idx_create_time (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
