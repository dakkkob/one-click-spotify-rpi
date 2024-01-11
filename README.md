
# Spotify One-Click Play for Raspberry Pi

This repository contains a Python program designed for Raspberry Pi that allows users to play songs from specific Spotify playlists with the push of a button. The program is bound to hardware buttons on the Raspberry Pi. Each button is associated with a different Spotify playlist, and pressing a button starts playing a song from the corresponding playlist.

## Features

- **Button-Triggered Playback**: Each button on the Raspberry Pi triggers the playback of a song from a specific Spotify playlist.
- **Playlist Navigation**: Subsequent presses of the same button navigate through the playlist, playing one song at a time.
- **LED Feedback**: The program includes functionality to illuminate LEDs on the Raspberry Pi during the playback.

## Files in the Repository

1. `__init__.py`: Initialization script.
2. `main.py`: Main module that adds handlers for Raspberry Pi buttons. Each button is linked to a specific Spotify playlist, and pressing it starts or skips songs.
3. `settings.json.template`: Template for configuration settings including Spotify credentials, device names, playlist URIs, and LED configurations.
4. `settings.py`: Script to read and manage settings for the Spotify application.
5. `spotify.py`: Class that manages Spotify-related tasks such as connection, playback, and handling speaker IDs.

## Setup and Configuration

1. Clone the repository to your Raspberry Pi.
2. Rename `settings.json.template` to `settings.json` and fill in your Spotify details, including client ID, secret, and user information.
3. Make sure your Raspberry Pi is equipped with physical buttons and LEDs as required by the program.
4. Run `main.py` to start the application.

## Prerequisites

- A Raspberry Pi with internet access.
- Physical buttons and LEDs (optional) connected to the Raspberry Pi.
- A Spotify Premium account.

## Dependencies

- Python 3
- Spotipy library
- RPi.GPIO library

## Disclaimer

This project is not affiliated with Spotify. It's a third-party integration built using the Spotify API.
