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
    "  `dni` varchar(10) NOT NULL,"
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
    "  `matricula` varchar(9) NOT NULL,"
    "  `telefono` varchar(15) NOT NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)

TABLES['ESPECIALIDADES'] = (
    "CREATE TABLE `ESPECIALIDADES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `descripcion` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)

TABLES["VETERINARIO_ESPECIALIDAD"] = (
    "CREATE TABLE `VETERINARIO_ESPECIALIDAD` ("
    "  `veterinario_id` int(11) NOT NULL,"
    "  `especialidad_id` int(11) NOT NULL,"
    " foreign key (`veterinario_id`) references VETERINARIOS(id),"
    " foreign key (`especialidad_id`) references ESPECIALIDADES(id)"
    ") "
)

TABLES['ESPECIES'] = (
    "CREATE TABLE `ESPECIES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL UNIQUE,"
    "  `nombre_cientifico` varchar(50) NOT NULL UNIQUE,"
    "  `clase` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)

TABLES['MASCOTAS'] = (
    "CREATE TABLE `MASCOTAS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `fecha_nac` date NOT NULL,"
    "  `propietario_id` int(11) NOT NULL,"
    "  `especie_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  foreign key (`propietario_id`) references PROPIETARIOS(id),"
    "  foreign key (`especie_id`) references ESPECIES(id)"
    ") "
)

# TABLES['VACUNAS'] = (
#     "CREATE TABLE `VACUNAS` ("
#     "  `id` int(11) NOT NULL AUTO_INCREMENT,"
#     "  `nombre` varchar(50) NOT NULL UNIQUE,"
#     "  `DESCRIPCION` varchar(100) NOT NULL,"
#     "  PRIMARY KEY (`id`)"
#     ") "
# )

# TABLES["MASCOTAS_VACUNA"] = (
#     "CREATE TABLE `MASCOTAS_VACUNA` ("
#     "  `mascota_id` int(11) NOT NULL,"
#     "  `vacuna_id` int(11) NOT NULL,"
#     "  `fecha_aplicacion` date NOT NULL,"
#     "  `proxima_aplicacion` date NOT NULL,"
#     "  `observaciones` varchar(200) NOT NULL,"
#     " foreign key (`mascota_id`) references MASCOTAS(id),"
#     " foreign key (`vacuna_id`) references VACUNAS(id)"
#     ") "
# )

SEEDS['PROPIETARIOS'] = (
    "INSERT INTO PROPIETARIOS (id, nombre, apellido, dni, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Juan', 'Pérez', '30123456', '1144556677', 'juan.perez@email.com'),
        (2, 'María Laura', 'García', '28456789', '1167891234', 'ml.garcia@gmail.com'),
        (3, 'Ricardo', 'Rodríguez', '32112233', '1133445566', 'rrodriguez@outlook.com'),
        (4, 'Florencia', 'Martínez', '35987654', '1122334455', 'flo.mtz@email.com')
    ]
)

SEEDS["VETERINARIOS"] = (
    "INSERT INTO VETERINARIOS (id, nombre, apellido, matricula, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Roberto', 'Sánchez', 'MP1024', '1145678901', 'roberto.sanchez@vet.com'),
        (2, 'Elena', 'Gatti', 'MP2156', '1156789012', 'elena.gatti@clinica.com'),
        (3, 'Marcos', 'Paz', 'MP0987', '1167890123', 'mpaz_vet@hotmail.com'),
        (4, 'Julieta', 'Ortega', 'MP3342', '1178901234', 'j.ortega@vetservicios.com')
    ]
)

SEEDS['ESPECIALIDADES'] = (
    "INSERT INTO ESPECIALIDADES (id, nombre, descripcion) "
    "VALUES (%s, %s, %s)",
    [
        (1, 'Cirugía General', 'Intervenciones quirúrgicas de tejidos blandos y traumatología.'),
        (2, 'Dermatología', 'Tratamiento de afecciones de la piel y alergias.'),
        (3, 'Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón.'),
        (4, 'Clínica de Felinos', 'Especialista dedicado exclusivamente al cuidado de gatos.'),
        (5, 'Oftalmología', 'Tratamiento de patologías oculares y visión.')
    ]
)
SEEDS['VETERINARIO_ESPECIALIDAD'] = (
    "INSERT INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
    "VALUES (%s, %s)",
    [
        (1, 1), # Roberto - Cirugía
        (1, 3), # Roberto - Cardiología
        (2, 2), # Elena - Dermatología
        (2, 4), # Elena - Felinos
        (2, 5), # Elena - Oftalmología
        (3, 1)  # Marcos - Cirugía
        # El ID 4 no se agrega para que quede con 0 especialidades
    ]
)
SEEDS['ESPECIES'] = (
    "INSERT INTO ESPECIES (id, nombre, nombre_cientifico, clase) "
    "VALUES (%s, %s, %s, %s)",
    [
        (1, 'Perro', 'Canis lupus familiaris', 'Mamífero'),
        (2, 'Gato', 'Felis catus', 'Mamífero'),
        (3, 'Loro Hablador', 'Amazona aestiva', 'Ave'),
        (4, 'Tortuga de Tierra', 'Chelonoidis chilensis', 'Reptil')
    ]
)
SEEDS['MASCOTAS'] = (
    "INSERT INTO MASCOTAS (id, nombre, fecha_nac, propietario_id, especie_id) "
    "VALUES (%s, %s, %s, %s, %s)",
    [
        (1, 'Firulais', '2020-05-15', 1, 1), # Perro de Juan Pérez
        (2, 'Michi', '2021-10-20', 2, 2),    # Gato de María García
        (3, 'Paco', '2019-03-12', 3, 3),     # Loro de Ricardo Rodríguez
        (4, 'Tambor', '2022-01-05', 4, 4)    # Conejo de Florencia Martínez
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