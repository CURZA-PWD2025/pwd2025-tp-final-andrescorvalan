from .propietario_controller import PropietarioController
from flask import jsonify, request, Blueprint

propietario_bp = Blueprint("propietarios",__name__,url_prefix='/propietarios')
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los Propietarios.
#--------------------------------------------------------------------------------------------------------
@propietario_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        propietarios = PropietarioController.get_all()
        if propietarios is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietario: Error al intentar obtener datos de la BD.'
            }), 500
        return jsonify(propietarios), 200
    except Exception as una_execpcion:
       return jsonify({
           'estado': 'exception', 
           'mensaje': f"Propietario: Excepción en el servidor al intentar leer los registros ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener un Propietario.
#--------------------------------------------------------------------------------------------------------
@propietario_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        propietario = PropietarioController.get_one(id)
        if propietario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietario: Error al intentar obtener datos de la BD.'
            }), 500
        if propietario:
            return jsonify(propietario), 200
        return jsonify({
            'estado': 'not_found',
            'mensaje': f"Propietario: Registro con ID {id} no encontrado."
        }), 404
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Propietario: Excepción en el servidor al intentar leer el registro ({str(una_execpcion)})."
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
                'mensaje': 'Propietario: Petición de creación no válida.'
            }), 400
        propietario = PropietarioController.create(data)
        if propietario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietario: No se pudo insertar en la BD por una excepción.'
            }), 500
        if propietario['estado'] == 'ok':
            return  jsonify(propietario), 201
        else: # propietario={'estado':'error'...}
            return  jsonify(propietario), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Propietario: Excepción en el servidor al intentar crear el nuevo registro({str(una_execpcion)})."
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
                'mensaje': 'Propietario: Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        propietario = PropietarioController.update(data)
        if propietario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Propietario: No se pudo actualizar en la BD por una excepción.'
            }), 500
        if propietario['estado'] == 'ok':
            return  jsonify(propietario), 200
        
        if propietario['estado'] == 'not_found':
            return  jsonify(propietario), 404

        # aqui estado=='error'
        return jsonify(propietario), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Propietario: Excepción en el servidor al intentar actualizar el registro ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar un Propietario.
#-------------------------------------------------------------------------------------------------------- 
@propietario_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        propietario = PropietarioController.delete(id)
        if propietario is None:
            return jsonify({
                'estado': 'exception',
                'mensaje': 'Propietario: No se pudo eliminar de la BD por una excepción.'
            }), 500
        if propietario['estado'] == 'ok':
            return  '', 204  
        else:
            return  jsonify(propietario), 404
    except Exception as una_execpcion:
        return jsonify({
                'estado': 'exception',
                'mensaje': f"Propietario: Excepción en el servidor al intentar eliminar ({str(una_execpcion)})."
            }), 500