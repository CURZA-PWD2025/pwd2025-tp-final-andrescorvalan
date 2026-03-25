from .especialidad_controller import EspecialidadController
from flask import jsonify, request, Blueprint

especialidad_bp = Blueprint("especialidades",__name__,url_prefix='/especialidades')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas las Especialidades.
#--------------------------------------------------------------------------------------------------------
@especialidad_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        respuesta = EspecialidadController.get_all()
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        return jsonify(respuesta), 500
    except Exception as e: 
        print(f"DEBUG - Especialidades (get_all): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidades: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Especialidad.
#--------------------------------------------------------------------------------------------------------
@especialidad_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        respuesta = EspecialidadController.get_one(id)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especialidades (get_one): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidades: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para crear una Especialidad.
#--------------------------------------------------------------------------------------------------------
@especialidad_bp.route("/", methods = ["POST"])
def create() -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Petición de creación no válida.'
            }), 400
        respuesta = EspecialidadController.create(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 201
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especialidades (create): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidades: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para actualizar una Especialidad.
#--------------------------------------------------------------------------------------------------------    
@especialidad_bp.route("/<int:id>", methods = ["PUT"])
def update(id: int) -> tuple:
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'estado': 'error', 
                'mensaje': 'Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        respuesta = EspecialidadController.update(data)
        if respuesta['estado'] == 'ok':
            return jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especialidades (update): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidades: Error crítico en el servidor. Intente mas tarde.'
            }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Especialidad.
#-------------------------------------------------------------------------------------------------------- 
@especialidad_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        respuesta = EspecialidadController.delete(id)
        if respuesta['estado'] == 'ok':
            return  jsonify(respuesta), 200
        if respuesta['estado'] == 'error':
            return  jsonify(respuesta), 400
        if respuesta['estado'] == 'not_found':
            return  jsonify(respuesta), 404
        return  jsonify(respuesta), 500
    except Exception as e:
        print(f"DEBUG - Especialidades (delete): {e}")
        return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidades: Error crítico en el servidor. Intente mas tarde.'
        }), 500