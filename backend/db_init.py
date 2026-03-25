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
        (8, 'Esteban', 'Quito', '22333444', '1133557799', 'equito@test.com')
    ]
)

SEEDS["VETERINARIOS"] = (
    "INSERT INTO VETERINARIOS (id, nombre, apellido, matricula, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Roberto', 'Sánchez', 'MP1024', '1145678901', 'roberto.sanchez@vet.com'),
        (2, 'Elena', 'Gatti', 'MP2156', '1156789012', 'elena.gatti@clinica.com'),
        (3, 'Marcos', 'Paz', 'MP0987', '1167890123', 'mpaz_vet@hotmail.com'),
        (4, 'Julieta', 'Ortega', 'MP3342', '1178901234', 'j.ortega@vetservicios.com'),
        (5, 'Lucía', 'Fernández', 'MP4455', '1188776655', 'lucia.f@vet.com'),
        (6, 'Daniel', 'Ríos', 'MP6677', '1122112211', 'drios_veterinaria@test.com'),
        (7, 'Sofía', 'Castro', 'MP8899', '1144332211', 'scastro.vet@test.com')
    ]
)

SEEDS['ESPECIALIDADES'] = (
    "INSERT INTO ESPECIALIDADES (id, nombre, descripcion, activa) "
    "VALUES (%s, %s, %s, %s)",
    [
        (1, 'Cirugía General', 'Intervenciones quirúrgicas de tejidos blandos y traumatología.',1),
        (2, 'Dermatología', 'Tratamiento de afecciones de la piel y alergias.',1),
        (3, 'Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón.',1),
        (4, 'Clínica de Felinos', 'Especialista dedicado exclusivamente al cuidado de gatos.',1),
        (5, 'Oftalmología', 'Tratamiento de patologías oculares y visión.',0),
        (6, 'Nutrición Animal', 'Dietas especiales para patologías crónicas.', 1),
        (7, 'Fisioterapia', 'Rehabilitación post-quirúrgica y dolores crónicos.', 1),
        (8, 'Odontología', 'Limpieza dental y extracciones.', 1)
    ]
)
SEEDS['VETERINARIO_ESPECIALIDAD'] = (
    "INSERT INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
    "VALUES (%s, %s)",
    [
        (1, 1),
        (1, 3),
        (2, 2),
        (2, 4),
        (2, 5),
        (3, 1)
    ]
)
SEEDS['ESPECIES'] = (
    "INSERT INTO ESPECIES (id, nombre, nombre_cientifico, clase, esperanza_vida, exotica) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Perro', 'Canis lupus familiaris', 'Mamífero',10,0),
        (2, 'Gato', 'Felis catus', 'Mamífero',15,0),
        (3, 'Loro Hablador', 'Amazona aestiva', 'Ave',30,0),
        (4, 'Tortuga de Tierra', 'Chelonoidis chilensis', 'Reptil',100,1),
        (5, 'Conejo', 'Oryctolagus cuniculus', 'Mamífero', 8, 0),
        (6, 'Hámster', 'Cricetinae', 'Mamífero', 2, 0),
        (7, 'Iguana Verde', 'Iguana iguana', 'Reptil', 20, 1)
    ]
)
SEEDS['MASCOTAS'] = (
    "INSERT INTO MASCOTAS (id, nombre, fecha_nac, sexo, propietario_id, especie_id) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        (1, 'Firulais', '2020-05-15','Macho', 1, 1),
        (2, 'Michi', '2021-10-20','Hembra', 2, 2),
        (3, 'Paco', '2019-03-12','Macho', 3, 3),
        (4, 'Tambor', '2022-01-05','Hembra', 4, 4)
    ]
)

SEEDS['ATENCIONES'] = (
    "INSERT INTO ATENCIONES (id, fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
    [
        (1, '2026-01-10', 'Control anual y vacunación.', 'Se aplica vacuna Quíntuple y Rabia. Refuerzo en un año.', 'Paciente en buen estado general.', 1, 1),
        (2, '2026-02-05', 'Infección urinaria leve.', 'Cefalexina 500mg: 1 comprimido cada 12hs por 7 días.\nAbundante agua.', 'Realizar análisis de orina si no mejora en 48hs.', 2, 2),
        (3, '2026-02-15', 'Otitis externa en oído derecho.', 'Limpieza con solución fisiológica.\nGotas Otiflex: 3 gotas cada 8hs por 10 días.', 'Se recomienda uso de collar isabelino.', 3, 3),
        (4, '2026-03-01', 'Desparasitación interna y externa.', 'Pipeta contra pulgas y garrapatas.\nPastilla antiparasitaria según peso (5kg).', 'Próxima aplicación en 30 días.', 4, 4),
        (5, '2026-03-05', 'Gastroenteritis por cambio de dieta.', 'Dieta blanda (pollo y arroz) por 48hs.\nReliverán: 5 gotas cada 8hs si hay vómitos.', 'El propietario indica que comió alimento nuevo.', 1, 2),
        (6, '2026-03-10', 'Control de peso.', 'Cambio a alimento light.', 'Bajó 200gr respecto al mes pasado.', 1, 1),
        (7, '2026-03-12', 'Limpieza de herida.', 'Curación con yodo.', 'Herida pequeña en pata trasera.', 2, 2),
        (8, '2026-03-15', 'Vacunación refuerzo.', 'Séxtuple aplicada.', 'Sin reacciones adversas.', 1, 3),
        (9, '2026-03-18', 'Consulta por picazón.', 'Apoquel 5.4mg.', 'Posible alergia estacional.', 1, 1),
        (10, '2026-03-20', 'Corte de uñas y limpieza.', 'Servicio estético.', 'Paciente muy tranquilo.', 2, 4),
        (11, '2026-03-22', 'Control post-cirugía.', 'Retiro de puntos.', 'Cicatrización perfecta.', 3, 1),
        (12, '2026-03-25', 'Análisis de sangre.', 'Extracción de muestra.', 'Resultados en 24hs.', 1, 2),
        (13, '2026-03-26', 'Ecografía abdominal.', 'Estudio por imagen.', 'No se observan anomalías.', 2, 1),
        (14, '2026-03-28', 'Desparasitación periódica.', 'Pastilla Total Full.', 'Se entrega recordatorio.', 1, 4),
        (15, '2026-03-30', 'Urgencia - Vómitos.', 'Suero fisiológico.', 'Queda en observación 2 horas.', 1, 2)
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