import os
# import redis
from flask import Flask
from backend.config import Config
from backend.database import db
from backend.models import User, Role
# from flask_caching import Cache
# from celery import Celery
from flask_restful import Api
# import backend.workers as workers

app = None
api = None
jwt = None
celery = None
cache = None

def create_admin():
    role = Role.query.filter_by(name='admin').first()
    if not role:
        adminRole = Role('admin')
        userRole = Role('user')
        managerRole = Role('manager')
        db.session.add(adminRole)
        db.session.add(userRole)
        db.session.add(managerRole)
        admin = User(
            'Rajnish', 
            'Kumar',
            'rajnish@gmail.com',
            '1234567890',
            'Admin@123'
        )
        admin.roles.append(adminRole)
        admin.roles.append(userRole)
        admin.roles.append(managerRole)
        db.session.add(admin)
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.secret_key='ticketshow'
    if os.getenv('ENV', 'development') == 'production':
        raise Exception('Production environment not configured yet')
    else:
        print('Starting in development mode')
        app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
        create_admin()
    api = Api(app)

    # # create celery 
    # celery = workers.celery
    # celery.conf.update(
    #     broker_url=app.config["CELERY_BROKER_URL"],
    #     result_backend=app.config["CELERY_RESULT_BACKEND"],
    # )
    # celery.Task = workers.ContextTask
    # app.app_context().push()


    # redis_connection = redis.StrictRedis(
    #     host=app.config['REDIS_HOST'],
    #     port=app.config['REDIS_PORT'],
    #     db=app.config['REDIS_DB']
    # )
    # app.redis = redis_connection
    # app.app_context().push()

    
    # cache = Cache()

    # cache.init_app(app)
    app.app_context().push()

    # return app, api, celery, cache
    return app, api

app, api = create_app()

from backend.resources import *
from backend.routes import *
