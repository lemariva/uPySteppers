"""
Copyright 2020 LeMaRiva|Tech (Mauro Riva) info@lemariva.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import utime
from config import *

from webserver import webserver
from stepper import STEPPER

server = webserver()
server.run()

stepper = STEPPER(motor_config)

while True:
    if server.check_data():
        rotation = int(server.rotation/360 * motor_config['number_of_steps'])
        speed = int(motor_config['max_speed'] * server.speed / 100)
       
        brake = server.brake
        server.busy = True
        clockwise = server.clockwise
        if not clockwise:
            rotation = -rotation

        stepper.step(rotation, speed, brake)
        server.busy = False