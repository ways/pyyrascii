#!/usr/bin/env python
# -*- coding: UTF-8; -*-

"""
PyYrAscii
-------

PyYrAscii is a simple python grapher for using Yr.no’s weather data API.

You are welcome to participate in this project!
"""

__version__ = '0.1a'
__url__ = 'https://github.com/ways/pyyrascii'
__license__ = 'GPL License'
__docformat__ = 'markdown'

import SocketServer, subprocess, re, sys
import pyyrlib

def pyyrascii (location):
  weatherdata = pyyrlib.returnWeatherData(location, True)
  #print weatherdata
  #weatherdata = {'tabular': [{'from': u'2012-01-17T21:00:00', 'temperature': u'-3', 'pressure': u'1022.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-17T22:00:00', 'windSpeed': {'mps': u'1.3', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-17T22:00:00', 'temperature': u'-2', 'pressure': u'1022.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-17T23:00:00', 'windSpeed': {'mps': u'0.5', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-17T23:00:00', 'temperature': u'-2', 'pressure': u'1022.3', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T00:00:00', 'windSpeed': {'mps': u'0.4', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T00:00:00', 'temperature': u'-2', 'pressure': u'1022.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T01:00:00', 'windSpeed': {'mps': u'0.0', 'name': u'Stille'}, 'symbolnumber': u'4', 'windDirection': {'code': u'S', 'degrees': None, 'name': u'S\xf8r'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T01:00:00', 'temperature': u'-2', 'pressure': u'1021.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T02:00:00', 'windSpeed': {'mps': u'0.7', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'NNE', 'degrees': None, 'name': u'Nord-nord\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T02:00:00', 'temperature': u'-2', 'pressure': u'1020.9', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T03:00:00', 'windSpeed': {'mps': u'0.9', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'ENE', 'degrees': None, 'name': u'\xd8st-nord\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T03:00:00', 'temperature': u'-2', 'pressure': u'1020.5', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T04:00:00', 'windSpeed': {'mps': u'0.6', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'E', 'degrees': None, 'name': u'\xd8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T04:00:00', 'temperature': u'-2', 'pressure': u'1020.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T05:00:00', 'windSpeed': {'mps': u'0.5', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'ENE', 'degrees': None, 'name': u'\xd8st-nord\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T05:00:00', 'temperature': u'-3', 'pressure': u'1019.2', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T06:00:00', 'windSpeed': {'mps': u'1.3', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'E', 'degrees': None, 'name': u'\xd8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T06:00:00', 'temperature': u'-3', 'pressure': u'1018.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T07:00:00', 'windSpeed': {'mps': u'1.1', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'ESE', 'degrees': None, 'name': u'\xd8st-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T07:00:00', 'temperature': u'-3', 'pressure': u'1017.8', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T08:00:00', 'windSpeed': {'mps': u'1.0', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'E', 'degrees': None, 'name': u'\xd8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T08:00:00', 'temperature': u'-3', 'pressure': u'1017.4', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T09:00:00', 'windSpeed': {'mps': u'1.0', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'E', 'degrees': None, 'name': u'\xd8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T09:00:00', 'temperature': u'-3', 'pressure': u'1016.5', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T10:00:00', 'windSpeed': {'mps': u'1.5', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'ESE', 'degrees': None, 'name': u'\xd8st-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T10:00:00', 'temperature': u'-2', 'pressure': u'1016.2', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T11:00:00', 'windSpeed': {'mps': u'1.2', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T11:00:00', 'temperature': u'-2', 'pressure': u'1014.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T12:00:00', 'windSpeed': {'mps': u'1.8', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'ESE', 'degrees': None, 'name': u'\xd8st-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T12:00:00', 'temperature': u'-2', 'pressure': u'1013.2', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T13:00:00', 'windSpeed': {'mps': u'1.7', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SE', 'degrees': None, 'name': u'S\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T13:00:00', 'temperature': u'-1', 'pressure': u'1012.1', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T14:00:00', 'windSpeed': {'mps': u'1.7', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T14:00:00', 'temperature': u'-1', 'pressure': u'1011.1', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T15:00:00', 'windSpeed': {'mps': u'1.8', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'S', 'degrees': None, 'name': u'S\xf8r'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T15:00:00', 'temperature': u'0', 'pressure': u'1009.1', 'precipitation': u'2.2', 'period': None, 'to': u'2012-01-18T16:00:00', 'windSpeed': {'mps': u'1.7', 'name': u'Svak vind'}, 'symbolnumber': u'13', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Sn\xf8'}, {'from': u'2012-01-18T16:00:00', 'temperature': u'0', 'pressure': u'1007.1', 'precipitation': u'1.2', 'period': None, 'to': u'2012-01-18T17:00:00', 'windSpeed': {'mps': u'1.5', 'name': u'Flau vind'}, 'symbolnumber': u'12', 'windDirection': {'code': u'SSE', 'degrees': None, 'name': u'S\xf8r-s\xf8r\xf8st'}, 'symbolname': u'Sludd'}, {'from': u'2012-01-18T17:00:00', 'temperature': u'1', 'pressure': u'1006.0', 'precipitation': u'0.2', 'period': None, 'to': u'2012-01-18T18:00:00', 'windSpeed': {'mps': u'2.7', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T18:00:00', 'temperature': u'2', 'pressure': u'1005.4', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T19:00:00', 'windSpeed': {'mps': u'3.1', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SW', 'degrees': None, 'name': u'S\xf8rvest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-18T19:00:00', 'temperature': u'2', 'pressure': u'1004.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T20:00:00', 'windSpeed': {'mps': u'2.4', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'SW', 'degrees': None, 'name': u'S\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-18T20:00:00', 'temperature': u'2', 'pressure': u'1003.7', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T21:00:00', 'windSpeed': {'mps': u'2.3', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-18T21:00:00', 'temperature': u'2', 'pressure': u'1003.8', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T22:00:00', 'windSpeed': {'mps': u'2.7', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-18T22:00:00', 'temperature': u'0', 'pressure': u'1004.1', 'precipitation': u'0', 'period': None, 'to': u'2012-01-18T23:00:00', 'windSpeed': {'mps': u'2.0', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-18T23:00:00', 'temperature': u'-1', 'pressure': u'1004.3', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T00:00:00', 'windSpeed': {'mps': u'1.1', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T00:00:00', 'temperature': u'-2', 'pressure': u'1003.9', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T01:00:00', 'windSpeed': {'mps': u'1.9', 'name': u'Svak vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T01:00:00', 'temperature': u'-2', 'pressure': u'1003.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T02:00:00', 'windSpeed': {'mps': u'1.3', 'name': u'Flau vind'}, 'symbolnumber': u'1', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Klarv\xe6r'}, {'from': u'2012-01-19T02:00:00', 'temperature': u'-3', 'pressure': u'1002.8', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T03:00:00', 'windSpeed': {'mps': u'0.7', 'name': u'Flau vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'S', 'degrees': None, 'name': u'S\xf8r'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T03:00:00', 'temperature': u'-5', 'pressure': u'1002.2', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T04:00:00', 'windSpeed': {'mps': u'1.9', 'name': u'Svak vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'SW', 'degrees': None, 'name': u'S\xf8rvest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T04:00:00', 'temperature': u'-5', 'pressure': u'1001.5', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T05:00:00', 'windSpeed': {'mps': u'2.2', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T05:00:00', 'temperature': u'-4', 'pressure': u'1000.7', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T06:00:00', 'windSpeed': {'mps': u'1.3', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-19T06:00:00', 'temperature': u'-5', 'pressure': u'1001.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T07:00:00', 'windSpeed': {'mps': u'2.2', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T07:00:00', 'temperature': u'-5', 'pressure': u'1000.7', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T08:00:00', 'windSpeed': {'mps': u'2.0', 'name': u'Svak vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T08:00:00', 'temperature': u'-5', 'pressure': u'1000.5', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T09:00:00', 'windSpeed': {'mps': u'2.0', 'name': u'Svak vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T09:00:00', 'temperature': u'-5', 'pressure': u'1000.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T10:00:00', 'windSpeed': {'mps': u'1.5', 'name': u'Flau vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T10:00:00', 'temperature': u'-4', 'pressure': u'999.7', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T11:00:00', 'windSpeed': {'mps': u'1.5', 'name': u'Flau vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-19T11:00:00', 'temperature': u'-5', 'pressure': u'999.8', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T12:00:00', 'windSpeed': {'mps': u'1.6', 'name': u'Svak vind'}, 'symbolnumber': u'4', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Skyet'}, {'from': u'2012-01-19T12:00:00', 'temperature': u'-3', 'pressure': u'999.1', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T13:00:00', 'windSpeed': {'mps': u'0.8', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'WNW', 'degrees': None, 'name': u'Vest-nordvest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T13:00:00', 'temperature': u'-3', 'pressure': u'998.8', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T14:00:00', 'windSpeed': {'mps': u'0.7', 'name': u'Flau vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T14:00:00', 'temperature': u'-3', 'pressure': u'998.6', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T15:00:00', 'windSpeed': {'mps': u'1.1', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T15:00:00', 'temperature': u'-3', 'pressure': u'998.5', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T16:00:00', 'windSpeed': {'mps': u'0.9', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'SW', 'degrees': None, 'name': u'S\xf8rvest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T16:00:00', 'temperature': u'-4', 'pressure': u'999.0', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T17:00:00', 'windSpeed': {'mps': u'1.4', 'name': u'Flau vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'SSW', 'degrees': None, 'name': u'S\xf8r-s\xf8rvest'}, 'symbolname': u'Delvis skyet'}, {'from': u'2012-01-19T17:00:00', 'temperature': u'-4', 'pressure': u'998.9', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T18:00:00', 'windSpeed': {'mps': u'1.0', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'WSW', 'degrees': None, 'name': u'Vest-s\xf8rvest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T18:00:00', 'temperature': u'-4', 'pressure': u'999.2', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T19:00:00', 'windSpeed': {'mps': u'1.5', 'name': u'Flau vind'}, 'symbolnumber': u'2', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Lettskyet'}, {'from': u'2012-01-19T19:00:00', 'temperature': u'-4', 'pressure': u'999.1', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T20:00:00', 'windSpeed': {'mps': u'0.8', 'name': u'Flau vind'}, 'symbolnumber': u'1', 'windDirection': {'code': u'W', 'degrees': None, 'name': u'Vest'}, 'symbolname': u'Klarv\xe6r'}, {'from': u'2012-01-19T20:00:00', 'temperature': u'-5', 'pressure': u'998.9', 'precipitation': u'0', 'period': None, 'to': u'2012-01-19T21:00:00', 'windSpeed': {'mps': u'1.1', 'name': u'Flau vind'}, 'symbolnumber': u'3', 'windDirection': {'code': u'NW', 'degrees': None, 'name': u'Nordvest'}, 'symbolname': u'Delvis skyet'}], 'text': [{'to': u'2012-01-18', 'from': u'2012-01-17', 'description': u'\xd8stlandet og Telemark: Skiftende bris. Oppholdsv\xe6r. Fra sent onsdag formiddag s\xf8rlig bris, p\xe5 kysten frisk bris, senere liten kuling utsatte steder. Tilskyende og etter hvert sn\xf8, f\xf8rst i vest. Utover kvelden vestlig bris, frisk bris utsatte steder. Oppklarning.', 'title': u'tirsdag og onsdag'}, {'to': u'2012-01-19', 'from': u'2012-01-19', 'description': u'\xd8stlandet og Telemark: Skiftende bris. Opphold og gl\xf8tt av sol.', 'title': u'torsdag'}, {'to': u'2012-01-20', 'from': u'2012-01-20', 'description': u'Telemark, \xd8stlandet og Fjellet i S\xf8r-Norge: Bris mellom vest og nord. Lettskyet, for det meste pent v\xe6r, men i grensestr\xf8kene mot Sverige noe mer skyer og kan hende litt spredt sn\xf8. Kaldere.', 'title': u'fredag'}, {'to': u'2012-01-22', 'from': u'2012-01-21', 'description': u'S\xf8r-Norge s\xf8r for Stad og Dovre: Skiftende vindforhold, p\xe5 Vestlandet periodevis s\xf8r\xf8stlig kuling, og p\xe5 Skagerrakkysten av og til nord\xf8stlig kuling. Perioder med sn\xf8 og sn\xf8byger og gjennomg\xe5ende lave temperaturer.', 'title': u'l\xf8rdag og s\xf8ndag'}, {'to': u'2012-01-26', 'from': u'2012-01-23', 'description': u'Norge og Spitsbergen: Denne uken er utsiktene noe usikre, men mest et sannsynlig vil svake lavtrykk passere i en s\xf8rlig bane fra Nordsj\xf8en mot \xd8stersj\xf8en. \n     S\xf8r for Stad og Dovre ventes vind fra nord eller \xf8st, av og til opp i kuling. Perioder med sn\xf8, av og til regn p\xe5 kysten lengst i s\xf8r. Ogs\xe5 dager med opphold og sol. Nord for Stad og Dovre fortsatt fralandsvind, periodevis kuling, og ellers lange perioder med pent v\xe6r. Fortsatt lave temperaturer.\n     P\xe5 Spitsbergen ventes overveiende nord\xf8stlig bris, stort sett oppholdsv\xe6r og sm\xe5 endringer i temperaturforholdene.', 'title': u'mandag til torsdag'}], 'sunset': u'2012-01-17T15:52:24', 'location': u'0458 Oslo', 'sunrise': u'2012-01-17T09:01:54'}

  ''' Goal~
  'C
   4
   3
   2           ****-----___
   1     ###--/            _______
   0 -###
  -1
     ^| ^| ^/ ^/ ^/ -> -> \v |v  O  Wind direction
     10 11 12 13 14 15 16 17 18 19  Time
  '''


  ret = "Meteogram for " + location + " for the next 24 hours\n"
  graph=dict()
  graph[0] = " 'C"
  graph[10] = "  " #wind
  graph[11] = "  " #time
  temphigh=0
  templow=0
  hourcount=10

  #TODO: Symbols that display wind direction in two characters
  wind={
    "N":"I^", "NNE":"/^", "NE":"/A", "ENE":"/^", \
    "E":"->", "ESE":"\\v", "SE":"\V", "SSE":"\\v", \
    "S":"Iv", "SSW":"/v", "SW":"/V", "WSW":"/v", \
    "W":"<-", "WNW":"\^", "NW":"\A", "NNW":"\^"}

  #collect temps
  for item in weatherdata['tabular'][:hourcount]:
  #  print item['temperature'], item['from']
    if int(item['temperature']) >= temphigh:
      temphigh = item['temperature']

    if int(item['temperature']) <= templow:
      templow = item['temperature']

  #print "high",temphigh
  #print "low",templow

  #create temp range
  temps=[]
  for t in range(int(temphigh)+2, int(templow)-2, -1):
    temps.append(t)

  #print "temps",temps
  for i in range(1, hourcount):
    try:
      graph[i] = str(temps[i]).rjust(3, ' ')
    except KeyError as (errno, strerror):
      print "err ",i,errno,strerror
      pass
    except IndexError: #list empty
      pass
  #print "graph",graph

  time=[]
  #create graph
  for item in weatherdata['tabular'][:hourcount]:
    #create wind on y axis
    graph[10] += " " + wind[ item['windDirection']['code'] ]
    #create time on y axis
    graph[11] += " " + str(item['from'])[11:13] #2012-01-17T21:00
    #create time range
    time.append(str(item['from'])[11:13])

    #for each y look for matching temp
    for i in range(1, hourcount):
      try:
        if item['temperature'].strip() == graph[i][:3].strip():
	  #print "==", item['temperature'].strip(), " ", graph[i][:3].strip()
	  graph[i] += "--"
        else:
	  #print "!=", item['temperature'].strip(), " ", graph[i][:3].strip()
	  graph[i] += "  "
      except KeyError:
        pass

  #  print item
  #  break
    continue

  #print graph
  for g in graph.values():
    print g #+ "\n"



'''

crap data for later testing:

  # Format precipitation if there are any
  if item['precipitation'] != '0.0':
    precipitation = '%s mm nedbor,' % (item['precipitation'])
  else:
    precipitation = ''
  # Format windSpeed if it is higher than 5
  if item['windSpeed']['mps'] != '.' or int(item['windSpeed']['mps']) > 5:
    windSpeed = '%s (%s mps) %s' % (item['windSpeed']['name'], item['windSpeed']['mps'], item['windDirection']['code'])
  else:
    windSpeed = ''

  ret += item['from'][12]
  ret += item['symbolnumber']
#  ret += weathergfx.get_wind(item['windDirection']['code'])
  ret += "%s\n" % (weatherdata['location'])
  ret += item['symbolname'] + ", "
  ret += precipitation + " " + windSpeed.lower() + "\n\n"

print ret
'''

if __name__ == "__main__":
  # Test if location is provided
  if sys.argv[1] == []:
    location = "0458"
  else:
    location = sys.argv[1]
  # Run simple print function
  sys.exit(pyyrascii(location))

