# Aplicación Android + Backend en Python
Este proyecto está compuesto por dos partes principales:

Backend (Python): Encargado de procesar las peticiones realizadas por la app móvil. Repositorio disponible aquí:.

Frontend (Java - Android): Aplicación Android desarrollada en Java, que representa la interfaz visible para el usuario. Repositorio disponible aquí: [FCTProject](https://github.com/MarcosPatron/FCTProject).

### Cómo ejecutar la aplicación:

Instalar las dependencias del fichero requirements.txt y ejecutar run.py con python.

### Necesario para la ejecución correcta:

Creacion la base de datos especificada en este fichero en MySQL, y generar un fichero .env en la carpeta principal del proyecto con los datos para la conexión a la base de datos con el siguiente formato:
```
OPENAI_API_KEY=
DB_HOST= localhost o la IP en cuestión
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_bbdd
```
**Script Base de Datos**:

```sql
DROP DATABASE IF EXISTS sistema_soporte;
CREATE DATABASE sistema_soporte CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_soporte;

-- Tabla de logs
CREATE TABLE LOGS (
    LOGSID INT AUTO_INCREMENT PRIMARY KEY,
    MENSAJE VARCHAR(1000) NOT NULL,
    DESCRIPCION TEXT,
    TIPO_LOG VARCHAR(20) NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    OBJETO VARCHAR(100) NOT NULL,
    METODO VARCHAR(100) NOT NULL
);

-- Tabla de usuarios
CREATE TABLE USERS (
    USERSID INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(50) UNIQUE NOT NULL,
    FULLNAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(10),
    PASSWORD VARCHAR(255) NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla de hilos (conversaciones)
CREATE TABLE THREADS (
    THREADSID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL,
    PROVIDER VARCHAR(100) NOT NULL,
    PROMPT_TOKENS INT,
    COMPLETION_TOKENS INT,
    TOTAL_TOKENS INT,
    STATUS VARCHAR(100) NOT NULL,
    ID_THREAD VARCHAR(128),
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    DESCRIPTION VARCHAR(200),
    FOREIGN KEY (USER_ID) REFERENCES USERS(USERSID)
);

-- Tabla de mensajes
CREATE TABLE MESSAGES (
    MESSAGESID INT AUTO_INCREMENT PRIMARY KEY,
    THREAD_ID INT NOT NULL,
    TYPE VARCHAR(100),
    CONTENT TEXT,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (THREAD_ID) REFERENCES THREADS(THREADSID)
);

-- Tabla de archivos adjuntos
CREATE TABLE ATTACHMENTS (
    ATTACHMENTSID INT AUTO_INCREMENT PRIMARY KEY,
    THREAD_ID INT NOT NULL,
    FILENAME VARCHAR(250) NOT NULL,
    CONTENT_TYPE VARCHAR(100) NOT NULL,
    FILE_CONTENT LONGBLOB NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (THREAD_ID) REFERENCES THREADS(THREADSID)
);

-- Tabla de tickets de soporte
CREATE TABLE TICKETS_SOPORTE (
    TICKET_ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL,
    DESCRIPCION TEXT NOT NULL,
    CATEGORIA ENUM('Cuenta', 'Asistente', 'Tecnicos') DEFAULT 'Tecnicos',
    PRIORIDAD ENUM('baja', 'media', 'alta') DEFAULT 'media',
    ESTADO ENUM('abierto', 'en_progreso', 'cerrado') DEFAULT 'abierto',
    RESPUESTA TEXT,
    CREADO_EN DATETIME DEFAULT CURRENT_TIMESTAMP,
    ACTUALIZADO_EN DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (USER_ID) REFERENCES USERS(USERSID)
);

-- Crear usuario invitado (Debe estar creado, ya que se toma por defecto si no está la sesión iniciada)
INSERT INTO USERS (USERNAME, FULLNAME, EMAIL, TELEFONO, PASSWORD)
VALUES ('invitado', 'Usuario Invitado', 'invitado@example.com', '000000000', '00000');
```
