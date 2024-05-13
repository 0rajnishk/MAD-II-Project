from datetime import datetime
import io
import sqlite3
from backend.tasks import export_creators_csv, export_songs_csv, reminder_email, test_task
from flask import Config, jsonify, request
import jwt
from backend import app
from backend import api
from flask_restful import Resource, reqparse
from backend.auth import role_required
from backend.models import  Album, Comment, Playlist, RecentlyPlayedSongs, Song, SongRating, User, Role, ReportedSong, user_song_like
from backend.database import db
from backend.dto import Response, ErrorResponse
from backend import cache
import base64
import matplotlib.pyplot as plt


class CeleryTestResource(Resource):
    def get(self):
        tool = request.args.get('tool')
        if tool == "export":
            export_songs_csv.delay('surajnish02@gmail.com')
        elif tool == 'test':
            test_task.delay()
        return jsonify({"message": "Test task triggered successfully!"})



def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, 'rajnish@123', algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id is None:
                raise ValueError("User ID missing in token payload")
            return user_id
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
            print(f"Token error: {e}")
            return None
    else:
        return None
 

class ExportJobs(Resource):
    @role_required(allowed_roles=['admin', 'Creator'])
    def get(self):
        user_id = get_user_id_from_token()


        if user_id is not None:
            email = User.query.get(user_id).email
            roles = User.query.get(user_id).roles
            if 'admin' not in [role.name for role in roles]:
                export_creators_csv.delay(email, user_id)
                return {"msg": "Exporting creators", "status": True, "error": None}, 200
            
            export_songs_csv.delay(email)
            return {"msg": "Exporting songs", "status": True, "error": None}, 200
        else:
            return {"error": "Unauthorized", "status": False}, 401

class UserResource(Resource):
    @role_required(allowed_roles=['admin'])
    @cache.cached(timeout=60)
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
            cache.clear()
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
            cache.clear()
            return {"msg":Response('User deleted successfully').serialize(), "status":True, "error": None}
        except Exception as e:
            return {"error":ErrorResponse('Error deleting user', str(e)).serialize(), "status": False}, 400

class UsersResourceList(Resource):
    @cache.cached(timeout=60)
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
                    return {"msg":'User already exists please Login', "status": True, "error": 'User already exists please Login'}, 409
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
                cache.clear()
                return {"msg":Response('User created successfully', user.serialize()).serialize(), "status":True, "error": None}, 201
            
            except ValueError as e:
                return {"error":ErrorResponse('Error creating user', str(e)).serialize(), "status":False}, 400
        except Exception as e:
            return {"error": ErrorResponse('Error creating user', str(e)).serialize(), "status": False}, 400
     

