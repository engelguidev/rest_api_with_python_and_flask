from sql_alchemy import banco
from flask import request, url_for
import requests



MAILGUN_DOMAIN = "sandboxbc339db79c18472c9ad8600e1f94454b.mailgun.org"
MAILGUN_API_KEY = "cd72061d130b80aa5951c07a4c8dc21f-8c8e5529-474f86bf"
FROM_TITLE = "NO-REPLY"
FROM_EMAIL = "no-reply@apigui.com"

class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", f"{MAILGUN_API_KEY}"),
            data={"from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                  "to": self.email,
                  "subject": "Confirmação de cadastro",
                  "text": f"Por favor, confirme o link para cadastro: {link}"})

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() #SELECT * FROM hoteis WHERE hotel_id = $hotel_id
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()  # SELECT * FROM hoteis WHERE hotel_id = $hotel_id
        if user:
            return user
        return None
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first() #SELECT * FROM hoteis WHERE hotel_id = $hotel_id
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()