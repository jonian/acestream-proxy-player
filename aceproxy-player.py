#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AceProxy Player: Open acestream links with any media player"""

import sys
import time
import socket
import urllib
import psutil
import notify2
import argparse

class AceProxyPlayer(object):
    """AceProxy Player"""

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

        self.appname = 'Acestream Proxy Player'
        self.args = parser.parse_args()

        notify2.init(self.appname)
        self.notifier = notify2.Notification(self.appname)

        self.parse_url()
        self.start_proxy()
        self.start_session()
        self.start_player()
        self.close_player()

    def notify(self, message):
        """Show player status notifications"""

        icon = self.args.player
        messages = {
            'running': 'Acestream local proxy running.',
            'missing': 'Acestream local proxy not installed!',
            'waiting': 'Waiting for channel response...',
            'started': 'Streaming started. Launching player.',
            'unavailable': 'Acestream channel unavailable!'
        }

        print(messages[message])
        self.notifier.update(self.appname, messages[message], icon)
        self.notifier.show()

    def parse_url(self):
        """Parse the given url"""

        url = self.args.url
        host = self.args.host
        port = self.args.port

        if 'acestream' in url:
            url = url.split('//')[1]
            url = 'http://' + host + ':' + port + '/pid/' + url + '/acestream.mp4'

        elif 'http' in url:
            url = urllib.parse.quote_plus(url)
            url = 'http://' + host + ':' + port + '/torrent/' + url + '/torrent.mp4'

        else:
            url = 'http://' + host + ':' + port + '/' + url

        self.url = url

    def start_proxy(self):
        """Start aceproxy if not running"""

        if self.args.host not in ['localhost', '127.0.0.1', '0.0.0.0']:
            return

        for process in psutil.process_iter():
            if 'aceproxy' in process.name():
                process.kill()

            if 'acestreamengine' in process.name():
                process.kill()

        try:
            self.proxy = psutil.Popen('aceproxy')
            self.notify('running')
            time.sleep(5)
        except FileNotFoundError:
            self.notify('missing')
            self.close_player(1)

    def start_session(self):
        """Start player socket session"""

        self.notify('waiting')
        time.sleep(15)

        try:
            session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            session.settimeout(30)
            session.connect((self.args.host, int(self.args.port)))
            session.close()

            self.notify('started')
        except socket.error:
            self.notify('unavailable')
            self.close_player(1)

    def start_player(self):
        """Start the media player"""

        self.player = psutil.Popen([self.args.player, self.url])
        self.player.wait()

    def close_player(self, code=0):
        """Close aceproxy and media player"""

        try:
            self.proxy.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('AceProxy not running...')

        try:
            self.player.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        sys.exit(code)

def main():
    """Start AceProxy Player"""

    try:
        AceProxyPlayer()
    except (KeyboardInterrupt, EOFError):
        print('AceProxy Player exiting...')
        sys.exit(0)

main()
