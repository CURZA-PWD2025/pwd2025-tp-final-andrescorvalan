from .mascota_controller import MascotaController
from flask import jsonify, request, Blueprint

mascota_bp = Blueprint("mascotas",__name__,url_prefix='/mascotas')

#--------------------------------------------------------------------------------------------------------
# Ruta para obtener todas los Mascotas.
#--------------------------------------------------------------------------------------------------------
@mascota_bp.route("/", methods=["GET"])
def get_all() -> tuple:
    try:
        mascotas = MascotaController.get_all()
        print(mascotas)
        if mascotas is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascota: Error al intentar obtener datos de la BD.'
            }), 500
        return jsonify(mascotas), 200
    except Exception as una_execpcion:
       return jsonify({
           'estado': 'exception', 
           'mensaje': f"Mascota: Excepción en el servidor al intentar leer los registros ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para obtener una Mascota.
#--------------------------------------------------------------------------------------------------------
@mascota_bp.route("/<int:id>", methods=["GET"])
def get_one(id: int) -> tuple:
    try:
        mascota = MascotaController.get_one(id)
        if mascota is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascota: Error al intentar obtener datos de la BD.'
            }), 500
        if mascota:
            return jsonify(mascota), 200
        return jsonify({
            'estado': 'not_found',
            'mensaje': f"Mascota: Registro con ID {id} no encontrada."
        }), 404
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Mascota: Excepción en el servidor al intentar leer el registro ({str(una_execpcion)})."
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
                'mensaje': 'Mascota: Petición de creación no válida.'
            }), 400
        mascota = MascotaController.create(data)
        if mascota is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascota: No se pudo insertar en la BD por una excepción.'
            }), 500
        if mascota['estado'] == 'ok':
            return  jsonify(mascota), 201
        else: # mascota={'estado':'error'...}
            return  jsonify(mascota), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Mascota: Excepción en el servidor al intentar crear el nuevo registro({str(una_execpcion)})."
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
                'mensaje': 'Mascota: Petición de actualización no válida.'
            }), 400
       
        data['id'] = id     # Por si el id no esta en data

        mascota = MascotaController.update(data)
        if mascota is None:
            return jsonify({
                'estado': 'exception', 
                'mensaje': 'Mascota: No se pudo actualizar en la BD por una excepción.'
            }), 500
        if mascota['estado'] == 'ok':
            return  jsonify(mascota), 200
        
        if mascota['estado'] == 'not_found':
            return  jsonify(mascota), 404

        # aqui estado=='error'
        return jsonify(mascota), 400
    except Exception as una_execpcion:
        return jsonify({
            'estado': 'exception', 
            'mensaje': f"Mascota: Excepción en el servidor al intentar actualizar el registro ({str(una_execpcion)})."
        }), 500
#--------------------------------------------------------------------------------------------------------
# Ruta para eliminar una Mascota
#-------------------------------------------------------------------------------------------------------- 
@mascota_bp.route("/<int:id>", methods = ["DELETE"])
def delete(id: int) -> tuple:
    try:
        mascota = MascotaController.delete(id)
        if mascota is None:
            return jsonify({
                'estado': 'exception',
                'mensaje': 'Mascota: No se pudo eliminar de la BD por una excepción.'
            }), 500
        if mascota['estado'] == 'ok':
            return  '', 204  
        else:
            return  jsonify(mascota), 404
    except Exception as una_execpcion:
        return jsonify({
                'estado': 'exception',
                'mensaje': f"Mascota: Excepción en el servidor al intentar eliminar ({str(una_execpcion)})."
            }), 500