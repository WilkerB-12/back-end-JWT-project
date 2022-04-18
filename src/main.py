"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask_jwt_extended import JWTManager,create_access_token
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route("/signin", methods=['POST'])
def createUser():
    new_email=request.json.get("email",None)
    registered_email=User.query.filter_by(email=new_email).first()
    if registered_email is not None:
        return jsonify({"msg":"El email ya está en uso"}),400
    else:
        body=request.json
        user=User.create(
            email=body['email'],
            password=body['password']
        )
        dictionary= user.serialize()
        print(dictionary)
        return jsonify(dictionary),201

@app.route("/token",methods=['POST'])
def create_token():
    email=request.json.get("email",None)
    password=request.json.get("password",None)
    user=User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg":"Error en el email o en la contraseña"}),401
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id, "email":user.email})

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/private', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "esta página es privada"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5432))
    app.run(host='0.0.0.0', port=PORT, debug=False)
