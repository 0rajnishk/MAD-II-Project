from backend.api import AdminSongResource, AdminAlbumResource, Albums_Resource, BlacklistUsersResource, CeleryTestResource, ReportedSongsResource, SearchAlbumsResource, SearchCreatorsResource, SearchSongsResource, SearchUsersResource, SongPerformanceResource, StatsResource, TopSongResource, UserPlaylistRes, UserRole, WhitelistUserResource, api, AlbumResource, PlaylistResource, Song_Resource, SongRatingResource, SongResource,  UserResource, UsersResourceList, Album_Resource, ReportSongResource, LikeSongResource,RecentlyPlayedSongsResource, ExportJobs
from backend.auth import AuthResource

api.add_resource(AuthResource, '/api/login')   

api.add_resource(UserResource, '/api/users/<int:id>')
api.add_resource(UsersResourceList, '/api/users')

api.add_resource(AlbumResource, '/api/albums')
api.add_resource(SongResource, '/api/songs')

api.add_resource(AdminSongResource, '/api/admin/songs')
api.add_resource(AdminAlbumResource, '/api/admin/albums')

api.add_resource(PlaylistResource, '/api/playlists')
api.add_resource(SongRatingResource, '/api/rating')

api.add_resource(Song_Resource, '/api/songs/audio/<int:song_id>')
api.add_resource(Albums_Resource, '/api/albums/<int:album_id>')

api.add_resource(Album_Resource, '/api/album/<int:album_id>')

api.add_resource(ReportSongResource, '/api/report')
api.add_resource(LikeSongResource, '/api/like')

api.add_resource(RecentlyPlayedSongsResource, '/api/recently_played_songs')
api.add_resource(SearchSongsResource, '/api/search_songs')
api.add_resource(SearchAlbumsResource, '/api/search_albums')
api.add_resource(UserRole, '/api/update_role')
api.add_resource(StatsResource, '/api/stats')

api.add_resource(SongPerformanceResource, '/api/stats/song_performance')
api.add_resource(TopSongResource, '/api/stats/top_songs')


api.add_resource(ReportedSongsResource, '/api/reported_songs')
api.add_resource(SearchUsersResource, '/api/search_users')
api.add_resource(SearchCreatorsResource, '/api/search_creators')


api.add_resource(BlacklistUsersResource, '/api/blacklist_users')
api.add_resource(WhitelistUserResource, '/api/whitelist_users')


api.add_resource(UserPlaylistRes, '/api/playlist')



api.add_resource(CeleryTestResource, '/api/celery_test')
api.add_resource(ExportJobs, '/api/export')