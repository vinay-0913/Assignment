-- ============================================================
-- Database & Table Setup for the Users API
-- Run this script in MySQL before starting the application.
-- ============================================================

CREATE DATABASE IF NOT EXISTS users
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE users;

-- The 'users' table (created automatically by SQLAlchemy,
-- but included here for reference / manual setup).
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(120)  NOT NULL,
    email       VARCHAR(255)  NOT NULL UNIQUE,
    role        VARCHAR(80)   NOT NULL,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Admin users table for JWT authentication (bonus).
CREATE TABLE IF NOT EXISTS admin_users (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(80)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
