import pymysql
from datetime import datetime
from config import Config


def get_db_connection():
    """Establece conexión con MySQL usando la configuración actual."""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=10,
    )


def init_database():
    """Crea tablas e inserta datos iniciales si la base está vacía."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL,
            name VARCHAR(100) NOT NULL,
            role VARCHAR(50) DEFAULT 'Administradora'
        )
    """)

    cursor.execute("""
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
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            clave VARCHAR(50) UNIQUE NOT NULL,
            valor VARCHAR(100) NOT NULL,
            descripcion VARCHAR(200)
        )
    """)

    # Usuario administrador
    cursor.execute("SELECT id FROM users WHERE email = %s", ("frank@nexzone.com",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (email, password, name, role) VALUES (%s, %s, %s, %s)",
            ("frank@nexzone.com", "admin123", "Frank Cetina", "Administradora"),
        )

    # Parámetro de token
    cursor.execute(
        "SELECT id FROM parametros WHERE clave = %s", ("token_expiration_minutes",)
    )
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO parametros (clave, valor, descripcion) VALUES (%s, %s, %s)",
            ("token_expiration_minutes", "20", "Minutos de duración del token JWT"),
        )

    # Contenido inicial
    cursor.execute("SELECT COUNT(*) AS total FROM content")
    if cursor.fetchone()["total"] == 0:
        initial = [
            ("Big Buck Bunny", "video", "Publicado", 124, "9:56", "aqz-KE-bpKQ",
             "https://img.youtube.com/vi/aqz-KE-bpKQ/hqdefault.jpg", "2026-05-10"),
            ("Sintel", "video", "Publicado", 89, "14:48", "eRsGyueVLvQ",
             "https://img.youtube.com/vi/eRsGyueVLvQ/hqdefault.jpg", "2026-05-12"),
            ("Sprite Fright", "video", "Publicado", 67, "10:57", "_cMxraX_5RE",
             "https://img.youtube.com/vi/_cMxraX_5RE/hqdefault.jpg", "2026-05-18"),
            ("Coffee Run", "video", "Publicado", 45, "7:48", "PVGeM40dABA",
             "https://img.youtube.com/vi/PVGeM40dABA/hqdefault.jpg", "2026-05-20"),
            ("Spring", "video", "Publicado", 38, "8:01", "WhWc3b3KhnY",
             "https://img.youtube.com/vi/WhWc3b3KhnY/hqdefault.jpg", "2026-05-22"),
            ("Tears of Steel", "video", "Publicado", 52, "12:14", "R6MlUcmOul8",
             "https://img.youtube.com/vi/R6MlUcmOul8/hqdefault.jpg", "2026-05-15"),
        ]
        for item in initial:
            cursor.execute("""
                INSERT INTO content
                (title, type, status, plays, duration, youtube_id, thumb, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, item)

    conn.close()
    print("[DB] Base de datos inicializada correctamente.")


def validate_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s", (email, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_parametro(clave, default=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM parametros WHERE clave = %s", (clave,))
    row = cursor.fetchone()
    conn.close()
    return row["valor"] if row else default


def set_parametro(clave, valor, descripcion=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parametros (clave, valor, descripcion)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            valor = VALUES(valor),
            descripcion = COALESCE(VALUES(descripcion), descripcion)
    """, (clave, valor, descripcion))
    conn.close()


def get_all_content():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content ORDER BY created_at DESC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_content_by_id(content_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content WHERE id = %s", (content_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_content_db(item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO content
        (title, type, status, plays, duration, youtube_id, thumb, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
    """, (
        item.get("title", "Sin título"),
        item.get("type", "video"),
        item.get("status", "Publicado"),
        0,
        item.get("duration", "—"),
        item.get("youtube_id", ""),
        item.get("thumb", "https://picsum.photos/id/160/300/170"),
    ))
    new_id = cursor.lastrowid
    conn.close()
    return get_content_by_id(new_id)


def update_content_db(content_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in data.items():
        if k in ("title", "status", "duration", "plays"):
            fields.append(f"{k} = %s")
            values.append(v)
    if not fields:
        return None
    values.append(content_id)
    sql = f"UPDATE content SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(sql, values)
    conn.close()
    return get_content_by_id(content_id)


def delete_content_db(content_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM content WHERE id = %s", (content_id,))
    conn.close()


def increment_plays_db(content_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE content SET plays = plays + 1 WHERE id = %s", (content_id,)
    )
    cursor.execute("SELECT plays FROM content WHERE id = %s", (content_id,))
    row = cursor.fetchone()
    conn.close()
    return row["plays"] if row else 0


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, role FROM users ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_user_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, password, name, role)
        VALUES (%s, %s, %s, %s)
    """, (
        data.get("email"),
        data.get("password", "123456"),
        data.get("name", "Nuevo Usuario"),
        data.get("role", "Administradora"),
    ))
    new_id = cursor.lastrowid
    conn.close()
    return get_user_by_id(new_id)


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, name, role FROM users WHERE id = %s", (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_user_db(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in data.items():
        if k in ("email", "name", "role", "password"):
            fields.append(f"{k} = %s")
            values.append(v)
    if not fields:
        return None
    values.append(user_id)
    sql = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(sql, values)
    conn.close()
    return get_user_by_id(user_id)


def delete_user_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.close()
