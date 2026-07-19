# NexZone

Panel de administración de contenido multimedia desarrollado con Flask y MySQL.

Proyecto universitario — Ingeniería en Sistemas · 2026

---

## Características

- Autenticación con JWT (tiempo de expiración configurable desde la base de datos)
- Gestión completa de contenido (CRUD + contador de reproducciones)
- Catálogo de usuarios (altas, bajas y cambios)
- Parámetros del sistema
- Interfaz oscura tipo plataforma de streaming
- Reproductor embebido de YouTube
- Página pública de ejemplo

---

## Requisitos

- Python 3.11 o superior
- MySQL 8.0 o superior (local o remoto)
- Cuenta en [Railway](https://railway.app) o proveedor equivalente para el despliegue

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/nexzone.git
cd nexzone

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env          # Windows
# cp .env.example .env          # Linux / macOS

# Editar .env con tus credenciales de MySQL

# 5. Crear la base de datos
mysql -u root -p < schema_mysql.sql

# 6. Ejecutar
python app.py
```

Abrir: http://127.0.0.1:5000

**Credenciales de acceso**

| Campo     | Valor                 |
|-----------|-----------------------|
| Correo    | frank@nexzone.com     |
| Contraseña| admin123              |

---

## Despliegue en Railway (recomendado)

### 1. Subir el código a GitHub

```bash
git init
git add .
git commit -m "Initial commit - NexZone"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/nexzone.git
git push -u origin main
```

### 2. Crear proyecto en Railway

1. Ir a [railway.app](https://railway.app) e iniciar sesión con GitHub.
2. **New Project** → **Deploy from GitHub repo** → seleccionar `nexzone`.
3. Railway detectará automáticamente el `Procfile` y desplegará la aplicación.

### 3. Agregar base de datos MySQL

1. Dentro del mismo proyecto: **+ New** → **Database** → **MySQL**.
2. Esperar a que el servicio MySQL esté activo.
3. En la pestaña **Variables** del servicio MySQL copiar:
   - `MYSQLHOST`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`
   - `MYSQLDATABASE`
   - `MYSQLPORT`

### 4. Configurar variables de la aplicación

En el servicio de la aplicación web, agregar las siguientes variables:

| Variable          | Valor                                      |
|-------------------|--------------------------------------------|
| `MYSQL_HOST`      | valor de `MYSQLHOST`                       |
| `MYSQL_USER`      | valor de `MYSQLUSER`                       |
| `MYSQL_PASSWORD`  | valor de `MYSQLPASSWORD`                   |
| `MYSQL_DB`        | valor de `MYSQLDATABASE`                   |
| `MYSQL_PORT`      | valor de `MYSQLPORT`                       |
| `SECRET_KEY`      | cadena aleatoria segura                    |
| `JWT_SECRET`      | otra cadena aleatoria diferente            |
| `DEBUG`           | `False`                                    |

### 5. Cargar el esquema (opcional)

La aplicación crea las tablas automáticamente al iniciar.  
Si se desea cargar el archivo SQL manualmente:

1. Conectar al MySQL de Railway con cualquier cliente (DBeaver, MySQL Workbench, TablePlus, etc.).
2. Ejecutar el contenido de `schema_mysql.sql`.

### 6. Generar dominio público

En el servicio de la aplicación: **Settings** → **Networking** → **Generate Domain**.

La URL generada será la liga pública del proyecto.

---

## Estructura del proyecto

```
nexzone/
├── app.py                 # Punto de entrada
├── config.py              # Configuración y variables de entorno
├── requirements.txt
├── Procfile               # Configuración para Railway / Heroku
├── schema_mysql.sql       # Esquema y datos iniciales
├── .env.example
├── src/
│   ├── __init__.py        # Factory de la aplicación
│   ├── models/
│   │   ├── database.py    # Acceso a MySQL
│   │   └── content.py
│   └── routes/
│       ├── auth.py
│       ├── dashboard.py
│       └── public.py
├── static/
│   ├── css/style.css
│   └── js/dashboard.js
└── templates/
    ├── login.html
    ├── dashboard.html
    └── public_page.html
```

---

## API interna (requiere sesión)

| Método | Ruta                              | Descripción                    |
|--------|-----------------------------------|--------------------------------|
| GET    | `/dashboard/api/content`          | Listar contenido               |
| POST   | `/dashboard/api/content`          | Crear contenido                |
| PUT    | `/dashboard/api/content/<id>`     | Actualizar contenido           |
| DELETE | `/dashboard/api/content/<id>`     | Eliminar contenido             |
| POST   | `/dashboard/api/content/<id>/play`| Incrementar reproducciones     |
| GET    | `/dashboard/api/users`            | Listar usuarios                |
| POST   | `/dashboard/api/users`            | Crear usuario                  |
| PUT    | `/dashboard/api/users/<id>`       | Actualizar usuario             |
| DELETE | `/dashboard/api/users/<id>`       | Eliminar usuario               |
| GET    | `/dashboard/api/parametros`       | Obtener parámetros             |
| POST   | `/dashboard/api/parametros`       | Actualizar parámetro           |
| POST   | `/dashboard/api/refresh_token`    | Renovar JWT                    |
| GET    | `/dashboard/api/verify_token`     | Verificar validez del token    |

---

## Notas de seguridad

- Las contraseñas se almacenan en texto plano únicamente con fines académicos.  
  En un entorno real se debe utilizar hashing (bcrypt / argon2).
- Cambiar siempre `SECRET_KEY` y `JWT_SECRET` en producción.
- No subir el archivo `.env` al repositorio.

---

## Autor

Frank David Cetina Pereyra  
Ingeniería en Sistemas · 2026
