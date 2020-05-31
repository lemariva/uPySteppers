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

import gc
import machine
import json
import time

from microWebSrv import MicroWebSrv

class webserver():

    def __init__(self):

        self.rotation = 360
        self.delay = 1000
        self.speed = 50
        self.clockwise = True
        self.brake = True

        self._busy = False
        self._newdata = False

        self.routeHandlers = [
            ("/", "GET", self._httpHandlerIndex),
            ("/logo.svg", "GET", self._httpLogo),
            ("/upy/<rotation>/<delay>/<speed>/<clockwise>/<brake>", "GET", self._httpHandlerSetData),
            ("/upy", "GET", self._httpHandlerGetData),
            ("/memory/<query>", "GET", self._httpHandlerMemory)
        ]

    def run(self):
        mws = MicroWebSrv(routeHandlers=self.routeHandlers, webPath="www/")
        mws.Start(threaded=True)
        gc.collect()

    def busy(self, state=None):
        if state is not None:
            self._busy = state
        else:
            return self._busy

    def check_data(self):
        newdata = self._newdata
        self._newdata = False
        return newdata

    def _httpLogo(self, httpClient, httpResponse):
        f = open("www/logo.svg", "r")
        content =  f.read()
        f.close()

        httpResponse.WriteResponseOk(headers=None,
                                    contentType="image/svg+xml",
                                    contentCharset="UTF-8",
                                    content=content)


    def _httpHandlerIndex(self, httpClient, httpResponse):
        f = open("www/index.html", "r")
        content =  f.read()
        f.close()

        httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=content)

    def _httpHandlerSetData(self, httpClient, httpResponse, routeArgs):
        self.rotation = int(routeArgs['rotation'])
        self.delay = int(routeArgs['delay'])
        self.clockwise = int(routeArgs['clockwise'])
        self.speed = int(routeArgs['speed'])
        self.brake = int(routeArgs['brake'])

        #print("In EDIT HTTP variable route :")

        data = {
            'rotation': self.rotation,
            'delay': self.delay,
            'clockwise': self.clockwise,
            'speed': self.speed,
            'brake': self.brake
        }
        self._newdata = True
        httpResponse.WriteResponseOk(headers=None,
                                        contentType="text/html",
                                        contentCharset="UTF-8",
                                        content=json.dumps(data))

    def _httpHandlerGetData(self, httpClient, httpResponse):
        print("In Get HTTP variable route :")
        data = {
            'rotation': self.rotation,
            'delay': self.delay,
            'clockwise': self.clockwise,
            'speed': self.speed,
            'brake': self.brake
        }

        httpResponse.WriteResponseOk(headers=None,
                                    contentType="application/json",
                                    contentCharset="UTF-8",
                                    content=json.dumps(data))

    def _httpHandlerMemory(self, httpClient, httpResponse, routeArgs):
        print("In Memory HTTP variable route :")
        query = str(routeArgs['query'])

        if 'gc' in query or 'collect' in query:
            gc.collect()

        content = """\
            {}
            """.format(gc.mem_free())
        httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=content)




