from .especialidad_controller import EspecialidadController
from flask import jsonify, request, Blueprint

especialidad_bp = Blueprint("especialidades",__name__,url_prefix='/especialidades')
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas las Especialidades.
#--------------------------------------------------------------------------------------------------------
@especialidad_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        especialidades = EspecialidadController.get_all()
        if especialidades is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidad: Error al intentar obtener datos de la BD.'
            }), 500
        return jsonify(especialidades), 200
    except Exception as una_execpcion:
       return jsonify({
           'estado': 'exception', 
           'mensaje': f"Especialidad: Excepción en el servidor al intentar leer los registros ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Especialidad.
#--------------------------------------------------------------------------------------------------------
@especialidad_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        especialidad = EspecialidadController.get_one(id)
        if especialidad is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidad: Error al intentar obtener datos de la BD.'
            }), 500
        if especialidad:
            return jsonify(especialidad), 200
        return jsonify({
            'estado': 'not_found',
            'mensaje': f"Especialidad: Registro con ID {id} no encontrado."
        }), 404
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especialidad: Excepción en el servidor al intentar leer el registro ({str(una_execpcion)})."
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
                'mensaje': 'Especialidad: Petición de creación no válida.'
            }), 400
        especialidad = EspecialidadController.create(data)
        if especialidad is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidad: No se pudo insertar en la BD por una excepción.'
            }), 500
        if especialidad['estado'] == 'ok':
            return  jsonify(especialidad), 201
        else: # especialidad={'estado':'error'...}
            return  jsonify(especialidad), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especialidad: Excepción en el servidor al intentar crear el nuevo registro({str(una_execpcion)})."
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
                'mensaje': 'Especialidad: Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data.

        especialidad = EspecialidadController.update(data)
        if especialidad is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especialidad: No se pudo actualizar en la BD por una excepción.'
            }), 500
        if especialidad['estado'] == 'ok':
            return  jsonify(especialidad), 200
        
        if especialidad['estado'] == 'not_found':
            return  jsonify(especialidad), 404

        # aqui estado=='error'
        return jsonify(especialidad), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especialidad: Excepción en el servidor al intentar actualizar el registro ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Especialidad.
#-------------------------------------------------------------------------------------------------------- 
@especialidad_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        especialidad = EspecialidadController.delete(id)
        if especialidad is None:
            return jsonify({
                'estado': 'exception',
                'mensaje': 'Especialidad: No se pudo eliminar de la BD por una excepción.'
            }), 500
        if especialidad['estado'] == 'ok':
            return  '', 204  
        else:
            return  jsonify(especialidad), 404
    except Exception as una_execpcion:
        return jsonify({
                'estado': 'exception',
                'mensaje': f"Especialidad: Excepción en el servidor al intentar eliminar ({str(una_execpcion)})."
            }), 500