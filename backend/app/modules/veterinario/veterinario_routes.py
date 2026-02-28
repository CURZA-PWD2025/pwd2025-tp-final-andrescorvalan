from .veterinario_controller import VeterinarioController
from flask import jsonify, request, Blueprint

veterinario_bp = Blueprint("veterinarios",__name__,url_prefix='/veterinarios')
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todos los Veterinarios
#--------------------------------------------------------------------------------------------------------
@veterinario_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        veterinarios = VeterinarioController.get_all()
        if veterinarios is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Veterinario: Error al intentar obtener datos de la BD.'
            }), 500
        return jsonify(veterinarios), 200
    except Exception as una_execpcion:
       return jsonify({
           'estado': 'exception', 
           'mensaje': f"Veterinario: Excepción en el servidor al intentar leer los registros ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener un Veterinario
#--------------------------------------------------------------------------------------------------------
@veterinario_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        veterinario = VeterinarioController.get_one(id)
        if veterinario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Veterinario: Error al intentar obtener datos de la BD.'
            }), 500
        if veterinario:
            return jsonify(veterinario), 200
        return jsonify({
            'estado': 'not_found',
            'mensaje': f"Veterinario: Registro con ID {id} no encontrado."
        }), 404
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Veterinario: Excepción en el servidor al intentar leer el registro ({str(una_execpcion)})."
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
                'mensaje': 'Veterinario: Petición de creación no válida.'
            }), 400
        veterinario = VeterinarioController.create(data)
        if veterinario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Veterinario: No se pudo insertar en la BD por una excepción.'
            }), 500
        if veterinario['estado'] == 'ok':
            return  jsonify(veterinario), 201
        else: # veterinario={'estado':'error'...}
            return  jsonify(veterinario), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Veterinario: Excepción en el servidor al intentar crear el nuevo registro({str(una_execpcion)})."
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
                'mensaje': 'Veterinario: Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        veterinario = VeterinarioController.update(data)
        if veterinario is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Veterinario: No se pudo actualizar en la BD por una excepción.'
            }), 500
        if veterinario['estado'] == 'ok':
            return  jsonify(veterinario), 200
        
        if veterinario['estado'] == 'not_found':
            return  jsonify(veterinario), 404

        # aqui estado=='error'
        return jsonify(veterinario), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Veterinario: Excepción en el servidor al intentar actualizar el registro ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar un Veterinario
#-------------------------------------------------------------------------------------------------------- 
@veterinario_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        veterinario = VeterinarioController.delete(id)
        if veterinario is None:
            return jsonify({
                'estado': 'exception',
                'mensaje': 'Veterinario: No se pudo eliminar de la BD por una excepción.'
            }), 500
        if veterinario['estado'] == 'ok':
            return  '', 204  
        else:
            return  jsonify(veterinario), 404
    except Exception as una_execpcion:
        return jsonify({
                'estado': 'exception',
                'mensaje': f"Veterinario: Excepción en el servidor al intentar eliminar ({str(una_execpcion)})."
            }), 500