from database.database import connect

def crear_compras(usuario_id, perfume_id, cantidad):
    connect = connect()
    cursor = connect.cursor()
    #verificar stock
    cursor.execute("SELECT stock FROM perfumes WHERE id = %s", (perfume_id))
    stock = cursor.fetchone()[0]
    if stock < cantidad:
        return {"error": "no hay suficiente stock"}, 400
    
    #crear la compra
    cursor.execute("INSERT INTO compras (usuario_id, perfume_id, cantidad) VALUES (%s, %s, %s)", (usuario_id, perfume_id, cantidad))

    #actualizar el stock
    cursor.execute("UPDATE perfumes SET stock = stock - %s WHERE id = %s",(cantidad, perfume_id))
    connect.commit()
    connect.close()
    cursor.close()
    return {"mensaje": "compra creada correctamente"}, 201

def obtener_compras_usuario(usuario_id):
    connect = connect()
    cursor = connect.cursor()
    cursor.execute("SELECT p.nombre, p.marca, c.cantidad, c.fecha FROM compras c JOIN perfumes p ON c.perfume_id = p.id WHERE c.usuario_id = %s", (usuario_id,))
    compras = cursor.fetchall()
    connect.close()
    cursor.close()
    return compras