import base64
from datetime import datetime
import re
from backend.database import db

user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

playlist_song = db.Table('playlist_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

user_song_like = db.Table('user_song_like',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String, nullable=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    blacklist = db.Column(db.Boolean, default=False, nullable=False)
    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
        backref=db.backref('users', lazy=True))
    liked_songs = db.relationship('Song', secondary=user_song_like,
                                  backref=db.backref('likers', lazy='dynamic'))

    def __init__(self, fname, lname, email, phone, password):
        self.fname = fname
        self.lname = lname
        self.set_email(email)
        self.set_phone(phone)
        self.set_password(password)

    def __repr__(self):
        return f'<User {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'image': self.image,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'phone': self.phone,
            'image': self.image,
            'roles': [role.serialize() for role in self.roles]
        }
    
    def set_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email address")

        self.email = email

    def set_phone(self, phone):
        phone_pattern = r'^\d{10}$'
        if not re.match(phone_pattern, phone):
            raise ValueError("Invalid phone number")

        self.phone = phone

    def set_password(self, password):
        if len(password) < 5:
            raise ValueError("Password must be at least 5 characters long")
        # if len(password) > 16:
        #     raise ValueError("Password must be at most 16 characters long")
        # if not any(char.isupper() for char in password):
        #     raise ValueError("Password must contain at least one uppercase letter")
        # if not any(char.isdigit() for char in password):
        #     raise ValueError("Password must contain at least one number")
        # if not any(char in '!@#$%^&*()_-+={}[]|\:;"<>,.?/~`' for char in password):
        #     raise ValueError("Password must contain at least one special character")
        self.password = password

    def blacklist_user(self):
        self.blacklist = True
        db.session.commit()

    def unblacklist_user(self):
        self.blacklist = False
        db.session.commit()
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'role': self.name
        }

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    singer = db.Column(db.String(128))
    genre = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    songs = db.relationship('Song', backref='album', lazy=True)

    def __init__(self, name, singer, user_id, genre):
        self.name = name
        self.singer = singer
        self.user_id = user_id
        self.genre = genre
    def __repr__(self):
        return f'<id {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'singer': self.singer,
            'user_id': self.user_id,
            'genre': self.genre
        }

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    audio_file = db.Column(db.LargeBinary)  
    image = db.Column(db.LargeBinary)
    genre = db.Column(db.String(128))
    date = db.Column(db.String)
    lyrics = db.Column(db.String(10000), nullable=False)
    singer = db.Column(db.String(128), nullable=False)
    play_count = db.Column(db.Integer, default=0, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), default=None)
    ratings = db.relationship('SongRating', backref='song', lazy=True)
    comments = db.relationship('Comment', backref='song', lazy=True)

    def __repr__(self):
        return f"<Song id={self.id}, name='{self.name}', singer='{self.singer}', genre='{self.genre}'>"
    
    def __init__(self, name, user_id, audio_file, image, lyrics, singer, album_id, genre):
        self.name = name    
        self.user_id = user_id
        self.audio_file = audio_file
        self.image = image
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.lyrics = lyrics
        self.singer = singer  
        self.album_id = album_id
        self.genre = genre

        
    def increment_play_count(self):
        self.play_count += 1
        db.session.commit()

    def serialize(self, exclude_audio=False):
        data = {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'image': base64.b64encode(self.image).decode('utf-8') if self.image else None,
            'genre': self.genre,
            'date': self.date,
            'lyrics': self.lyrics,
            'singer': self.singer,
            'play_count': self.play_count,
            'album_id': self.album_id,
        }

        if not exclude_audio:
            data['audio_file'] = base64.b64encode(self.audio_file).decode('utf-8') if self.audio_file else None

        return data


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_song, backref='playlists', lazy='dynamic')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<Playlist id={self.id}, name='{self.name}'>"
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'songs': [song.serialize() for song in self.songs]  # Assuming Song has a serialize method
        }
    
class SongRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"<SongRating id={self.id}, user_id={self.user_id}, song_id={self.song_id}, rating={self.rating}>"

    def __init__(self, user_id, song_id, rating):
        self.user_id = user_id
        self.song_id = song_id
        self.rating = rating

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'song_id': self.song_id,
            'rating': self.rating
        }
    
class RecentlyPlayedSongs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<RecentlyPlayedSongs id={self.id}, song_id={self.song_id}, user_id={self.user_id}, timestamp={self.timestamp}>"

    def serialize(self):
        return {
            'id': self.id,
            'song_id': self.song_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
    def __init__(self, song_id, user_id):
        self.song_id = song_id
        self.user_id = user_id

class ReportedSong(db.Model):
    __tablename__ = 'reported_songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.String(1000))  # Adjust size as needed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    song = db.relationship('Song', backref='reports')
    user = db.relationship('User', backref='reported_songs')
    def serialize(self):
        return {
            'id': self.id,
            'song_id': self.song_id,
            'user_id': self.user_id,
            'reason': self.reason,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }

    def __init__(self, song_id, user_id, reason):
        self.song_id = song_id
        self.user_id = user_id
        self.reason = reason

    def __repr__(self):
        return f'<ReportedSong id={self.id}, song_id={self.song_id}, user_id={self.user_id}, reason="{self.reason}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'),nullable=False)
    comment = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f"<Comment id={self.id}, user_id={self.user_id}, song_id={self.song_id}, comment='{self.comment}'>"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'song_id': self.song_id,
            'comment': self.comment
        }
    def __init__(self, user_id, song_id, comment):
        self.user_id = user_id
        self.song_id = song_id
        self.comment = comment
