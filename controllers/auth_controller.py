from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from database.database import connect

def register_user(username, password, role="user"):
    connection = connect()
    cursor = connection.cursor()
    # verificacion de usuario ya existente
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    if cursor.fetchone():
        return {"error": "el usuario ya existe"}, 400
    # crear el usuario
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
    connection.commit()
    connection.close()
    cursor.close()
    return {"message": "usuario creado correctamente"}, 201

def login_user(username, password):
    connection = connect()
    cursor = connection.cursor()
    # buscar el usuario en la base de datos 
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    user = cursor.fetchone()
    connection.close()
    cursor.close()

    if user and check_password_hash(user[1], password):
        # crear el token de acceso
        access_token = create_access_token(identity=user[0], additional_claims={"role": user[2]})
        return {"access_token": access_token}, 200
    else:
        return {"error": "usuario o contraseña incorrectos"}, 400