from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot left in blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot left in blank")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool) #Não coloco como required pois alguém malicioso pode tentar fazer login sem a confirmação

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404  # not found
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message:' 'An internal error ocurred trying to delete the user.'}, 500  # Internal server error
            return {'message': 'User deleted'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {'message': "The field 'email' cannot be left in blank"}, 400

        if UserModel.find_by_email(dados['email']):
            return {'message': f"The email '{dados['email']}' already exists."}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message:": f"The login '{dados['login']}' already exists."}
        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created succesfully'}, 201 #Created

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if user and compare_digest(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'acess_token': token_de_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect'}, 401 # Unauthorized

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200

class UserConfirm(Resource):
    #raiz_do_site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {'message': f"User id '{user_id}' not found."}, 404
        user.ativado = True
        user.save_user()
        #return {'message:': f"User id '{user_id}' confirmed successfully."}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login),200, headers)
