-- =============================================
-- NexZone - Esquema MySQL
-- Proyecto universitario 2026
-- =============================================

CREATE DATABASE IF NOT EXISTS nexzone_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE nexzone_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'Administradora'
);

-- Tabla de contenido
CREATE TABLE IF NOT EXISTS content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    type VARCHAR(20) DEFAULT 'video',
    status VARCHAR(30) DEFAULT 'Publicado',
    plays INT DEFAULT 0,
    duration VARCHAR(20) DEFAULT '—',
    youtube_id VARCHAR(50),
    thumb VARCHAR(300),
    created_at DATE
);

-- Tabla de parámetros del sistema
CREATE TABLE IF NOT EXISTS parametros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(50) UNIQUE NOT NULL,
    valor VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200)
);

-- Usuario administrador inicial
INSERT IGNORE INTO users (email, password, name, role)
VALUES ('frank@nexzone.com', 'admin123', 'Frank Cetina', 'Administradora');

-- Parámetro de expiración de token
INSERT IGNORE INTO parametros (clave, valor, descripcion)
VALUES ('token_expiration_minutes', '20', 'Minutos de duración del token JWT');

-- Contenido inicial (Blender Foundation - Creative Commons)
INSERT IGNORE INTO content (title, type, status, plays, duration, youtube_id, thumb, created_at) VALUES
('Big Buck Bunny', 'video', 'Publicado', 124, '9:56', 'aqz-KE-bpKQ', 'https://img.youtube.com/vi/aqz-KE-bpKQ/hqdefault.jpg', '2026-05-10'),
('Sintel', 'video', 'Publicado', 89, '14:48', 'eRsGyueVLvQ', 'https://img.youtube.com/vi/eRsGyueVLvQ/hqdefault.jpg', '2026-05-12'),
('Sprite Fright', 'video', 'Publicado', 67, '10:57', '_cMxraX_5RE', 'https://img.youtube.com/vi/_cMxraX_5RE/hqdefault.jpg', '2026-05-18'),
('Coffee Run', 'video', 'Publicado', 45, '7:48', 'PVGeM40dABA', 'https://img.youtube.com/vi/PVGeM40dABA/hqdefault.jpg', '2026-05-20'),
('Spring', 'video', 'Publicado', 38, '8:01', 'WhWc3b3KhnY', 'https://img.youtube.com/vi/WhWc3b3KhnY/hqdefault.jpg', '2026-05-22'),
('Tears of Steel', 'video', 'Publicado', 52, '12:14', 'R6MlUcmOul8', 'https://img.youtube.com/vi/R6MlUcmOul8/hqdefault.jpg', '2026-05-15');
