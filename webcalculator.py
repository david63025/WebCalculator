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
__last_update__ = "13 March 2016"

import cherrypy

class WebCalculator(object):
    def _header(self):
        return """
        <!DOCTYPE html>
        <html>
        <head> </head>"""

    def _styles(self):
        return """
        <style>
        input[type=text] {
            width: 100%;
            box-sizing: border-box;
            padding: 10px 10px;
            margin: 10px 10px;
            border: 1px solid #cccccc;
            border-radius: 8px;
            font-size: 18px;
            text-align: center;
        }
        .button {
            width: 100%;
            box-sizing: border-box;
            background-color: #4caf50;
            color: white;
            padding: 10px 10px;
            margin: 10px 10px;
            border: none;
            text-align: center;
            text-decoration: none;
            font-size: 18px;
            border-radius: 8px;
        }
        div {
            width: 25%;
            border-radius: 5px;
            background-color: #f2f2f2;
            padding: 40px;
        }
        h2 {
            text-align: left;
        }
        </style>"""

    def _body(self, temperature, calc):
        if calc.endswith('C'):
            result = self._f2c(temperature)
            units1 = 'F'
            units2 = 'C'
        elif calc.endswith('F'):
            result = self._c2f(temperature)
            units1 = 'C'
            units2 = 'F'
        else:
            result = 999.9
            units1 = units2 = 'X'
        
        return """
        <body>
        <div>
        <form method="get" action="calculate">
        <h2>Enter Temperature: </h2><br>
        <input type="text" value= %.1f name="temperature" /> <br>
        <button class="button" type="submit" name="calc" value="F2C">&#176;F &#8680 &#176;C</button>
        <button class="button" type="submit" name="calc" value="C2F">&#176;C &#8680 &#176;F</button>
        <br>
        <h2>%.1f &#176;%s is %.1f &#176;%s</h2>
        </form> </div> </body>""" % (temperature, temperature, units1, result, units2) 

    def _footer(self):
        return """
        </form> </body> </html>"""

    def _c2f(self, temp):
        return 9.0 * temp / 5.0 + 32.0

    def _f2c(self, temp):
        return 5.0 * (temp - 32.0) / 9.0

    @cherrypy.expose
    def index(self):
        return (self._header() + self._styles() +
                self._body(40.0, 'C2F') + self._footer())

    @cherrypy.expose
    def calculate(self, calc, temperature):
        return (self._header() + self._styles() +
                self._body(float(temperature), calc) + self._footer())

# end of class WebCalculator

if __name__ == '__main__':
    cherrypy.quickstart(WebCalculator())
