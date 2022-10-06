''' Class for managing spotify related tasks (connection, playback, speaker_id) '''

from spotipy import Spotify, SpotifyOAuth, CacheFileHandler

class MySpotify:
    ''' Class for managing spotify related tasks (connection, playback, speaker_id) '''

    def __init__(self, mysettings):
        ''' Initialize connection to Spotify, speaker ID, sets its volume '''

        self.__spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=mysettings.cid,
                client_secret=mysettings.secret,
                redirect_uri = mysettings.redirect,
                scope=mysettings.scope,
                cache_handler=CacheFileHandler(username=mysettings.user),
                open_browser=False
            )
        )

        self.__speaker_id = self.get_device_id(
            self.__spotify.devices()['devices'],
            mysettings.speaker_name
            )

        if self.__speaker_id is None:
            raise Exception(f"No Spotify Device called {mysettings.speaker_name} available")

        self.__spotify.volume(mysettings.speaker_default_volume, device_id=self.__speaker_id)
        self.__playlist_items = []
        self.__currently_playing = ""

    def get_device_id(self, devices, device_name):
        ''' Checks spotify devices and retrieves ID of the one with SPEAKER_NAME value
        from settings '''
        for device in devices:
            if device['name'].startswith(device_name):
                return device['id']
        return None

    def start_playback(self, playlist_uri):
        ''' Starts to play give playlist '''
        if self.__currently_playing != playlist_uri:
            self.__playlist_items = []
            self.__currently_playing = playlist_uri

        if len(self.__playlist_items) == 0:
            tracks = self.__spotify.playlist_items(playlist_id=playlist_uri)['items']

            for track in tracks:
                self.__playlist_items.append(track['track']['uri'])

        self.__spotify.start_playback(
            device_id=self.__speaker_id,
            uris=[self.__playlist_items.pop(0)]
            )
