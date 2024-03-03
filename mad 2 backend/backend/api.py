from datetime import datetime
from flask import jsonify, request
from backend import app
from backend import api
from flask_restful import Resource, reqparse
from backend.auth import role_required
from backend.models import  Album, Comment, Playlist, RecentlyPlayedSongs, Song, SongRating, User, Role
from backend.database import db
from backend.dto import Response, ErrorResponse
# from backend import cache

class UserResource(Resource):
    @role_required(allowed_roles=['admin'])
    # @cache.cached(timeout=60)
    def get(self, id):
        try:
            user = User.query.get(id)
            if not user:
                return {"error":Response('User not found').serialize(), "status":False}, 404
            return {"msg":user.serialize(), "status":True, "error": None }
        except Exception as e:
            return {"error":ErrorResponse('Error getting user', str(e)).serialize(), "status":False}, 400
    
    @role_required(allowed_roles=['user', 'admin'])
    def put(self, id):
        parser = reqparse.RequestParser()
        try: 
            parser.add_argument('fname', type=str)
            parser.add_argument('lname', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('phone', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('role', type=str)

            args = parser.parse_args()

            user = User.query.get(id)
            
            try:
                if not user:
                    return {'error' : 'User not found would you like to register?', "status": False}, 404
                if args['fname']:
                    user.fname = args['fname']
                if args['lname']:
                    user.lname = args['lname']
                if args['email']:
                    user.email = args['email']
                if args['phone']:
                    user.phone = args['phone']
                if args['password']:
                    user.password = args['password']
                if args['role']:
                    roles = []
                    if args['role']=='manager':
                        role1 = Role.query.filter_by(name='user').first()
                        role2 = Role.query.filter_by(name='manager').first()
                        roles.append(role1)
                        roles.append(role2)
                    elif args['role']=='user':
                        role = Role.query.filter_by(name='user').first()
                        roles.append(role)
                    user.roles = roles
                
            except ValueError as e:
                return {"error":ErrorResponse('Error updating user', str(e)).serialize(), "status": False}, 400

            db.session.commit()
            # cache.clear()
            return {"msg":user.serialize(), "status": True, "error": None}
        except Exception as e:
            return {"error": ErrorResponse('Error updating user', str(e)).serialize(), "status":False}, 400
    
    @role_required(allowed_roles=['admin'])
    def delete(self, id):
        try:
            user = User.query.get(id)
            if 'admin' in [role.name for role in user.roles]:
                return {"error":Response('Admin cannot be deleted').serialize(), "status":False}, 400
            if not user:
                return { "error": Response('User already deleted!').serialize(), "status":False}, 404
            db.session.delete(user)
            db.session.commit()
            # cache.clear()
            return {"msg":Response('User deleted successfully').serialize(), "status":True, "error": None}
        except Exception as e:
            return {"error":ErrorResponse('Error deleting user', str(e)).serialize(), "status": False}, 400

class UsersResourceList(Resource):
    # @role_required(allowed_roles=['admin'])
    # @cache.cached(timeout=60)
    def get(self):
        try:
            users = User.query.all()
            if not users:
                return {"error": Response('No users found').serialize(), "status":False}
            return{"msg": [user.serialize() for user in users], "status":True, "error": None}
        except Exception as e:
            return {"error":ErrorResponse('Error getting users', str(e)).serialize(), "status":False}, 400

    def post(self):
        parser = reqparse.RequestParser()
        try:
            parser.add_argument('fname', type=str, required=True, help='First name is required')
            parser.add_argument('lname', type=str, required=True, help='Last name is required')
            parser.add_argument('email', type=str, required=True, help='Email is required')
            parser.add_argument('phone', type=str, required=True, help='Phone number is required')
            parser.add_argument('password', type=str, required=True, help='Password is required')
            args = parser.parse_args()
            try :
                user = User.query.filter_by(email=args['email']).first()
                if user:
                    return {"msg":Response('User already exists please Login').serialize(), "status": True, "error": None}, 400
                user = User.query.filter_by(phone=args['phone']).first()
                if user:
                    return {"error":Response('Phone no. already registered with different account').serialize(), "status": False}, 400
                user = User(
                    args['fname'], 
                    args['lname'], 
                    args['email'], 
                    args['phone'], 
                    args['password']
                    )
                role = Role.query.filter_by(name='user').first()

                if not role:
                    role = Role('user')
                    db.session.add(role)

                user.roles.append(role)
                db.session.add(user)
                db.session.commit()
                # cache.clear()
                return {"msg":Response('User created successfully', user.serialize()).serialize(), "status":True, "error": None}, 201
            
            except ValueError as e:
                return {"error":ErrorResponse('Error creating user', str(e)).serialize(), "status":False}, 400
        except Exception as e:
            return {"error": ErrorResponse('Error creating user', str(e)).serialize(), "status": False}, 400
        
class AlbumResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('singer', type=str)
        self.parser.add_argument('genre', type=str)
        self.parser.add_argument('user_id', type=int, required=True, help='User ID is required')

    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        try:
            albums = Album.query.all()
            if not albums:
                return {"message": "No albums found"}, 404
            return {"msg": [album.serialize() for album in albums], "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        try:
            args = self.parser.parse_args()
            album = Album(name=args['name'], singer=args['singer'], genre=args['genre'], user_id=args['user_id'])
            db.session.add(album)
            db.session.commit()
            return {"msg": "Album created successfully", "album_id": album.id, "status":True, "error": None}, 201
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['user', 'admin'])
    def put(self):
        try:
            args = self.parser.parse_args()
            album_id = request.args.get('album_id')
            album = Album.query.get(album_id)
            if not album:
                return {"error": "Album not found", "status": False}, 404
            album.name = args['name']
            album.singer = args['singer']
            album.genre = args['genre']
            db.session.commit()
            return {"message": "Album updated successfully", "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        try:
            album_id = request.args.get('album_id')
            album = Album.query.get(album_id)
            if not album:
                return {"error": "Album not found", "status": False}, 404
            db.session.delete(album)
            db.session.commit()
            return {"msg": "Album deleted successfully", "status": True}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
class SongResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('singer', type=str, required=True, help='Singer is required')
        self.parser.add_argument('genre', type=str)
        self.parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        self.parser.add_argument('audio_file', type=str)
        self.parser.add_argument('image', type=str)
        self.parser.add_argument('date', type=str)
        self.parser.add_argument('lyrics', type=str)
        self.parser.add_argument('album_id', type=int)

    @role_required(allowed_roles=['user', 'admin', 'creator'])
    def get(self):
        try:
            songs = Song.query.all()
            if not songs:
                return {"error": "No songs found", "status": False}, 404
            return {"songs": [song.serialize() for song in songs], "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['creator', 'admin'])
    def post(self):
        try:
            args = self.parser.parse_args()
            song = Song(**args)
            db.session.add(song)
            db.session.commit()
            return {"msg": "Song created successfully", "song_id": song.id, "status":True, "error": None}, 201
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['creator', 'admin'])
    def put(self):
        try:
            song_id = request.args.get('song_id')
            args = self.parser.parse_args()
            song = Song.query.get(song_id)
            if not song:
                return {"error": "Song not found", "status":False}, 404
            for key, value in args.items():
                setattr(song, key, value)
            db.session.commit()
            return {"msg": "Song updated successfully", "status":True}, 200
        except Exception as e:
            return {"error": str(e), "status":True}, 400
        
    @role_required(allowed_roles=['creator', 'admin'])
    def delete(self):
        try:
            song_id = request.args.get('song_id')
            song = Song.query.get(song_id)
            if not song:
                return {"error": "Song not found", "status": False}, 404
            db.session.delete(song)
            db.session.commit()
            return {"msg": "Song deleted successfully", "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status":False}, 400
        
class PlaylistResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        playlist_id =  request.args.get('id')
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {"error": "Playlist not found", "status":False}, 404
        return jsonify(playlist.serialize())

    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        args = parser.parse_args()

        playlist = Playlist(name=args['name'], user_id=args['user_id'])
        db.session.add(playlist)
        db.session.commit()
        return jsonify(playlist.serialize()), 201

    @role_required(allowed_roles=['user', 'admin'])
    def put(self):
        playlist_id = request.args.get("playlist_id")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()

        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {"message": "Playlist not found"}, 404

        playlist.name = args['name']
        db.session.commit()
        return {"msg":jsonify(playlist.serialize()), "error":None, "status":True}

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        playlist_id = request.args.get("playlist_id")
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {"error": "Playlist not found", "status": False}, 404
        db.session.delete(playlist)
        db.session.commit()
        return {"error": "Playlist deleted successfully", "status": False}, 200
    
class SongRatingResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        rating_id =  request.args.get('id')
        song_rating = SongRating.query.get(rating_id)
        if not song_rating:
            return {"error": "Song rating not found", "status": False}, 404
        return {"msg":jsonify(song_rating.serialize()), "status":True, "error": None}
    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('rating', type=int, required=True, help='Rating is required')
        args = parser.parse_args()

        song_rating = SongRating(user_id=args['user_id'], song_id=args['song_id'], rating=args['rating'])
        db.session.add(song_rating)
        db.session.commit()
        return {"msg":jsonify(song_rating.serialize()), "error":None, "status": True}, 201
    @role_required(allowed_roles=['user', 'admin'])
    def put(self):
        rating_id =  request.args.get('id')
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, required=True, help='Rating is required')
        args = parser.parse_args()

        song_rating = SongRating.query.get(rating_id)
        if not song_rating:
            return {"error": "Song rating not found", "status": False}, 404

        song_rating.rating = args['rating']
        db.session.commit()
        return {"msg":jsonify(song_rating.serialize()), "status": True, "error": False}
    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        rating_id =  request.args.get('id')
        song_rating = SongRating.query.get(rating_id)
        if not song_rating:
            return {"error": "Song rating not found", "status": False }, 404
        db.session.delete(song_rating)
        db.session.commit()
        return {"error": "Song rating deleted successfully", "status": False}, 200
    
class CommentResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        comment_id =  request.args.get('id')
        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found", "status": False}, 404
        return {"msg":jsonify(comment.serialize()), "status": True, "error": None}
    
    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('comment', type=str, required=True, help='Comment is required')
        args = parser.parse_args()

        comment = Comment(user_id=args['user_id'], song_id=args['song_id'], comment=args['comment'])
        db.session.add(comment)
        db.session.commit()
        return {"msg":jsonify(comment.serialize()), "error":None, "status": True}, 201

    @role_required(allowed_roles=['user', 'admin'])
    def put(self):
        comment_id =  request.args.get('id')
        parser = reqparse.RequestParser()
        parser.add_argument('comment', type=str, required=True, help='Comment is required')
        args = parser.parse_args()

        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found", "status": False}, 404

        comment.comment = args['comment']
        db.session.commit()
        return {"msg":jsonify(comment.serialize()), "status":True, "error":None}, 204

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        comment_id =  request.args.get('id')
        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found", "status": False}, 404
        db.session.delete(comment)
        db.session.commit()
        return {"msg": "Comment deleted successfully", "error": None, "status": True}, 200
    
class RecentlyPlayedSongsResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        played_song_id = request.args.get('id')
        played_song = RecentlyPlayedSongs.query.get(played_song_id)
        if not played_song:
            return {"error": "Recently played song not found", "status":False}, 404
        return {"msg":jsonify(played_song.serialize()), "status": True, "error": None}

    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        args = parser.parse_args()

        played_song = RecentlyPlayedSongs(song_id=args['song_id'], user_id=args['user_id'])
        db.session.add(played_song)
        db.session.commit()
        return {"msg":jsonify(played_song.serialize()), "status": True, "error":None}, 201
    
    @role_required(allowed_roles=['user', 'admin'])
    def put(self):
        played_song_id = request.args.get('id')
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        args = parser.parse_args()

        played_song = RecentlyPlayedSongs.query.get(played_song_id)
        if not played_song:
            return {"error": "Recently played song not found", "status": False}, 404

        played_song.song_id = args['song_id']
        played_song.user_id = args['user_id']
        db.session.commit()
        return {"msg":jsonify(played_song.serialize()), "error": None, "status": True }

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        played_song_id = request.args.get('id')
        played_song = RecentlyPlayedSongs.query.get(played_song_id)
        if not played_song:
            return {"error": "Recently played song not found", "status": False}, 404
        db.session.delete(played_song)
        db.session.commit()
        return {"msg": "Recently played song deleted successfully", "status": True}, 200