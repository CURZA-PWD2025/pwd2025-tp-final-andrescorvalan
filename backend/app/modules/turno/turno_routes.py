from .turno_controller import TurnoController
from flask import jsonify, request, Blueprint

turno_bp = Blueprint("turnos",__name__,url_prefix='/turnos')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los Turnos.
#--------------------------------------------------------------------------------------------------------
@turno_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = TurnoController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Turnos (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener un Turno.
#--------------------------------------------------------------------------------------------------------
@turno_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta =TurnoController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los turnos futuros, y los pasados del día actual.
#--------------------------------------------------------------------------------------------------------
@turno_bp.route("proximos/", methods=["GET"])
def get_proximos_turnos() -> tuple:
    try:
        respuesta =TurnoController.proximos_turnos()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (get_proximos_turnos): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico al recuperar los turnos futuros.'
            }), 500
# @turno_bp.route("/historial", methods=["GET"])
@turno_bp.route("historial/", methods=["GET"])
def get_historial_turnos() -> tuple:
    try:
        respuesta =TurnoController.historial_turnos()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (get_historial_turnos): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico al recuperar los turnos pasados.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear un Turno
#--------------------------------------------------------------------------------------------------------
@turno_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta =TurnoController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar un Turno.
#--------------------------------------------------------------------------------------------------------    
@turno_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta =TurnoController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar un Turno.
#-------------------------------------------------------------------------------------------------------- 
@turno_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta =TurnoController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Turnos (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Turnos: Error crítico en el servidor. Intente más tarde.'
        }), 500