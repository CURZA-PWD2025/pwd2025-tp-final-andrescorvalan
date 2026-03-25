from .mascota_controller import MascotaController
from flask import jsonify, request, Blueprint

mascota_bp = Blueprint("mascotas",__name__,url_prefix='/mascotas')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas los Mascotas.
#--------------------------------------------------------------------------------------------------------
@mascota_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = MascotaController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Mascotas (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascotas: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Mascota.
#--------------------------------------------------------------------------------------------------------
@mascota_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = MascotaController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Mascotas (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascotas: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear una Mascota
#--------------------------------------------------------------------------------------------------------
@mascota_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = MascotaController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Mascotas (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascotas: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar una Mascota.
#--------------------------------------------------------------------------------------------------------    
@mascota_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = MascotaController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Mascotas (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascotas: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Mascota
#-------------------------------------------------------------------------------------------------------- 
@mascota_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = MascotaController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Mascotas (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascotas: Error crítico en el servidor. Intente más tarde.'
        }), 500