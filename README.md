# Aceproxy Player
Aceproxy Player allows you to open Ace Stream links with a Media Player of your choice

## Dependencies
    python, python-psutil, python-urllib3, python-notify2

## Usage
    aceproxy-player [--host HOST] [--port PORT] [--player PLAYER] URL

## Positional arguments
    URL              The acestream url to play

## Optional arguments
    -h, --help       Show help message and exit
    --host HOST      The aceproxy server host (default: localhost)
    --port PORT      The aceproxy server port (default: 8000)
    --player PLAYER  The media player to use (default: vlc)
