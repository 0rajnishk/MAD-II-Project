# data_access.py
from backend.database import db
from backend.models import User, Song, Album, Playlist, SongRating, RecentlyPlayedSongs, ReportedSong
import datetime as dt

# Fetch all users
def get_all_users():
    users = User.query.all()
    return [user.serialize() for user in users]

# Fetch all songs
def get_all_songs():
    songs = Song.query.all()
    return [song.serialize(exclude_audio=True) for song in songs]  # Exclude audio for performance

def get_creator_songs(user_id):
    # get all songs of a creator
    songs = Song.query.filter_by(user_id=user_id).all()
    return [song.serialize(exclude_audio=True) for song in songs]  # Exclude audio for performance

# Fetch all albums
def get_all_albums():
    albums = Album.query.all()
    return [album.serialize() for album in albums]

# Fetch all playlists for a user
def get_playlists_by_user(user_id):
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    return [playlist.serialize() for playlist in playlists]

# Fetch user by email
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.serialize()
    return None

# Like a song
def like_song(user_id, song_id):
    song = Song.query.get(song_id)
    user = User.query.get(user_id)
    if song and user:
        user.liked_songs.append(song)
        db.session.commit()

# Unlike a song
def unlike_song(user_id, song_id):
    song = Song.query.get(song_id)
    user = User.query.get(user_id)
    if song and user:
        user.liked_songs.remove(song)
        db.session.commit()

# Get recently played songs for a user
def get_recently_played_songs(user_id):
    recent_songs = RecentlyPlayedSongs.query.filter_by(user_id=user_id).order_by(RecentlyPlayedSongs.timestamp.desc()).limit(10)
    return [song.serialize() for song in recent_songs]

# Add a song to recently played
def add_to_recently_played(user_id, song_id):
    recent_song = RecentlyPlayedSongs(song_id=song_id, user_id=user_id)
    db.session.add(recent_song)
    db.session.commit()

# Report a song
def report_song(user_id, song_id, reason):
    report = ReportedSong(user_id=user_id, song_id=song_id, reason=reason)
    db.session.add(report)
    db.session.commit()

# Get all reports
def get_all_reports():
    reports = ReportedSong.query.all()
    return [report.serialize() for report in reports]

# Rate a song
def rate_song(user_id, song_id, rating):
    existing_rating = SongRating.query.filter_by(user_id=user_id, song_id=song_id).first()
    if existing_rating:
        existing_rating.rating = rating
    else:
        new_rating = SongRating(user_id=user_id, song_id=song_id, rating=rating)
        db.session.add(new_rating)
    db.session.commit()

# Get average rating of a song
def get_song_average_rating(song_id):
    ratings = SongRating.query.filter_by(song_id=song_id).all()
    if not ratings:
        return 0
    average = sum(rating.rating for rating in ratings) / len(ratings)
    return average

# Fetch a specific song by ID
def get_song_by_id(song_id):
    song = Song.query.get(song_id)
    if song:
        return song.serialize()
    return None



from datetime import datetime, date

def get_email_and_name_of_inactive_users():
    today = date.today()
    active_user_ids = db.session.query(RecentlyPlayedSongs.user_id).filter(db.func.date(RecentlyPlayedSongs.timestamp) == today).distinct()


    inactive_users = User.query.filter(~User.id.in_(active_user_ids)).all()


    result = [(user.email, f"{user.fname} {user.lname}") for user in inactive_users]
    return result

