from .atencion_controller import AtencionController
from flask import jsonify, request, Blueprint

atencion_bp = Blueprint("atenciones",__name__,url_prefix='/atenciones')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas los Atenciones.
#--------------------------------------------------------------------------------------------------------
@atencion_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = AtencionController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Atenciones (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Atencion.
#--------------------------------------------------------------------------------------------------------
@atencion_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = AtencionController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Atenciones (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas las atenciones de una mascota específica (Historial).
#--------------------------------------------------------------------------------------------------------
@atencion_bp.route("/mascota/<int:mascota_id>", methods=["GET"])
def get_by_mascota(mascota_id: int) -> tuple:
    try:
        respuesta = AtencionController.get_by_mascota(mascota_id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Atenciones (get_by_mascota): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico al recuperar el historial.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear una Atencion
#--------------------------------------------------------------------------------------------------------
@atencion_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = AtencionController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Atenciones (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar una Atencion.
#--------------------------------------------------------------------------------------------------------    
@atencion_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = AtencionController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Atenciones (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico en el servidor. Intente más tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Atencion
#-------------------------------------------------------------------------------------------------------- 
@atencion_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = AtencionController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Atenciones (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Atenciones: Error crítico en el servidor. Intente más tarde.'
        }), 500