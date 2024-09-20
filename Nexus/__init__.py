from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


    jwt = JWTManager(app)

    from .routes import routes



    with app.app_context():
        from Nexus import routes, auth, db
        db.init_db(app)
        app.register_blueprint(auth.auth)
        app.register_blueprint(routes.routes)

    return app

app = create_app()