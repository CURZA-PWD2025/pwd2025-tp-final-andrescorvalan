import mysql.connector
from mysql.connector import Error, errorcode

import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': os.getenv("DB_PORT"),
    'raise_on_warnings': True,
}
TABLES = {}
SEEDS = {}
TABLES['PROPIETARIOS'] = (
    "CREATE TABLE `PROPIETARIOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(35) NOT NULL,"
    "  `apellido` varchar(35) NOT NULL,"
    "  `dni` varchar(10) NOT NULL UNIQUE,"
    "  `telefono` varchar(15) NOT NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)
TABLES['VETERINARIOS'] = (
    "CREATE TABLE `VETERINARIOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(35) NOT NULL,"
    "  `apellido` varchar(35) NOT NULL,"
    "  `matricula` varchar(15) NOT NULL UNIQUE,"
    "  `telefono` varchar(15) NOT NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)
TABLES['ESPECIALIDADES'] = (
    "CREATE TABLE `ESPECIALIDADES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL UNIQUE,"
    "  `descripcion` varchar(100) NOT NULL,"
    "  `activa` int(1) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)
TABLES['ESPECIES'] = (
    "CREATE TABLE `ESPECIES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(35) NOT NULL UNIQUE,"
    "  `nombre_cientifico` varchar(50) NOT NULL UNIQUE,"
    "  `clase` varchar(35) NOT NULL,"
    "  `esperanza_vida` int(3) NOT NULL,"
    "  `exotica` int(1) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)
TABLES["VETERINARIO_ESPECIALIDAD"] = (
    "CREATE TABLE `VETERINARIO_ESPECIALIDAD` ("
    "  `veterinario_id` int(11) NOT NULL,"
    "  `especialidad_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`veterinario_id`, `especialidad_id`),"
    "  foreign key (`veterinario_id`) references VETERINARIOS(id) ON DELETE CASCADE,"
    "  foreign key (`especialidad_id`) references ESPECIALIDADES(id) ON DELETE RESTRICT"
    ") "
)
TABLES['MASCOTAS'] = (
    "CREATE TABLE `MASCOTAS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(35) NOT NULL,"
    "  `fecha_nac` date NOT NULL,"
    "  `sexo` ENUM('Macho', 'Hembra') NOT NULL,"
    "  `propietario_id` int(11) NOT NULL,"
    "  `especie_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  foreign key (`propietario_id`) references PROPIETARIOS(id) ON DELETE RESTRICT,"
    "  foreign key (`especie_id`) references ESPECIES(id) ON DELETE RESTRICT"
    ") "
)
TABLES['ATENCIONES'] = (
    "CREATE TABLE `ATENCIONES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `fecha` date NOT NULL,"
    "  `diagnostico` text NOT NULL,"
    "  `tratamiento` text NOT NULL,"
    "  `observaciones` text NOT NULL,"
    "  `mascota_id` int(11) NOT NULL,"
    "  `veterinario_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  foreign key (`mascota_id`) references MASCOTAS(id) ON DELETE RESTRICT,"
    "  foreign key (`veterinario_id`) references VETERINARIOS(id) ON DELETE RESTRICT"
    ") "
)
TABLES['TURNOS'] = (
    "CREATE TABLE `TURNOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `fecha_hora` datetime NOT NULL,"
    "  `estado` ENUM('Pendiente', 'Atendido', 'Ausente') NOT NULL DEFAULT 'Pendiente',"
    "  `motivo` varchar(255) NOT NULL DEFAULT '',"
    "  `mascota_id` int(11) NOT NULL,"
    "  `veterinario_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  foreign key (`mascota_id`) references MASCOTAS(id) ON DELETE RESTRICT,"
    "  foreign key (`veterinario_id`) references VETERINARIOS(id) ON DELETE RESTRICT,"
    "  UNIQUE KEY `uk_veterinario_fecha` (`veterinario_id`, `fecha_hora`)"
    ") "
)
SEEDS['PROPIETARIOS'] = (
    "INSERT INTO PROPIETARIOS (id, nombre, apellido, dni, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Juan', 'Pérez', '30123456', '1144556677', 'juan.perez@email.com'),
        (2, 'María Laura', 'García', '28456789', '1167891234', 'ml.garcia@gmail.com'),
        (3, 'Ricardo', 'Rodríguez', '32112233', '1133445566', 'rrodriguez@outlook.com'),
        (4, 'Florencia', 'Martínez', '35987654', '1122334455', 'flo.mtz@email.com'),
        (5, 'Carlos', 'Gómez', '31987456', '1155667788', 'carlos.gomez@test.com'),
        (6, 'Ana', 'Sánchez', '25123987', '1199887766', 'ana.sanchez@test.com'),
        (7, 'Beatriz', 'López', '40123123', '1122446688', 'blopez@test.com'),
        (8, 'Esteban', 'Quito', '22333444', '1133557799', 'equito@test.com'),
    ]
)
SEEDS["VETERINARIOS"] = (
    "INSERT INTO VETERINARIOS (id, nombre, apellido, matricula, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Roberto', 'Sánchez', 'MP1024', '1145678901', 'roberto.sanchez@vet.com'),
        (2, 'Elena', 'Gatti', 'MP2156', '1156789012', 'elena.gatti@clinica.com'),
    ]
)
SEEDS['ESPECIALIDADES'] = (
    "INSERT INTO ESPECIALIDADES (id, nombre, descripcion, activa) "
    "VALUES (%s, %s, %s, %s)",
    [
        (1, 'Cirugía General', 'Intervenciones quirúrgicas de tejidos blandos y traumatología.',1),
        (2, 'Odontología', 'Limpieza dental y extracciones.', 1),
        (3, 'Dermatología', 'Tratamiento de afecciones de la piel y alergias.',1),
        (4, 'Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón.',1),
        (5, 'Oftalmología', 'Tratamiento de patologías oculares y visión.',0),
        (6, 'Nutrición Animal', 'Dietas especiales para patologías crónicas.', 1),
    ]
)
SEEDS['VETERINARIO_ESPECIALIDAD'] = (
    "INSERT INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
    "VALUES (%s, %s)",
    [
        (1, 1),
        (1, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (1, 2),
    ]
)
SEEDS['ESPECIES'] = (
    "INSERT INTO ESPECIES (id, nombre, nombre_cientifico, clase, esperanza_vida, exotica) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Perro', 'Canis lupus familiaris', 'Mamífero',10,0),
        (2, 'Gato', 'Felis catus', 'Mamífero',15,0),
        (3, 'Conejo', 'Oryctolagus cuniculus', 'Mamífero', 8, 0),
        (4, 'Tortuga de Tierra', 'Chelonoidis chilensis', 'Reptil',100,1),
    ]
)
SEEDS['MASCOTAS'] = (
    "INSERT INTO MASCOTAS (id, nombre, fecha_nac, sexo, propietario_id, especie_id) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Firulais', '2020-05-15','Macho', 1, 1),
        (2, 'Michi', '2021-10-20','Hembra', 2, 2),
        (3, 'Paco', '2019-03-12','Macho', 3, 3),
        (4, 'Tambor', '2022-01-05','Hembra', 4, 4),
        (5, 'Bobby', '2020-05-15','Macho', 5, 1),
        (6, 'Biky', '2021-10-20','Hembra', 6, 2),
        (7, 'Sultán', '2019-03-12','Macho', 7, 1),
        (8, 'Negro', '2022-01-05','Macho', 8, 1),
    ]
)
SEEDS['TURNOS'] = (
    "INSERT INTO TURNOS (id, fecha_hora, estado, motivo, mascota_id, veterinario_id) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        # --- TURNOS PASADOS (Atendidos) ---
        (1, '2026-04-06 09:00:00', 'Atendido', 'Control post-cirugía', 1, 1),
        (2, '2026-04-06 09:30:00', 'Atendido', 'Limpieza dental', 7, 1),
        (3, '2026-04-07 16:30:00', 'Atendido', 'Consulta cardiológica', 2, 2),
        (4, '2026-04-07 17:30:00', 'Atendido', 'Ajuste de dieta', 6, 2),
        (5, '2026-04-08 10:00:00', 'Atendido', 'Vacunación refuerzo', 5, 1),
        (6, '2026-04-08 10:30:00', 'Atendido', 'Consulta dermatológica', 8, 1),
        # --- DÍA DE LA ENTREGA (13/04) (Pendientes) ---
        (7, '2026-04-13 09:00:00', 'Pendiente', 'Extracción dental', 1, 1),
        (8, '2026-04-13 10:00:00', 'Pendiente', 'Cirugía programada', 5, 1),
        (9, '2026-04-13 11:30:00', 'Pendiente', 'Control de puntos', 8, 1),
        (10, '2026-04-13 16:30:00', 'Pendiente', 'Ecocardiograma', 2, 2),
        (11, '2026-04-13 17:00:00', 'Pendiente', 'Control obesidad', 4, 2),
        (12, '2026-04-13 18:00:00', 'Pendiente', 'Urgencia - Tos persistente', 6, 2),
        # --- FUTUROS (Pendientes) ---
        (13, '2026-04-14 09:30:00', 'Pendiente', 'Chequeo general', 3, 1),
        (14, '2026-04-15 16:30:00', 'Pendiente', 'Evaluación cardíaca', 2, 2),
    ]
)
SEEDS['ATENCIONES'] = (
    "INSERT INTO ATENCIONES (id, fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
    [
        (1, '2026-04-06', 'Herida sana', 'Continuar faja', 'Sin signos de infección.', 1, 1),
        (2, '2026-04-06', 'Sarro moderado', 'Limpieza profunda', 'Se recomienda cepillado.', 7, 1),
        (3, '2026-04-07', 'Soplo grado II', 'Enalapril', 'Michi debe evitar el estrés.', 2, 2),
        (4, '2026-04-07', 'Sobrepeso', 'Dieta controlada', 'Biky bajó 100g.', 6, 2),
        (5, '2026-04-08', 'Salud óptima', 'Vacuna Rabia', 'Bobby pesó 12kg.', 5, 1),
        (6, '2026-04-08', 'Alergia leve', 'Champú especial', 'Piel irritada en abdomen.', 8, 1),
    ]
)

def create_database(cursor):
    try:
        cursor.execute(
        f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'", )
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database already exists")
        else:
            print(err)
    else:
        print(f"Database {DB_NAME} created successfully.")

def create_tables(tables, cursor):
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print(f"Creating table {table_name}: ", end="")
            cursor.execute(table_description)
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def seeds_tables(seed, cursor):
    for table_name in seed:
        seed_description = seed[table_name]
        try:
            print(f"Seeding table {table_name}: ", end="")
            cursor.executemany(seed_description[0], seed_description[1])
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

if __name__ == "__main__":
    cxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cxn.cursor()
    create_database(cursor)
    cursor.close()
    cxn.close()

    CONF_DB = DB_CONFIG.copy()
    CONF_DB['database'] = DB_NAME
    cxn = mysql.connector.connect(**CONF_DB)
    cursor = cxn.cursor()
    create_tables(TABLES, cursor)
    seeds_tables(SEEDS, cursor)
    cxn.commit()
    cursor.close()
    cxn.close() 