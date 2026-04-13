from flask import Flask
from flask_cors import CORS

from .modules.propietario.propietario_routes import propietario_bp
from .modules.veterinario.veterinario_routes import veterinario_bp
from .modules.especie.especie_routes import especie_bp
from .modules.mascota.mascota_routes import mascota_bp
from .modules.especialidad.especialidad_routes import especialidad_bp
from .modules.admindb.admindb_routes import admindb_bp
from .modules.atencion.atencion_routes import atencion_bp
from .modules.turno.turno_routes import turno_bp



def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.register_blueprint(propietario_bp)
    app.register_blueprint(veterinario_bp)
    app.register_blueprint(especie_bp)
    app.register_blueprint(mascota_bp)
    app.register_blueprint(especialidad_bp)
    app.register_blueprint(admindb_bp)
    app.register_blueprint(atencion_bp)
    app.register_blueprint(turno_bp)

    # Ruta de prueba
    @app.route('/')
    def home():
        return "<h1>TP Final de PWD (flask)</h1>"

    return app