class SongResource(Resource):
    @cache.cached(timeout=60)
    @role_required(allowed_roles=['user', 'admin', 'Creator'])
    def get(self):
        try:
            songs = Song.query.all()
            if not songs:
                return {"error": "No songs found", "status": False}, 404

            return {"songs": [song.serialize(exclude_audio=True) for song in songs], "status": True, "error": None}, 200

        except Exception as e:
            return {"error": str(e), "status": False}, 400
    @role_required(allowed_roles=['Creator', 'admin'])
    def post(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            try:
                args = self.parser.parse_args()
                args['image'] =  base64.b64decode(args['image'].split(',')[1])
                args['audio_file'] = base64.b64decode(args['audio_file'].split(',')[1])

                song = Song(**args, user_id=user_id, album_id=None)
                db.session.add(song)
                db.session.commit()
                cache.clear()
                return {"msg": "Song created successfully", "song_id": song.id, "status":True, "error": None}, 201
            except Exception as e:
                print("\n",e,"\n")
                return {"error": str(e), "status": False}, 400
            
    @role_required(allowed_roles=['Creator', 'admin'])
    def delete(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            try:
                song_id = request.args.get('song_id')
                song = Song.query.get(song_id)
                if not song:
                    return {"error": "Song not found", "status": False}, 404
                
                # Delete all ratings associated with the song
                ratings = SongRating.query.filter_by(song_id=song_id).all()
                for rating in ratings:
                    db.session.delete(rating)
                    # Delete all reported songs associated with the song
                reported_songs = ReportedSong.query.filter_by(song_id=song_id).all()
                for reported_song in reported_songs:
                    db.session.delete(reported_song)
                # Now delete the song itself
                db.session.delete(song)
                
                # Commit the changes
                db.session.commit()
                cache.clear()
                
            except sqlite3.OperationalError as e:
                cache.clear()
                return {"msg": "Song deleted successfully", "status": True, "error": None}, 200
            except Exception as e:
                # Rollback the session in case of any error
                db.session.rollback()
                return {"error": str(e), "status": False}, 400

class Song_Resource(Resource):
    def get(self, song_id):
        try:
            song = Song.query.get(song_id)
            if not song:
                return {"error": "Song not found", "status": False}, 404
            return {"msg":song.serialize(), "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400

    def put(self, song_id):
        try:
            song = Song.query.get(song_id)
            if not song:
                return {"error": "Song not found", "status": False}, 404
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='Name is required')
            parser.add_argument('singer', type=str)
            parser.add_argument('genre', type=str)
            parser.add_argument('audio_file', type=str)
            parser.add_argument('image', type=str)
            parser.add_argument('lyrics', type=str)
            parser.add_argument('album_id', type=int)
            args = parser.parse_args()
            song.name = args['name']
            song.singer = args['singer']
            song.genre = args['genre']
            song.album_id = args['album_id']
            if args["album_id"]:
                song.album_id = args["album_id"]
            if args['audio_file']:
                song.audio_file = base64.b64decode(args['audio_file'].split(',')[1])
            if args['image']:
                song.image = base64.b64decode(args['image'].split(',')[1])
            song.lyrics = args['lyrics']
            db.session.commit()
            cache.clear()
            cache.clear()
            return {"msg":song.serialize(), "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400

class AdminSongResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
        self.parser.add_argument('singer', type=str)
        self.parser.add_argument('genre', type=str)
        self.parser.add_argument('audio_file', type=str)
        self.parser.add_argument('image', type=str)
        self.parser.add_argument('lyrics', type=str)

    @role_required(allowed_roles=['user', 'admin', 'Creator'])
    def get(self):
        user_id = get_user_id_from_token()
        try:
            songs = Song.query.filter_by(user_id=user_id).all()
            # print the number of songs
            print(len(songs))
            if not songs:
                return {"error": "No songs found", "status": False}, 404

            return {"songs": [song.serialize(exclude_audio=True) for song in songs], "status": True, "error": None}, 200

        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['Creator', 'admin'])
    def post(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            try:
                args = self.parser.parse_args()
                args['image'] =  base64.b64decode(args['image'].split(',')[1])
                args['audio_file'] = base64.b64decode(args['audio_file'].split(',')[1])

                song = Song(**args, user_id=user_id, album_id=None)
                db.session.add(song)
                db.session.commit()
                cache.clear()
                return {"msg": "Song created successfully", "song_id": song.id, "status":True, "error": None}, 201
            except Exception as e:
                print("\n",e,"\n")
                return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['Creator', 'admin'])
    def put(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            try:
                song_id = request.args.get('song_id')
                args = self.parser.parse_args()
                song = Song.query.get(song_id)
                if not song:
                    return {"error": "Song not found", "status":False}, 404
                
                if song.user_id != user_id:
                    return {"error": "You are not authorized to update this song", "status":False}, 403
                

                args['image'] =  base64.b64decode(args['image'].split(',')[1])
                args['audio_file'] = base64.b64decode(args['audio_file'].split(',')[1])

                for key, value in args.items():
                    setattr(song, key, value)
                db.session.commit()
                cache.clear()
                return {"msg": "Song updated successfully", "status":True}, 200
            except Exception as e:
                return {"error": str(e), "status":True}, 400
        
    @role_required(allowed_roles=['Creator', 'admin'])
    def delete(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            try:
                song_id = request.args.get('song_id')
                print('***'*100, song_id)
                song = Song.query.get(song_id)
                if not song:
                    print("not song")
                    return {"error": "Song not found", "status": False}, 404
                if song.user_id != user_id:
                    print("song. user ! same")
                    return {"error": "You are not authorized to delete this song", "status": False}, 403
                print("everything ok just something")
                db.session.delete(song)
                db.session.commit()
                cache.clear()
                return {"msg": "Song deleted successfully", "status":True, "error": None}, 200
            except Exception as e:
                return {"error": str(e), "status":False}, 400

        
class PlaylistResource(Resource):
    @role_required(allowed_roles=['Creator', 'user'])
    def get(self):
        user_id = get_user_id_from_token()
        print(user_id, "get plalist", '**************************')
        playlists = Playlist.query.filter_by(user_id=user_id).all()  # Assuming a user can have multiple playlists

        if not playlists:
            return {"error": "No playlists found for the user", "status": False}, 404

        # Serializing multiple playlists
        playlists_data = [playlist.serialize() for playlist in playlists]
        return {"msg": playlists_data, "error": None, "status": True}, 200

    @role_required(allowed_roles=['user', 'Creator', 'admin'])
    def post(self):
        print("Playlist", '**************************')
        user_id = get_user_id_from_token()
        print(user_id, "Playlist", '**************************')
        if user_id is not None:
            # Initialize the request parser and add expected arguments
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='Name is required')
            parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
            args = parser.parse_args()

            # Retrieve the song based on song_id
            song = Song.query.get(args['song_id'])
            if song is None:
                return {"msg": "Song not found", "error": "Song with provided ID does not exist", "status": False}, 404

            # Create a new playlist
            playlist = Playlist(name=args['name'], user_id=user_id)
            
            # Add the playlist to the session
            db.session.add(playlist)
            # It's important to flush the session to ensure 'playlist' is assigned an ID
            db.session.flush()

            # Associate the song with the newly created playlist
            playlist.songs.append(song)

            # Commit changes to the database
            db.session.commit()
            cache.clear()

            return {"msg": "Playlist created and song added successfully", "error": None, "status": True}, 201

    @role_required(allowed_roles=['user', 'admin'])
    def patch(self):
        user_id = get_user_id_from_token()

        if user_id is not None:
            parser = reqparse.RequestParser()
            parser.add_argument('song_id', type=int, required=True, help='Song ID is required to add to the playlist')
            parser.add_argument('playlist_id', type=int, required=True, help='Playlist ID is required')
            args = parser.parse_args()

            # Retrieve the playlist
            playlist = Playlist.query.filter_by(id=args['playlist_id'], user_id=user_id).first()
            if not playlist:
                return {"msg": "Playlist not found or you do not have permission to edit it.", "error": "Not Found", "status": False}, 404

            song = Song.query.get(args['song_id'])
            if not song:
                return {"msg": "Song not found", "error": "Song with provided ID does not exist", "status": False}, 404


            if song in playlist.songs:
                return {"msg": "Song already in the playlist", "error": None, "status": False}, 400

            # Add the song to the playlist and commit the change
            playlist.songs.append(song)
            db.session.commit()
            cache.clear()

            return {"msg": "Song added to the playlist successfully", "error": None, "status": True}, 200

        else:
            return {"msg": "Unauthorized", "error": "Unauthorized", "status": False}, 401

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        user_id = get_user_id_from_token()
        if user_id is not None:
            playlist_id = request.args.get("playlist_id")
            playlist = Playlist.query.get(playlist_id)
            if not playlist:
                return {"error": "Playlist not found", "status": False}, 404
            if playlist.user_id != user_id:
                return {"error": "You are not authorized to delete this playlist", "status": False}, 403
            db.session.delete(playlist)
            db.session.commit()
            cache.clear()
            return {"error": "Playlist deleted successfully", "status": False}, 200

class SongRatingResource(Resource):
    @role_required(allowed_roles=['user', 'Creator', 'admin'])
    def get(self):
        song_id = request.args.get('song_id', type=int)
        if song_id is None:
            return {"error": "Song ID is required", "status": False}, 400
        
        user_id = get_user_id_from_token()
        rating = SongRating.query.filter_by(user_id=user_id, song_id=song_id).first()
        if not rating:
            return {"error": "Rating not found", "status": False}, 404
        return {"msg": rating.serialize(), "error": None, "status": True}, 200

    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        user_id = get_user_id_from_token()
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('rating', type=int, required=True, help='Rating is required')
        args = parser.parse_args()

        # Check if the user has already rated the song
        existing_rating = SongRating.query.filter_by(user_id=user_id, song_id=args['song_id']).first()

        if existing_rating:
            # If the user has already rated the song, update the existing record
            existing_rating.rating = args['rating']
            db.session.commit()
            cache.clear()
            return {"msg": "Rating updated successfully", "error": None, "status": True}, 200
        else:
            # If the user hasn't rated the song yet, create a new rating record
            song_rating = SongRating(user_id=user_id, song_id=args['song_id'], rating=args['rating'])
            db.session.add(song_rating)
            db.session.commit()
            cache.clear()
            return {"msg": song_rating.serialize(), "error": None, "status": True}, 201

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
        cache.clear()
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
        cache.clear()
        return {"msg":jsonify(comment.serialize()), "status":True, "error":None}, 204

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        comment_id =  request.args.get('id')
        comment = Comment.query.get(comment_id)
        if not comment:
            return {"error": "Comment not found", "status": False}, 404
        db.session.delete(comment)
        db.session.commit()
        cache.clear()
        return {"msg": "Comment deleted successfully", "error": None, "status": True}, 200

class RecentlyPlayedSongsResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def get(self):
        user_id = get_user_id_from_token()
        played_songs = RecentlyPlayedSongs.query.filter_by(user_id=user_id).order_by(RecentlyPlayedSongs.timestamp.desc()).all()
        if not played_songs:
            return ({"error": "Recently played songs not found", "status": False}), 404

        # Fetch song details for each played song
        song_details = []
        for played_song in played_songs:
            song = Song.query.get(played_song.song_id)
            if song:
                song_details.append({"song_id": song.id, "song_name": song.name})

        return ({"msg": song_details, "status": True, "error": None})

    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        user_id = get_user_id_from_token()
        if user_id is None:
            return ({"error": "Unauthorized", "status": False}), 401
        
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        args = parser.parse_args()

        played_song = RecentlyPlayedSongs.query.filter_by(song_id=args['song_id'], user_id=user_id).first()

        if played_song:
            played_song.timestamp = datetime.utcnow()
            db.session.commit()
            cache.clear()
            return ({"msg": "time stamp updated successfully", "status": True, "error": None}), 200
        else:
            # If the song doesn't exist, create a new entry
            new_played_song = RecentlyPlayedSongs(song_id=args['song_id'], user_id=user_id)
            db.session.add(new_played_song)
            db.session.commit()
            cache.clear()
            return ({"msg": "Success", "status": True, "error": None}), 201


class AlbumResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('singer', type=str)
        self.parser.add_argument('genre', type=str)

    @role_required(allowed_roles=['user','Creator', 'admin'])
    def get(self):
        try:
            albums = Album.query.all()
            if not albums:
                return {"message": "No albums found"}, 404
            print(album.serialize() for album in albums)
            return {"msg": [album.serialize() for album in albums], "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
        
    @role_required(allowed_roles=['user', 'Creator', 'admin'])
    def post(self):
        try:
            print("Inside post")
            user_id = get_user_id_from_token()
            print(user_id)
            args = self.parser.parse_args()
            print(args)
            album = Album(name=args['name'], singer=args['singer'], genre=args['genre'], user_id=user_id)
        
            db.session.add(album)
            db.session.commit()
            cache.clear()
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
            cache.clear()
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
            cache.clear()
            return {"msg": "Album deleted successfully", "status": True}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400

class Album_Resource(Resource):
    def get(self, album_id):
        try:
            album = Album.query.get(album_id)

            return {"msg": album.serialize(), "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
  
class Albums_Resource(Resource):
    def get(self, album_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                return {"error": "Album not found", "status": False}, 404
            songs = album.songs
            serialized_songs = [song.serialize(exclude_audio=True) for song in songs]
            return {"msg": serialized_songs, "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400

class AdminAlbumResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('singer', type=str)
        self.parser.add_argument('genre', type=str)

    @role_required(allowed_roles=['user','Creator', 'admin'])
    def get(self):
        user_id = get_user_id_from_token()
        try:
            albums = Album.query.filter_by(user_id=user_id).all()
            if not albums:
                return {"message": "No albums found"}, 404
            return {"msg": [album.serialize() for album in albums], "status":True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400
    @role_required(allowed_roles=['user', 'Creator', 'admin'])
    def post(self):
        try:
            print("Inside post")
            user_id = get_user_id_from_token()
            print(user_id)
            args = self.parser.parse_args()
            print(args)
            album = Album(name=args['name'], singer=args['singer'], genre=args['genre'], user_id=user_id)
        
            db.session.add(album)
            db.session.commit()
            cache.clear()
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
            cache.clear()
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
            cache.clear()
            return {"msg": "Album deleted successfully", "status": True}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 400

class ReportSongResource(Resource):
    @role_required(allowed_roles=['user'])
    def post(self):
        user_id = get_user_id_from_token()
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        parser.add_argument('reason', type=str, required=True, help='Reason for reporting is required')
        
        args = parser.parse_args()

        song_id = args['song_id']
        reason = args['reason']

        # Optional: Verify the song exists
        song = Song.query.get(song_id)
        if not song:
            return {"error": "Song not found", "status": False}, 404
        
        # Create and save the new report
        report = ReportedSong(song_id=song_id, user_id=user_id, reason=reason)
        db.session.add(report)
        db.session.commit()
        cache.clear()

        return {"message": "Report submitted successfully", "status": True, "error": None}, 201

class LikeSongResource(Resource):
    @role_required(allowed_roles=['user', 'admin'])
    def post(self):
        user_id = get_user_id_from_token()
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        
        args = parser.parse_args()
        song_id = args['song_id']

        print(f"User {user_id} is liking song {song_id}")
        # Verify the song exists
        song = Song.query.get(song_id)
        if not song:
            return {"error": "Song not found", "status": False}, 404

        # Check if the user already liked the song
        existing_like = db.session.query(user_song_like).filter_by(user_id=user_id, song_id=song_id).first()
        if existing_like:
            return {"message": "Song already liked", "status": False}, 400

        # Add a new like
        new_like = user_song_like.insert().values(user_id=user_id, song_id=song_id)
        db.session.execute(new_like)
        db.session.commit()
        cache.clear()

        return {"message": "Song liked successfully", "status": True}, 201

    @role_required(allowed_roles=['user', 'admin'])
    def delete(self):
        user_id = get_user_id_from_token()
        parser = reqparse.RequestParser()
        parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
        
        args = parser.parse_args()
        song_id = args['song_id']


        song = Song.query.get(song_id)
        if not song:
            return {"error": "Song not found", "status": False}, 404

        existing_like = db.session.query(user_song_like).filter_by(user_id=user_id, song_id=song_id).first()
        if not existing_like:
            return {"message": "Song not liked previously", "status": False}, 400

        db.session.execute(user_song_like.delete().where((user_song_like.c.user_id == user_id) & (user_song_like.c.song_id == song_id)))
        db.session.commit()
        cache.clear()

        return {"message": "Song unliked successfully", "status": True}, 201 


class UserPlaylistRes(Resource):
    def get(self):
        try:
            id = request.args.get('id')
            playlist = Playlist.query.get(id)
            if not playlist:
                return {"error": "Playlist not found", "status": False}, 404
            
            songs = playlist.songs
            return {"msg": [song.serialize(exclude_audio=True) for song in songs], "status": True, "error": None}, 200
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            return {"error": str(e), "status": False}, 500


class SearchSongsResource(Resource):
    def get(self):
        try:
            query = request.args.get('query')
            rating = request.args.get('rating')

            print(rating, query, '*******************')
            if not query:
                return {"error": "At least one search parameter is required", "status": False}, 400

            songs_query = Song.query.filter(
                (Song.name.ilike(f'%{query}%')) |
                (Song.singer.ilike(f'%{query}%')) |
                (Song.genre.ilike(f'%{query}%'))
            )
            if rating and rating != '0':
                songs_query = songs_query.filter(Song.ratings.any(rating=int(rating)))

            songs = songs_query.all()

            if not songs:
                return {"error": "No songs found", "status": False}, 404

            serialized_songs = [song.serialize(exclude_audio=True) for song in songs]

            return {"msg": serialized_songs, "status": True, "error": None}, 200

        except Exception as e:
            return {"error": str(e), "status": False}, 500

class SearchAlbumsResource(Resource):
    def get(self):
        try:
            query = request.args.get('query')

            if not query:
                return {"error": "At least one search parameter is required", "status": False}, 400

            albums_query = Album.query.filter(
                (Album.name.ilike(f'%{query}%')) |
                (Album.singer.ilike(f'%{query}%')) |
                (Album.genre.ilike(f'%{query}%'))
            )

            albums = albums_query.all()

            if not albums:
                return {"error": "No albums found", "status": False}, 404


            serialized_albums = [album.serialize() for album in albums]


            return {"msg": serialized_albums, "status": True, "error": None}, 200

        except Exception as e:
            return {"error": str(e), "status": False}, 500

class UserRole(Resource):
    @role_required(allowed_roles=['user']) 
    def get(self):
        user_id = get_user_id_from_token()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found", "status": False}, 404
        
        # Check if the 'Creator' role already exists
        creator_role = Role.query.filter_by(name='Creator').first()
        if not creator_role:
            creator_role = Role('Creator')
            db.session.add(creator_role)
            db.session.commit()
            cache.clear()
        
        # Add 'Creator' role to the user if not already assigned
        if creator_role not in user.roles:
            user.roles.append(creator_role)
            db.session.commit()
            cache.clear()
            return {"msg": "Creator role added successfully", "status": True}, 200

        return {"msg": "Already a creator", "status": True}, 200


class StatsResource(Resource):
    def get(self):
        try:
            # Query total counts for each entity
            total_songs = Song.query.count()
            print(total_songs, '*******************')
            total_albums = Album.query.count()
            print(total_albums, '*******************')
            total_users = User.query.count()
            print(total_users, '*******************')
            total_creators = User.query.filter(User.roles.any(name='Creator')).count()

            print("total creators",total_creators, '*******************')

            # Construct the response
            stats = {
                "total_songs": total_songs,
                "total_albums": total_albums,
                "total_users": total_users,
                "total_creators": total_creators
            }

            return {"stats": stats, "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500




class TopSongResource(Resource):
    def get(self):
        try:
            # Retrieve all songs
            songs = Song.query.all()


            song_data = {}


            for song in songs:
                # Retrieve ratings for the current song
                ratings = SongRating.query.filter_by(song_id=song.id).all()
                
                # Calculate average rating
                if ratings:
                    total_rating = sum(rating.rating for rating in ratings)
                    average_rating = total_rating / len(ratings)
                else:
                    average_rating = 0
                
                # Calculate rating distribution
                rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} 
                for rating in ratings:
                    rating_distribution[rating.rating] += 1
                

                song_data[song.name] = {"average_rating": average_rating, "rating_distribution": rating_distribution}
            

            top_songs = sorted(song_data.items(), key=lambda x: x[1]["average_rating"], reverse=True)[:5]

            encoded_images = {}
            for song_name, data in top_songs:
                rating_distribution = data["rating_distribution"]
                
                plt.bar(rating_distribution.keys(), rating_distribution.values())
                plt.xlabel('Rating')
                plt.ylabel('Number of Ratings')
                plt.title(f'Rating Distribution for {song_name}\nAverage Rating: {data["average_rating"]}')
                
                # Encode the chart to a base64 string
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
                encoded_images[song_name] = encoded_image
                
                plt.close()

            return {"encoded_images": encoded_images, "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500
# ========================================================================================
# ===============================rajnish=================================================|
# ========================================================================================
class SongPerformanceResource(Resource):
    @role_required(allowed_roles=['admin'])
    def get(self):
        try:
            # Retrieve all songs
            songs = Song.query.all()

            total_ratings = {}
            average_ratings = {}


            for song in songs:
                # Retrieve ratings for the current song
                ratings = SongRating.query.filter_by(song_id=song.id).all()


                total_ratings[song.name] = len(ratings)
                if total_ratings[song.name] > 0:
                    total_score = sum(rating.rating for rating in ratings)
                    average_ratings[song.name] = total_score / total_ratings[song.name]
                else:
                    average_ratings[song.name] = 0  



            return {
                "total_ratings": total_ratings,
                "average_ratings": average_ratings,
                "status": True,
                "error": None
            }, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500




        
class ReportedSongsResource(Resource):
    @role_required(allowed_roles=['admin'])
    def get(self):
        try:
            # Query all reported songs
            reported_songs = ReportedSong.query.all()
            

            serialized_reported_songs = [reported_song.serialize() for reported_song in reported_songs]

            return {"reported_songs": serialized_reported_songs, "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500
        


class SearchUsersResource(Resource):
    @role_required(allowed_roles=['admin'])
    def get(self):
        try:
            query = request.args.get('query')
            # You can add more parameters as needed
            
            if not query:
                return {"error": "Search query parameter is required", "status": False}, 400
            
            users_query = User.query.filter((User.fname.ilike(f'%{query}%')) | (User.lname.ilike(f'%{query}%')))
            
            users = users_query.all()
            if not users:
                return {"error": "No users found", "status": False}, 404
            
            return {"users": [user.serialize() for user in users], "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500

class SearchCreatorsResource(Resource):
    @role_required(allowed_roles=['admin'])
    def get(self):
        try:
            query = request.args.get('query')

            
            if not query:
                return {"error": "Search query parameter is required", "status": False}, 400
            
            creators_query = User.query.filter(User.roles.any(Role.name == 'Creator')).filter((User.fname.ilike(f'%{query}%')) | (User.lname.ilike(f'%{query}%')))
            
            creators = creators_query.all()
            if not creators:
                return {"error": "No creators found", "status": False}, 404
            
            return {"creators": [creator.serialize() for creator in creators], "status": True, "error": None}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500

class BlacklistUsersResource(Resource):
    @role_required(allowed_roles=['admin'])
    def get(self):
        try:
            # Fetch all blacklisted users
            blacklisted_users = User.query.filter_by(blacklist=True).all()
            return {"blacklisted_users": [user.serialize() for user in blacklisted_users], "status": True}, 200
        except Exception as e:
            return {"error": str(e), "status": False}, 500
    @role_required(allowed_roles=['admin'])
    def post(self):
        try:
            # Blacklist a user
            user_id = request.args.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.blacklist = True
                db.session.commit()
                cache.clear()
                return {"message": f"User with ID {user_id} has been blacklisted", "status": True}, 200
            else:
                return {"error": f"User with ID {user_id} not found", "status": False}, 404
        except Exception as e:
            return {"error": str(e), "status": False}, 500

    @role_required(allowed_roles=['admin'])
    def put(self):
        try:
            user_id = request.args.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.blacklist = False
                db.session.commit()
                cache.clear()
                return {"message": f"User with ID {user_id} has been whitelisted", "status": True}, 200
            else:
                return {"error": f"User with ID {user_id} not found", "status": False}, 404
        except Exception as e:
            return {"error": str(e), "status": False}, 500
class WhitelistUserResource(Resource):
    @role_required(allowed_roles=['admin'])
    def post(self):
        try:
            # Whitelist a user
            user_id = request.args.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.blacklist = False
                db.session.commit()
                cache.clear()
                return {"message": f"User with ID {user_id} has been whitelisted", "status": True}, 200
            else:
                return {"error": f"User with ID {user_id} not found", "status": False}, 404
        except Exception as e:
            return {"error": str(e), "status": False}, 500