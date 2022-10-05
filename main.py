''' This module adds handlers for 3 RPi buttons.
Each of them starts playing of specific Spotify playlist
on given Spotify device. Further pressing of the button
skips to next track '''

import sys
import time
import threading
import json
from signal import pause
from queue import Queue
from spotipy import Spotify, SpotifyOAuth, CacheFileHandler
from RPi import GPIO

SETTINGS_FILE_PATH = "settings.json"

def load_settings():
    ''' Loads settings from the settings file '''
    try:
        with open(SETTINGS_FILE_PATH, mode='r', encoding='utf-8') as settings_file:
            return json.loads(settings_file.read())
    except FileNotFoundError as exc:
        raise f"Configuration file {SETTINGS_FILE_PATH} not found" from exc

def get_device_id(devices, device_name):
    ''' Checks spotify devices and retrieves ID of the one with SPEAKER_NAME value
    from settings '''
    for device in devices:
        if device['name'].startswith(device_name):
            return device['id']
    return None

def get_setting(mysettings, name):
    ''' Returns value called name from given dictionary '''
    if name not in mysettings:
        raise Exception(
            f"Configuration item {name} not found in settings file {SETTINGS_FILE_PATH}"
            )
    return mysettings[name]

settings = load_settings()

cid                     = get_setting(settings, 'CID')
secret                  = get_setting(settings, 'SECRET')
user                    = get_setting(settings, 'USER')
scope                   = get_setting(settings, 'SCOPE')
redirect                = get_setting(settings, 'REDIRECT')
speaker_name            = get_setting(settings, 'SPEAKER_NAME')
speaker_default_volume  = get_setting(settings, 'SPEAKER_DEFAULT_VOLUME')
playlist_mo_uri         = get_setting(settings, 'PLAYLIST_MO_URI')
playlist_we_uri         = get_setting(settings, 'PLAYLIST_WE_URI')
playlist_th_uri         = get_setting(settings, 'PLAYLIST_TH_URI')
leds                    = get_setting(settings, 'LEDS')

spotify = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=cid,
        client_secret=secret,
        redirect_uri = redirect,
        scope=scope,
        cache_handler=CacheFileHandler(username=user),
        open_browser=False
    )
)
speaker_id = get_device_id(spotify.devices()['devices'], speaker_name)

if speaker_id is None:
    raise f"No Spotify Device called {speaker_name} available"

spotify.volume(speaker_default_volume, device_id=speaker_id)
playlist_items = []
GPIO.setmode(GPIO.BCM)
queue = Queue()

def start_playing_playlist(playlist_uri):
    ''' Button handler function, resets the LEDs, starts playback of selected
    Spotify playlist and illuminates the LEDs '''

    if len(playlist_items) == 0:
        tracks = spotify.playlist_items(playlist_id=playlist_uri)['items']

        for track in tracks:
            playlist_items.append(track['track']['uri'])

    spotify.start_playback(device_id=speaker_id, uris=[playlist_items.pop(0)])

    if not queue.empty():
        queue.get(timeout=2)
        time.sleep(1)

    thread_for_leds = threading.Thread(target=illuminate, args=(queue,))
    thread_for_leds.start()

def illuminate(myqueue):
    ''' Illuminates the LEDs '''
    myqueue.put("working")
    switch_off_all_leds()
    for led in leds:
        blink_for_30s_and_stay_on(led, myqueue)
    switch_off_all_leds()
    myqueue.get(timeout=2)

def blink_for_30s_and_stay_on(led, myqueue):
    ''' Blinks single LED for 30s and keeps it on in the end '''
    for _ in range(0,30):
        check_if_exit(myqueue)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.5)
        check_if_exit(myqueue)
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)

def check_if_exit(myqueue):
    ''' Keeps checking the synchronization queue so that it stops the thread
    if user pressed another button earlier (before the song ends) '''
    if myqueue.empty():
        switch_off_all_leds()
        sys.exit()

def switch_off_all_leds():
    ''' Turns off all LEDs '''
    for led in leds:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)

GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(
    20,
    GPIO.BOTH,
    callback=lambda val: start_playing_playlist(playlist_mo_uri),
    bouncetime=1500
    )
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(
    22,
    GPIO.BOTH,
    callback=lambda val: start_playing_playlist(playlist_we_uri),
    bouncetime=1500
    )
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(
    23,
    GPIO.BOTH,
    callback=lambda val: start_playing_playlist(playlist_th_uri),
    bouncetime=1500
    )

print("There we are")
pause()
