#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import psutil
import time

class AceProxyPlayer(object):
    """AceProxyPlayer"""

    def __init__(self):
        self.url = None
        self.proxy = None
        self.player = None

        self.get_url()
        self.start_proxy()
        self.start_player()
        self.exit_handler()

    def get_url(self):
        try:
            url = sys.argv[1]
        except IndexError:
            url = ''

        if 'acestream' in url:
            url = url.replace('acestream://', '')
            url = 'http://localhost:8000/pid/' + url + '/acestream.mp4'

        self.url = url

    def start_proxy(self):
        if not self.proxy_running():
            self.proxy = psutil.Popen('aceproxy')
            time.sleep(5)

    def start_player(self):
        self.player = psutil.Popen(['vlc', self.url])
        self.player.wait()
        self.close_player()

    def proxy_running(self):
        ports = psutil.net_connections()

        for connection in ports:
            if connection.laddr[1] == 8000:
                return True

        return False

    def exit_handler(self):
        try:
            input()
        except KeyboardInterrupt:
            sys.exit(0)

    def close_player(self):
        if not self.proxy == None:
            self.proxy.terminate()

        if not self.player == None:
            self.player.terminate()

        sys.exit(0)

player = AceProxyPlayer()
