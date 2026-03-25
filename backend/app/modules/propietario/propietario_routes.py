from .propietario_controller import PropietarioController
from flask import jsonify, request, Blueprint

propietario_bp = Blueprint("propietarios",__name__,url_prefix='/propietarios')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los Propietarios.
#--------------------------------------------------------------------------------------------------------
@propietario_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = PropietarioController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Propietarios (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietarios: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener un Propietario.
#--------------------------------------------------------------------------------------------------------
@propietario_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = PropietarioController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Propietarios (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietarios: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear un Propietario.
#--------------------------------------------------------------------------------------------------------
@propietario_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = PropietarioController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Propietarios (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietarios: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar un Propietario.
#--------------------------------------------------------------------------------------------------------    
@propietario_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = PropietarioController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Propietarios (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietarios: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar un Propietario.
#-------------------------------------------------------------------------------------------------------- 
@propietario_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = PropietarioController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Propietarios (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietarios: Error crítico en el servidor. Intente mas tarde.'
        }), 500