from .veterinario_controller import VeterinarioController
from flask import jsonify, request, Blueprint

veterinario_bp = Blueprint("veterinarios",__name__,url_prefix='/veterinarios')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los Veterinarios
#--------------------------------------------------------------------------------------------------------
@veterinario_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = VeterinarioController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Veterinarios (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener un Veterinario
#--------------------------------------------------------------------------------------------------------
@veterinario_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = VeterinarioController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Veterinarios (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear un Veterinario
#--------------------------------------------------------------------------------------------------------
@veterinario_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = VeterinarioController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Veterinarios (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar un Veterinario
#--------------------------------------------------------------------------------------------------------    
@veterinario_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = VeterinarioController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Veterinarios (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar un Veterinario
#-------------------------------------------------------------------------------------------------------- 
@veterinario_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = VeterinarioController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Veterinarios (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Error crítico en el servidor. Intente mas tarde.'
        }), 500