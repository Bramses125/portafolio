from database.database import connect

def get_perfumes():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM perfumes")
    perfumes = cursor.fetchall()
    connection.close()
    cursor.close()
    return perfumes

def get_perfume(id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM perfumes WHERE id = %s", (id,))
    perfumes = cursor.fetchone()
    connection.close()
    cursor.close()
    if perfumes is None:
        return {"error": "perfume no encontrado"}, 404
    return perfumes

def post_perfume(data):
    nombre = data.get('nombre')
    marca = data.get('marca')
    precio = data.get('precio')
    stock = data.get('stock')
    ml = data.get('ml')

    if not nombre or not marca or not precio or not stock or not ml:
        return {"error": "Faltan datos"}, 400
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO perfumes (nombre, marca, precio, stock, ml) VALUES (%s, %s, %s, %s, %s)", (nombre, marca, precio, stock, ml))
    connection.commit()
    connection.close()
    cursor.close()
    return {"message": "perfume creado correctamente"}, 201

def put_perfume(id, data):
    nombre = data.get('nombre')
    marca = data.get('marca')
    precio = data.get('precio')
    stock = data.get('stock')
    ml = data.get('ml')

    connect = connect()
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE perfumes SET nombre = %s, marca = %s, precio = %s, stock = %s, ml = %s WHERE id = %s",
        (nombre, marca, precio, stock, ml, id)
    )
    connect.commit()
    cursor.close()
    connect.close()
    return {"mensaje": "Perfume actualizado correctamente"}

def delete_perfume(id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM perfumes WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"mensaje": "Perfume eliminado correctamente"}