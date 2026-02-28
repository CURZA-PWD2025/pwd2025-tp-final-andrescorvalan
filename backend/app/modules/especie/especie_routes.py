from .especie_controller import EspecieController
from flask import jsonify, request, Blueprint

especie_bp = Blueprint("especies",__name__,url_prefix='/especies')
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas las Especies.
#--------------------------------------------------------------------------------------------------------
@especie_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        especies = EspecieController.get_all()
        if especies is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especie: Error al intentar obtener datos de la BD.'
            }), 500
        return jsonify(especies), 200
    except Exception as una_execpcion:
       return jsonify({
           'estado': 'exception', 
           'mensaje': f"Especie: Excepción en el servidor al intentar leer los registros ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Especie.
#--------------------------------------------------------------------------------------------------------
@especie_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        especie = EspecieController.get_one(id)
        if especie is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especie: Error al intentar obtener datos de la BD.'
            }), 500
        if especie:
            return jsonify(especie), 200
        return jsonify({
            'estado': 'not_found',
            'mensaje': f"Especie: Registro con ID {id} no encontrado."
        }), 404
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especie: Excepción en el servidor al intentar leer el registro ({str(una_execpcion)})."
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
                'mensaje': 'Especie: Petición de creación no válida.'
            }), 400
        especie = EspecieController.create(data)
        if especie is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especie: No se pudo insertar en la BD por una excepción.'
            }), 500
        if especie['estado'] == 'ok':
            return  jsonify(especie), 201
        else: # especie={'estado':'error'...}
            return  jsonify(especie), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especie: Excepción en el servidor al intentar crear el nuevo registro({str(una_execpcion)})."
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
                'mensaje': 'Especie: Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data.

        especie = EspecieController.update(data)
        if especie is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Especie: No se pudo actualizar en la BD por una excepción.'
            }), 500
        if especie['estado'] == 'ok':
            return  jsonify(especie), 200
        
        if especie['estado'] == 'not_found':
            return  jsonify(especie), 404

        # aqui estado=='error'
        return jsonify(especie), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Especie: Excepción en el servidor al intentar actualizar el registro ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Especie.
#-------------------------------------------------------------------------------------------------------- 
@especie_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        especie = EspecieController.delete(id)
        if especie is None:
            return jsonify({
                'estado': 'exception',
                'mensaje': 'Especie: No se pudo eliminar de la BD por una excepción.'
            }), 500
        if especie['estado'] == 'ok':
            return  '', 204  
        else:
            return  jsonify(especie), 404
    except Exception as una_execpcion:
        return jsonify({
                'estado': 'exception',
                'mensaje': f"Especie: Excepción en el servidor al intentar eliminar ({str(una_execpcion)})."
            }), 500