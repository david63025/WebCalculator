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
        "fromTemp": "40.0&#176;C", "toTemp": "104.0&#176;F",
        "fromDist": "3.107 mi", "toDist": "5.000 km"
        }
        
    def _header(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Web Calculators</title>
            <link rel="stylesheet" type="text/css" href="webcalculator.css">
        </head>"""
        
    def _footer(self):
        return """
        </html>"""

    def _body(self):
        return """
        <body>
        <div class="header"> </div>
        <ul>
            <li><a class="active" href="http://localhost:8080">Units Converters</a></li>
            <li><a href="#eecalc">Electronics Calculators</a></li>
            <li><a href="#simplecalc">Simple Calculator</a></li>
            <li><a href="#moon">Moon Almanac</a></li>
        </ul> </div>

        <div class="row">
        <div class="col-1"> </div>

        <div class="col-3">
            <form method="get" action="calculate">
            <h2>Enter Temperature: </h2><br>
            <input type="text" name="value" value= %s /> <br>
            <button class="button" type="submit" name="calc" value="f2c">F &#8680 C</button>
            <button class="button" type="submit" name="calc" value="c2f">C &#8680 F</button>
            <br>
            <h2>%s is %s</h2>
            </form>
        </div>

        <div class="col-1"> </div>

        <div class="col-3">
            <form method="get" action="calculate">
            <h2>Enter Distance: </h2><br>
            <input type="text" name="value" value= %s /> <br>
            <button class="button" type="submit" name="calc" value="mi2km">Miles &#8680 Kilometers</button>
            <button class="button" type="submit" name="calc" value="km2mi">Kilometers &#8680 Miles</button>
            <br>
            <h2>%s is %s</h2>
            </form>
        </div>

        <div class="col-1" </div>

        </body>""" % (self._data['fromTemp'][:-7], self._data['fromTemp'], self._data['toTemp'],
                      self._data['fromDist'][:-2], self._data['fromDist'], self._data['toDist'])

    def _c2f(self, temp):
        return '%.1f&#176;F' % (9.0 * float(temp) / 5.0 + 32.0)

    def _f2c(self, temp):
        return "%.1f&#176;C" % (5.0 * (float(temp) - 32.0) / 9.0)
    
    def _mi2km(self, dist):
        return 1.609344 * dist

    def _km2mi(self, dist):
        return dist / 1.609344

    @cherrypy.expose
    def index(self):
        return (self._header() + self._body() + self._footer())

    @cherrypy.expose
    def calculate(self, calc, value):
        if calc.endswith('c'):
            self._data['toTemp'] = '%.1f&#176;C' % (5.0 * (float(value) - 32.0) / 9.0)
            self._data['fromTemp'] = '%.1f&#176;F' % float(value)
        elif calc.endswith('f'):
            self._data['toTemp'] = '%.1f&#176;F' % (9.0 * float(value) / 5.0 + 32.0)
            self._data['fromTemp'] = '%.1f&#176;C' % float(value)
        elif calc.endswith('km'):
            self._data['toDist'] = '%.3f km' % (float(value) * 1.609344)
            self._data['fromDist'] = '%.3f mi' % float(value)
        elif calc.endswith('mi'):
            self._data['toDist'] = '%.3f mi' % (float(value) / 1.609344)
            self._data['fromDist'] = '%.3f km' % float(value)
        else:
            result = '999.9'
            units1 = units2 = 'X'
        
        return (self._header() + self._body() + self._footer())

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
