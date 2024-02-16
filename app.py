import os
from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.site import Site, Sites


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'banco.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

cria_banco = False
@app.before_request
def verifica_cria_banco():
    global cria_banco
    if not cria_banco:
        banco.create_all()
        cria_banco = True

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token["jti"] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify(msg=f"You have been logged out!"), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
