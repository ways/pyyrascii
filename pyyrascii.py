#!/usr/bin/env python
# -*- coding: UTF-8; -*-

"""
PyYrAscii
-------

PyYrAscii is a simple python grapher for using Yr.no’s weather data API.

You are welcome to participate in this project!
"""

__version__ = '0.3'
__url__ = 'https://github.com/ways/pyyrascii'
__license__ = 'GPL License'
__docformat__ = 'markdown'

import SocketServer, subprocess, re, sys, string
import pyyrlib # https://github.com/ways/pyyrlib
import pyofc # https://github.com/ways/pyofflinefilecache

def get_pyyrascii (location):
  weatherdata, source = pyyrlib.returnWeatherData(location, True)

  if not weatherdata:
    return "Error; no weather data for selected location " + location + ".\n" +\
      "Attempt a norwegian post code (4 digits), an international city or " +\
      "empty. International names comes from " +\
      "http://fil.nrk.no/yr/viktigestader/verda.txt" + ".\n"


  ret = "" #all output goes here
  graph=dict()
  graph[0] = " 'C"
  tempheight = 11
  rainline = 13
  windline = 14
  timeline = 15
  graph[rainline] = "   " #rain
  graph[windline] = "   " #wind
  graph[timeline] = "   " #time
  temphigh=-99
  templow=99
  hourcount=22

  headline = "Meteogram for " + location
  if location.isdigit():
    headline += " for the next " + str(hourcount) + " hours."
  ret += string.center(headline, 80) + "\n"

  wind={
    "N":" N", "NNE":"NE", "NE":"NE", "ENE":"NE", \
    "E":" E", "ESE":"SE", "SE":"SE", "SSE":"SE", \
    "S":" S", "SSW":"SW", "SW":"SW", "WSW":"SW", \
    "W":" W", "WNW":"NW", "NW":"NW", "NNW":"NW"}

  #collect temps
  for item in weatherdata['tabular'][:hourcount]:
    if int(item['temperature']) > temphigh:
      temphigh = int(item['temperature'])
      #print "h" + item['temperature']

    if int(item['temperature']) < templow:
      templow = int(item['temperature'])
      #print "l" + item['temperature']

  #create temp range
  #print "high",temphigh
  #print "low",templow
  if temphigh == templow:
    templow = temphigh-1

  temps=[]
  for t in range(int(temphigh), int(templow), -1):
    temps.append(t)

  #extend temp range
  #print "temps",temps
  #temps = [ (temps[0] +1) ] + temps
  for t in range(0, tempheight):
    if len(temps)+1 < tempheight:
      if t%2 == 0:
        temps.append( temps[len(temps)-1] -1 )
      else:
        temps = [ (temps[0] +1) ] + temps

  for i in range(1, tempheight):
    try:
      graph[i] = str(temps[i-1]).rjust(3, ' ')
    except KeyError as (errno, strerror):
      print "err ",i,errno,strerror
      pass
    except IndexError: #list empty
      pass
  #print "graph",graph

  time=[]
  #create graph
  for item in weatherdata['tabular'][:hourcount]:
    #create rain on y axis
    graph[rainline] += " " + '%2.0f' % float(item['precipitation'])
    #create wind on y axis
    graph[windline] += " " + \
      (wind[ item['windDirection']['code'] ] \
      if 0 != item['windSpeed']['mps'] else " O")
    #create time on y axis
    graph[timeline] += " " + str(item['from'])[11:13] #2012-01-17T21:00
    #create time range
    time.append(str(item['from'])[11:13])

    #for each y look for matching temp
    for i in range(1, hourcount):
      if tempheight < i:
        continue

      try:
        if item['temperature'].strip() == graph[i][:3].strip():
          if int(item['symbolnumber']) in [3,4,15]:
            graph[i] += "==="
          elif int(item['symbolnumber']) in [5,6,7,8,9,10,11,12,13,14]:
            graph[i] += "###"
          else:
            graph[i] += "---"
        else:
          graph[i] += "   "
      except KeyError:
        pass

  #  print item
  #  break

  #Legends
  graph[rainline] += " Rain (mm)"
  graph[windline] += " Wind dir."
  graph[timeline] += " Hour"

  #print graph
  for g in graph.values():
    ret += g + "\n"

  ret += '\nLegend:   --- : Sunny   === : Clouded   ### : Rain/snow \n' +\
    'Weather forecast from yr.no, delivered by the Norwegian Meteorological ' +\
    'Institute and the NRK.\n' +\
    'Source: ' + \
    str(source)\
      .replace('http://www.yr.no/sted/', '')\
      .replace('http://www.yr.no/place/', '')\
      .replace('/forecast.xml','')\
      .replace('/forecast_hour_by_hour.xml','') + \
    "\n"

  return ret


if __name__ == "__main__":
  # Test if location is provided
  if sys.argv[1] == []:
    location = "0458"
  else:
    location = ''.join(sys.argv[1:])

  print get_pyyrascii(location)
  sys.exit(0)
