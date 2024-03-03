from functools import wraps
from flask_restful import Resource, reqparse
from flask import request
from backend.models import User
from backend.config import Config
import jwt
import datetime

def create_jwt_token(user):
    try:
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Expires in 1 day
            'iat': datetime.datetime.utcnow()
        }
        secret_key = 'YOUR_SECRET_KEY'  # You should use a secret key from your configuration or environment variables
        return jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        print(f"Error creating JWT token: {str(e)}")
        return None
       
def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(' ')[1]

                try:
                    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    return {'message': 'Token has expired'}, 401
                except jwt.InvalidTokenError:
                    return {'message': 'Invalid token'}, 401

                current_user = payload['sub']
                user_roles = [r['role'] for r in current_user['roles']]
                if any(role in allowed_roles for role in user_roles):
                    return fn(*args, **kwargs)
                else:
                    return {'message': 'Insufficient permissions'}, 403
            else:
                return {'message': 'Token is missing'}, 401
        return wrapper
    return decorator

class AuthResource(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', required=True, type=str, help='Email cannot be blank.')
            parser.add_argument('password', required=True, type=str, help='Password cannot be blank.')
            args = parser.parse_args()

            username = args['email']
            password = args['password']

            user = User.query.filter_by(email=username).first()
            user_password = user.password if user else None
            if user and (password == user_password):
                print("Inside")
                access_token = create_jwt_token(user)
                print("Got access token", access_token)
                return {'access_token': access_token, 'user': user.serialize(), "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status":False}, 400