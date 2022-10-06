''' This module adds handlers for 3 RPi buttons.
Each of them starts playing of specific Spotify playlist
on given Spotify device. Further pressing of the button
skips to next track '''

import sys
import time
import threading
from signal import pause
from queue import Queue
from RPi import GPIO
from settings import Settings
from spotify import MySpotify

def start_playing_playlist(playlist_uri, spotify, leds, queue):
    ''' Button handler function, resets the LEDs, starts playback of selected
    Spotify playlist and illuminates the LEDs '''

    spotify.start_playback(playlist_uri)

    if not queue.empty():
        queue.get(timeout=2)
        time.sleep(1)

    thread_for_leds = threading.Thread(target=illuminate, args=(queue,leds,))
    thread_for_leds.start()

def illuminate(queue, leds):
    ''' Illuminates the LEDs '''
    queue.put("working")
    time.sleep(1)
    switch_off_all_leds(leds)
    for led in mysettings.leds:
        for _ in range(0,30):
            change_led_status(led, leds, GPIO.LOW, queue)
            change_led_status(led, leds, GPIO.HIGH, queue)
    switch_off_all_leds(leds)
    queue.get(timeout=2)

def change_led_status(led, leds, status, queue):
    ''' Changes status of given LED '''
    check_if_exit(queue, leds)
    GPIO.output(led, status)
    time.sleep(0.5)

def check_if_exit(queue, leds):
    ''' Keeps checking the synchronization queue so that it stops the thread
    if user pressed another button earlier (before the song ends) '''
    if queue.empty():
        switch_off_all_leds(leds)
        sys.exit()

def switch_off_all_leds(leds):
    ''' Turns off all LEDs '''
    for led in leds:
        GPIO.output(led, GPIO.LOW)

def setup_gpio(leds, spotify, queue):
    ''' Sets up GPIO devices '''
    GPIO.setmode(GPIO.BCM)
    for led in leds:
        GPIO.setup(led, GPIO.OUT)

    setup_gpio_button(20, lambda val: start_playing_playlist(
                            playlist_uri=mysettings.playlist_mo_uri,
                            spotify=spotify,
                            leds=leds,
                            queue=queue
                            )
                      )
    setup_gpio_button(22, lambda val: start_playing_playlist(
                            playlist_uri=mysettings.playlist_we_uri,
                            spotify=spotify,
                            leds=leds,
                            queue=queue
                            )
                      )
    setup_gpio_button(23, lambda val: start_playing_playlist(
                            playlist_uri=mysettings.playlist_th_uri,
                            spotify=spotify,
                            leds=leds,
                            queue=queue))

def setup_gpio_button(gpio_port, callback):
    ''' Sets up a button and assigns it a callback function '''
    GPIO.setup(gpio_port, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(
        gpio_port,
        GPIO.RISING,
        callback=callback,
        bouncetime=1500
    )

mysettings = Settings()
myspotify  = MySpotify(mysettings)
myqueue = Queue()
setup_gpio(mysettings.leds, myspotify, myqueue)

print("Initialization done, waiting for buttonos ...")
pause()
