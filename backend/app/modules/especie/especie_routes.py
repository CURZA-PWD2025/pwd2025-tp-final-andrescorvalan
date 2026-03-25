from .especie_controller import EspecieController
from flask import jsonify, request, Blueprint

especie_bp = Blueprint("especies",__name__,url_prefix='/especies')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas las Especies.
#--------------------------------------------------------------------------------------------------------
@especie_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = EspecieController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Especies (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especies: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Especie.
#--------------------------------------------------------------------------------------------------------
@especie_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = EspecieController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especies (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especies: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear una Especie.
#--------------------------------------------------------------------------------------------------------
@especie_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = EspecieController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especies (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especies: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar una Especie.
#--------------------------------------------------------------------------------------------------------    
@especie_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = EspecieController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especies (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especies: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Especie.
#-------------------------------------------------------------------------------------------------------- 
@especie_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = EspecieController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especies (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especies: Error crítico en el servidor. Intente mas tarde.'
        }), 500