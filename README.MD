## Endpoints

### Usuarios
- **POST** `/registro`: Registra un nuevo usuario.
- **POST** `/login`: Autentica un usuario y obtén un token JWT.

### Perfumes
- **GET** `/perfumes`: Obtén todos los perfumes.
- **GET** `/perfumes/<id>`: Obtén un perfume por ID.
- **POST** `/perfumes`: Crea un nuevo perfume (solo admin).
- **PUT** `/perfumes/<id>`: Actualiza un perfume por ID (solo admin).
- **DELETE** `/perfumes/<id>`: Elimina un perfume por ID (solo admin).

### Compras
- **POST** `/compras`: Realiza una compra (requiere autenticación).
- **GET** `/compras`: Obtén todas las compras del usuario (requiere autenticación).