from flask import Blueprint, jsonify

from . import admin_service as service

admindb_bp = Blueprint('admin_db', __name__)

@admindb_bp.route('/db/setup', methods=['POST'])
def setup():
    try:
        service.run_setup()
        return jsonify({"message": "Estructura creada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admindb_bp.route('/db/seed', methods=['POST'])
def seed():
    try:
        service.run_seed()
        return jsonify({"message": "Datos cargados con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admindb_bp.route('/db/clear', methods=['POST'])
def clear():
    try:
        service.run_clear()
        return jsonify({"message": "Base de datos limpia"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500