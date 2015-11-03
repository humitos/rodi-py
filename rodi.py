#!/usr/bin/env python
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

'''
RoDI (Robot Didactico Inalambrico) module
'''

import time
import json
import requests  # fades.pypi


def wheel(wheel_pos):
    '''
    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    '''
    wheel_pos = 255 - wheel_pos
    if wheel_pos < 85:
        return (255 - wheel_pos * 3, 0, wheel_pos * 3)
    if wheel_pos < 170:
        wheel_pos -= 85
        return (0, wheel_pos * 3, 255 - wheel_pos * 3)
    wheel_pos -= 170
    return (wheel_pos * 3, 255 - wheel_pos * 3, 0)


class RoDI(object):
    '''
    The RoDI (Robot Didactico Inalambrico) class
    '''
    _URL = 'http://{ip}:{port}/{method}/{args}'
    BLINK_METHOD = 1
    SENSE_METHOD = 2
    MOVE_METHOD = 3
    SING_METHOD = 4
    SEE_METHOD = 5
    PIXEL_METHOD = 6
    LIGHT_METHOD = 7
    LED_METHOD = 8

    def __init__(self, ip='192.168.4.1', port='1234'):
        '''
        Constructor for the robot
        '''
        self.robot_ip = ip
        self.port = port

    def _build_url(self, method, args):
        '''
        Helper method to construct the server url
        '''
        args = map(str, args)
        url = self._URL.format(
            ip=self.robot_ip,
            port=self.port,
            method=method,
            args='/'.join(args),
        )
        return url

    def blink(self, milliseconds):
        '''
        Makes the robot blink its led for the specified time
        '''
        url = self._build_url(
            self.BLINK_METHOD,
            [milliseconds]
        )
        requests.get(url)

    def move(self, left_wheel_speed, right_wheel_speed):
        '''
        Makes the robot move
        '''
        url = self._build_url(
            self.MOVE_METHOD,
            [left_wheel_speed, right_wheel_speed]
        )
        requests.get(url)

    def move_left(self):
        '''
        Moves the robot (rotates) to the left
        '''
        self.move(-100, 100)

    def move_right(self):
        '''
        Moves the robot (rotates) to the right
        '''
        self.move(100, -100)

    def move_forward(self):
        '''
        Moves the robot forward
        '''
        self.move(100, 100)

    def move_backward(self):
        '''
        Moves the robot backwards
        '''
        self.move(-100, -100)

    def move_stop(self):
        '''
        Stops the robot
        '''
        self.move(0, 0)

    def sing(self, note, duration):
        '''
        Makes the robot sing

        You need to specify a note and a duration in miliseconds
        (Notes can be found in http://arduino.cc/en/tutorial/tone)
        '''
        url = self._build_url(
            self.SING_METHOD,
            [note, duration]
        )
        requests.get(url)

    def see(self):
        '''
        Makes the robot "see"

        It returns the distance of an object in front of the robot in cm
        '''
        url = self._build_url(
            self.SEE_METHOD,
            []
        )
        response = requests.get(url)
        return json.loads(response.content)

    def sense(self):
        '''
        Senses the status of the infrarred sensors (line follower)

        Returns the reflectance of the object beneath the robot
        with values from 0 (black) to 1023 (white)
        '''
        url = self._build_url(
            self.SENSE_METHOD,
            []
        )
        response = requests.get(url)
        return json.loads(response.content)

    def pixel(self, red, green, blue):
        '''
        Changes the color of the Pixel in the robot

        Takes thre values, red, green and blue from 0 to 255
        '''
        url = self._build_url(
            self.PIXEL_METHOD,
            [red, green, blue]
        )
        requests.get(url)

    def light(self):
        '''
        Senses the status of the light sensors

        Returns the luminosity of the ambient with values from 0 to 1023
        '''
        url = self._build_url(
            self.LIGHT_METHOD,
            []
        )
        response = requests.get(url)
        return json.loads(response.content)

    def led(self, state):
        '''
        Turns the led on or off

        values for state are 0: off and 1: on
        '''
        url = self._build_url(
            self.LED_METHOD,
            [state]
        )
        requests.get(url)

    def run_test(self):
        '''
        Method to run some tests for the robot
        '''
        print "RoDI turn led on"
        self.led(1)
        time.sleep(1)

        print "RoDI turn led off"
        self.led(0)
        time.sleep(1)

        print "RoDI blink"
        self.blink(200)
        time.sleep(1)

        print "RoDI move forward"
        self.move_forward()
        time.sleep(1)

        print "RoDI rotate left"
        self.move_left()
        time.sleep(1)

        print "RoDI move forward"
        self.move_forward()
        time.sleep(1)

        print "RoDI rotate right"
        self.move_right()
        time.sleep(1)

        print "RoDI move backward"
        self.move_backward()
        time.sleep(1)

        print "RoDI stop"
        self.move_stop()
        time.sleep(1)

        print "RoDI sing"
        self.sing(33, 1000)
        time.sleep(1)

        print "RoDI do a rainbow"
        for j in range(256):
            red, green, blue = wheel(j)
            self.pixel(red, green, blue)
            time.sleep(0.005)
        self.pixel(0, 0, 0)

        print "RoDI see"
        print " - I see something at %d cm" % self.see()
        time.sleep(1)

        print "RoDI sense"
        print " - My sensors sense: %s" % self.sense()
        time.sleep(1)

        print "RoDI see light"
        print " - My light sensor senses: %s" % self.light()
        self.blink(0)


if __name__ == '__main__':
    ROBOT = RoDI()
    ROBOT.run_test()
