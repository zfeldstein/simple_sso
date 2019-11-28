from app import db, app, ma
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    passwd = db.Column(db.String(64))
    ssh_key = db.Column(db.VARCHAR(2000))
    expiration = db.Column(db.Integer)
    email_addr = db.Column(db.VARCHAR(100))
    is_admin = db.Column(db.Boolean, unique=False, default=False)


    def hash_password(self, password):
        self.passwd = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.passwd)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = Users.query.get(data['id'])
        return user

class UsersSchema(ma.ModelSchema):
    class Meta:
        model = Users
        # sqla_sesion = db.session
