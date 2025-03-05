from flask import Flask
from flask_jwt_extended import JWTManager
from routes.perfumes_routes import configure_routes

app = Flask(__name__)
#configuracion de jwt
app.config["JWT_SECRET_KEY"] = "1024"
jwt = JWTManager(app)
#configuracion de rutas
configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

