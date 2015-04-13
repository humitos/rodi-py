# Copyright (C) 2015 Manuel Kaufmann - humitos@gmail.com

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import time
import json
import requests  # fades.pypi


class RoDi(object):

    _URL = 'http://{ip}:{port}/{method}/{args}'
    BLINK_METHOD = 1
    SENSE_METHOD = 2
    MOVE_METHOD = 3
    SING_METHOD = 4
    SEE_METHOD = 5

    def __init__(self, ip='192.168.4.1', port='1234'):
        self.IP = ip
        self.PORT = port

    def _build_url(self, method, args):
        args = map(str, args)
        url = self._URL.format(
            ip=self.IP,
            port=self.PORT,
            method=method,
            args='/'.join(args),
        )
        return url

    def blink(self, milliseconds):
        url = self._build_url(
            self.BLINK_METHOD,
            [milliseconds]
        )
        requests.get(url)

    def move(self, left_wheel_speed, right_wheel_speed):
        url = self._build_url(
            self.MOVE_METHOD,
            [left_wheel_speed, right_wheel_speed]
        )
        requests.get(url)

    def move_left(self):
        self.move(-100, 100)

    def move_right(self):
        self.move(100, -100)

    def move_forward(self):
        self.move(100, 100)

    def move_backward(self):
        self.move(-100, -100)

    def move_stop(self):
        self.move(0, 0)

    def sing(self, note, duration):
        # Notes can be found in http://arduino.cc/en/tutorial/tone
        url = self._build_url(
            self.SING_METHOD,
            [note, duration]
        )
        requests.get(url)

    def see(self):
        url = self._build_url(
            self.SEE_METHOD,
            []
        )
        response = requests.get(url)
        return json.loads(response.content)

    def run_test(self):
        self.blink(1000)
        time.sleep(1)
        self.move_forward()
        time.sleep(1)
        self.move_left()
        time.sleep(1)
        self.move_forward()
        time.sleep(1)
        self.move_right()
        time.sleep(1)
        self.move_backward()
        time.sleep(1)
        self.move_stop()
        time.sleep(1)
        self.blink(0)
        self.sing(33, 1000)
        print(self.see())
