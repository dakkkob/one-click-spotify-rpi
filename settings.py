''' Reads and holds settings of the spotify one click app '''

import json

class Settings:
    ''' Reads and holds settings of the spotify one click app '''

    SETTINGS_FILE_PATH = "settings.json"

    def __init__(self) -> None:
        self.settings = self.load_settings()

        self.cid                     = self.get_setting('CID')
        self.secret                  = self.get_setting('SECRET')
        self.user                    = self.get_setting('USER')
        self.scope                   = self.get_setting('SCOPE')
        self.redirect                = self.get_setting('REDIRECT')
        self.speaker_name            = self.get_setting('SPEAKER_NAME')
        self.speaker_default_volume  = self.get_setting('SPEAKER_DEFAULT_VOLUME')
        self.playlist_mo_uri         = self.get_setting('PLAYLIST_MO_URI')
        self.playlist_we_uri         = self.get_setting('PLAYLIST_WE_URI')
        self.playlist_th_uri         = self.get_setting('PLAYLIST_TH_URI')
        self.leds                    = self.get_setting('LEDS')

    def load_settings(self):
        ''' Loads settings from the settings file '''
        try:
            with open(self.SETTINGS_FILE_PATH, mode='r', encoding='utf-8') as settings_file:
                return json.loads(settings_file.read())
        except FileNotFoundError as exc:
            raise f"Configuration file {self.SETTINGS_FILE_PATH} not found" from exc

    def get_setting(self, name):
        ''' Returns value called name from given dictionary '''

        assert self.settings

        if name not in self.settings:
            raise Exception(
                f"Configuration item {name} not found in settings file {self.SETTINGS_FILE_PATH}"
                )
        return self.settings[name]
    