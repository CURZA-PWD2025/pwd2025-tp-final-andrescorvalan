from flask import Blueprint, jsonify

from . import admin_service as service

admindb_bp = Blueprint('admin_db', __name__)

@admindb_bp.route('/db/setup', methods=['POST'])
def setup():
    try:
        service.run_setup()
        return jsonify({
            "estado": "ok", 
            "mensaje": "Base de Datos creada con éxito."
            }), 200
    except Exception as e:
        print(f"AdminDB Setup Exception: {e}")
        return jsonify({
            "estado": "exception", 
            "mensaje": "Error crítico al crear la base de datos."
            }), 500

@admindb_bp.route('/db/seed', methods=['POST'])
def seed():
    try:
        service.run_seed()
        return jsonify({
                "estado": "ok", 
                "mensaje": "Estructura creada y datos cargados con éxito."
            }), 200
    except Exception as e:
        print(f"AdminDB Seed Exception: {e}")
        return jsonify({
            "estado": "exception", 
            "mensaje": "Error crítico al cargar datos de ejemplo."
        }), 500

@admindb_bp.route('/db/clear', methods=['POST'])
def clear():
    try:
        service.run_clear()
        return jsonify({
            "estado": "ok", 
            "mensaje": "Base de datos eliminada con éxito."
        }), 200
    except Exception as e:
        print(f"AdminDB Clear Exception: {e}")
        return jsonify({
            "estado": "exception", 
            "mensaje": "Error crítico al intentar eliminar la base de datos."
        }), 500