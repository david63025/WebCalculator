#! /usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------#
#                                                                       #
# Copyright (C) 2016, David A. Hall                                     #
#                     Eureka, MO USA                                    #
# This program is free software. You can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License Version 2.     #
#   This program is distributed in the hope that it is useful,          #
#   but WITHOUT ANY WARRANTY IMPLIED OR OTHERWISE.                      #
#                                                                       #
#-----------------------------------------------------------------------#

__version__ = "0.1.0"
__author__ = "David Hall"
__last_update__ = "19 March 2016"

import os.path
import cherrypy

current_dir = os.path.dirname(os.path.abspath(__file__))

class WebCalculator(object):
    _data = {
        "fromTemp": "40.0",
        "toTemp": "104.0",
        "fromDist": "3.0",
        "toDist": "5.0"
        }
        
    def _header(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Web Calculators</title>
            <link rel="stylesheet" type="text/css" href="webcalculator.css">
        </head>"""

    def _body(self, temperature, calc):
        if calc.endswith('c'):
            result = self._f2c(temperature)
            units1 = 'F'
            units2 = 'C'
        elif calc.endswith('f'):
            result = self._c2f(temperature)
            units1 = 'C'
            units2 = 'F'
        else:
            result = 999.9
            units1 = units2 = 'X'
        
        return """
        <body>
        <div class="header"> </div>
        <ul>
            <li><a class="active" href="#converters">Units Converters</a></li>
            <li><a href="#eecalc">Electronics Calculators</a></li>
            <li><a href="#simplecalc">Simple Calculator</a></li>
            <li><a href="#moon">Moon Almanac</a></li>
        </ul> </div>

        <div class="row">
        <div class="col-1"> </div>

        <div class="col-3">
            <form method="get" action="calculate">
            <h2>Enter Temperature: </h2><br>
            <input type="text" name="temperature" value= %.1f /> <br>
            <button class="button" type="submit" name="calc" value="f2c">&#176;F &#8680 &#176;C</button>
            <button class="button" type="submit" name="calc" value="c2f">&#176;C &#8680 &#176;F</button>
            <br>
            <h2>%.1f &#176;%s is %.1f &#176;%s</h2>
            </form>
        </div>

        <div class="col-1"> </div>

        <div class="col-3">
            <form method="get" action="calculate">
            <h2>Enter Distance: </h2><br>
            <input type="text" name="temperature" value= %.1f /> <br>
            <button class="button" type="submit" name="calc" value="mi2km">Miles &#8680 Kilometers</button>
            <button class="button" type="submit" name="calc" value="km2mi">Kilometers &#8680 Miles</button>
            <br>
            <h2>%.1f &#176;%s is %.1f &#176;%s</h2>
            </form>
        </div>

        <div class="col-1" </div>

        </body>""" % (temperature, temperature, units1, result, units2,
                      temperature, temperature, units1, result, units2) 

    def _footer(self):
        return """
        </form> </body> </html>"""

    def _c2f(self, temp):
        return 9.0 * temp / 5.0 + 32.0

    def _f2c(self, temp):
        return 5.0 * (temp - 32.0) / 9.0
    
    def _mi2km(self, dist):
        return 1.609344 * dist

    def _km2mi(self, dist):
        return dist / 1.609344

    @cherrypy.expose
    def index(self):
        return (self._header() + self._body(40.0, 'c2f') + self._footer())

    @cherrypy.expose
    def calculate(self, calc, temperature):
        return (self._header() + self._body(float(temperature), calc) + self._footer())

# end of class WebCalculator

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': current_dir,
            'tools.staticdir.dir': current_dir
        }
    }
    cherrypy.quickstart(WebCalculator(), '/', conf)
