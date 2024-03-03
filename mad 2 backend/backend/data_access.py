from models import db, User
import datetime as dt

def get_all_users():
    users = User.query.all()
    return [user.serialize() for user in users]


