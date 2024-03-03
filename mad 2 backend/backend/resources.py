from backend.api import AlbumResource, PlaylistResource, SongRatingResource, SongResource, api, UserResource, UsersResourceList
from backend.auth import AuthResource



api.add_resource(AuthResource, '/api/login')   

api.add_resource(UserResource, '/api/users/<int:id>')
api.add_resource(UsersResourceList, '/api/users')

api.add_resource(AlbumResource, '/api/albums')
api.add_resource(SongResource, '/api/songs')
api.add_resource(PlaylistResource, '/api/playlist')
api.add_resource(SongRatingResource, '/api/rating')