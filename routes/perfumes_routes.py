from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from controllers.auth_controller import register_user, login_user
from controllers.perfumes_controller import (
    get_perfume,get_perfumes, put_perfume, post_perfume, delete_perfume
)
from controllers.compras_controller import crear_compras, obtener_compras_usuario

def configure_routes(app):
    #resgistro de usuario
    @app.route("/register", methods=["POST"])
    def route_register():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        role = data.get("role","user") #por defecto el rol es user
        return register_user(username, password, role)
    
    #login de usuario
    @app.route("/login",methods=["POST"])
    def route_login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        return login_user(username, password)
    
    #obtener todos los perfumes
    @app.route("/perfumes", methods=["GET"])
    def route_get_perfumes():
        perfumes = get_perfumes()
        return jsonify(perfumes)
    
    #obtener un perfume por id 
    @app.route("/perfumes/<int:id>", methods=["GET"])
    def route_get_perfume(id):
        perfume = get_perfume(id)
        if isinstance(perfume, tuple) and perfume[1] == 404:
            return jsonify(perfume[0]), 404
        return jsonify(perfume)
    
    #crear nuevo perfume
    @app.route("/perfumes", methods=["POST"])
    @jwt_required()
    def route_post_perfume():
       claims = get_jwt() #obtener los claims del token
       if claims["role"] != "admin":
                       return {"error": "no tienes permisos para realizar esta acción"}, 403
       data = request.get_json()
       resultado = post_perfume(data)
       return jsonify(resultado[0]), resultado[1]
    
      # Actualizar un perfume por ID (solo admin)
    @app.route('/perfumes/<int:id>', methods=['PUT'])
    @jwt_required()
    def route_actualizar_perfume(id):
        claims = get_jwt()
        if claims["role"] != "admin":
            return {"error": "Acceso denegado"}, 403

        data = request.get_json()
        resultado = put_perfume(id, data)
        return jsonify(resultado)

    # Eliminar un perfume por ID (solo admin)
    @app.route('/perfumes/<int:id>', methods=['DELETE'])
    @jwt_required()
    def route_eliminar_perfume(id):
        claims = get_jwt()
        if claims["role"] != "admin":
            return {"error": "Acceso denegado"}, 403

        resultado = delete_perfume(id)
        return jsonify(resultado)

    # Realizar una compra (requiere autenticación)
    @app.route('/compras', methods=['POST'])
    @jwt_required()
    def route_crear_compra():
        data = request.get_json()
        usuario_id = get_jwt_identity()
        perfume_id = data.get('perfume_id')
        cantidad = data.get('cantidad')
        return crear_compras(usuario_id, perfume_id, cantidad)

    # Obtener compras del usuario (requiere autenticación)
    @app.route('/compras', methods=['GET'])
    @jwt_required()
    def route_obtener_compras_usuario():
        usuario_id = get_jwt_identity()
        compras = obtener_compras_usuario(usuario_id)
        return jsonify(compras)
        