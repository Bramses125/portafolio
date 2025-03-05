from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from database.database import connect
def register_user(username, password, role="user"):
    connection = connect()
    cursor = connection.cursor()
    # Verificación de usuario ya existente
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    if cursor.fetchone():
        return {"error": "el usuario ya existe"}, 400
    # Crear el usuario
    hashed_password = generate_password_hash(password)
    print("Contraseña original:", password)  
    print("Contraseña hasheada:", hashed_password) 
    cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
    connection.commit()
    connection.close()
    cursor.close()
    return {"message": "usuario creado correctamente"}, 201

def login_user(username, password):
    connection = connect()
    cursor = connection.cursor()
    # Buscar el usuario en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    user = cursor.fetchone()
    connection.close()
    cursor.close()

    
    print("Usuario encontrado:", user) 
    if user:
        print("Contraseña hash en la base de datos:", user[2]) 
        print("Contraseña proporcionada:", password)  

    # Verificar si el usuario existe y si la contraseña coincide
    if user and check_password_hash(user[2], password):  
        # Crear el token de acceso
        access_token = create_access_token(identity=str(user[0]), additional_claims={"role": str(user[3])})
        return {"access_token": access_token}, 200
    else:
        return {"error": "usuario o contraseña incorrectos"}, 400