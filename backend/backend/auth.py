from functools import wraps
from flask_restful import Resource, reqparse
from flask import request
from backend.models import User
from backend.config import Config
import  jwt
import datetime

def create_jwt_token(user):
    try:
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),  # Expires in 1 day
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }
        secret_key = 'rajnish@123' 
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
                    user_id = payload.get('user_id')
                    if user_id is None:
                        raise ValueError("User ID missing in token payload")
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
                    print(f"Token error: {e}")
                    return {'message': f"Token error: {e}"}, 401
                
                # Fetch the user from the database
                current_user = User.query.get(user_id)
                if not current_user:
                    return {'message': 'User not found'}, 404

                # Check if the user has any of the allowed roles
                user_roles = [role.name for role in current_user.roles] 
                if not any(role in allowed_roles for role in user_roles):
                    print(f"User {current_user.id} does not have any of the required roles: {allowed_roles}")
                    return {'message': 'Insufficient permissions'}, 403
                return fn(*args, **kwargs)
            else:
                print("Token is missing")
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
                role_names = [role.name for role in user.roles]
                print("Got access token", access_token)
                return {'access_token': access_token, 'role_names':role_names, 'user': user.serialize(), "status":True, "error": None}, 200
            else:
                return {"error": "Invalid credentials", "status":False}, 401
        except Exception as e:
            return {"error": str(e), "status":False}, 400