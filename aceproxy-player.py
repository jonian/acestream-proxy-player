#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import time
import urllib
import psutil
import argparse

class AceProxyPlayer(object):
    """AceProxy Player: Open acestream links with any media player"""

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='aceproxy-player',
            description='Open acestream links with any media player'
        )
        parser.add_argument(
            'url',
            metavar='URL',
            help='The acestream url to play'
        )
        parser.add_argument(
            '--host',
            help='The aceproxy server host (default: localhost)',
            default='localhost'
        )
        parser.add_argument(
            '--port',
            help='The aceproxy server port (default: 8000)',
            default='8000'
        )
        parser.add_argument(
            '--player',
            help='The media player to use (default: vlc)',
            default='vlc'
        )

        self.args = parser.parse_args()

        self.start_proxy()
        self.parse_url()
        self.start_player()
        self.close_player()

    def parse_url(self):
        """Parse the given url"""

        url = self.args.url
        host = self.args.host
        port = self.args.port

        if 'acestream' in url:
            url = url.replace('acestream://', '')
            url = 'http://' + host + ':' + port + '/pid/' + url + '/acestream.mp4'

        if 'torrent' in url:
            url = urllib.quote_plus(url)
            url = 'http://' + host + ':' + port + '/torrent/' + url + '/torrent.mp4'

        self.url = url

    def start_proxy(self):
        """Start aceproxy if not running"""

        for process in psutil.process_iter():
            if 'acestreamengine' in process.name():
                return

        self.proxy = psutil.Popen('aceproxy')
        time.sleep(5)

    def start_player(self):
        """Start the media player"""

        self.player = psutil.Popen([self.args.player, self.url])
        self.player.wait()

    def close_player(self):
        """Close aceproxy and media player"""

        try:
            self.proxy.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('AceProxy not running...')

        try:
            self.player.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        sys.exit(0)

def main():
    """Start AceProxy Player"""

    try:
        AceProxyPlayer()
    except (KeyboardInterrupt, EOFError):
        print('AceProxy Player exiting...')
        sys.exit(0)

main()
