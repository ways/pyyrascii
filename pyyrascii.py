#!/usr/bin/env python
# -*- coding: UTF-8; -*-

"""
PyYrAscii
-------

PyYrAscii is a simple python grapher for using Yr.no’s weather data API.

You are welcome to participate in this project!
"""

__version__ = '0.2'
__url__ = 'https://github.com/ways/pyyrascii'
__license__ = 'GPL License'
__docformat__ = 'markdown'

import SocketServer, subprocess, re, sys
import pyyrlib


def get_pyyrascii (location):
  weatherdata = pyyrlib.returnWeatherData(location, True)

  if not weatherdata:
    return "Error; no weather data for selected location."

  ''' Goal~
  'C
   4
   3
   2           ****-----___
   1     ###--/            _______
   0 -###
  -1
         _  -  =  #  _ _- -= =# ##  Rain ( _-=#)
     NW  N NE  E SE  S SW  W  N  O  Wind direction
     10 11 12 13 14 15 16 17 18 19  Time

     ^\ ^| ^/ -> v\ v| v/ <- ^|  O  Wind direction

     ^   ^  ^     \  |  /     ^     Wind direction
      \  |  / ->  v  v  v <-  \  O  Wind direction

     35 00 02 04 07 18 20 28 30  -  Wind angle (/10)
      1  2  2  3  2  2  1  1  1  0  Wind strength

      0  2  1  1  0  5  0  0  0  0  Rain (mm)
     00 12 01 01 00 39 99  0  0  0  Rain (mm low, high)

Ledgend:
 ---                   ===                              ###
 L Sunny, or scattered L Partly clouded, clouded or fog L Rain, snow, storm
  '''

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
  temphigh=-20
  templow=20
  hourcount=22
  ret += "            Meteogram for " + location + " for the next " + \
    str(hourcount) + " hours.\n"
  #graph[0] += "     Meteogram for " + location + " for the next " + \
  #  str(hourcount) + " hours."

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
    graph[windline] += " " + wind[ item['windDirection']['code'] ]
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

  #Ledgends
  graph[rainline] += " Rain (mm)"
  graph[windline] += " Wind dir."
  graph[timeline] += " Hour"

  #print graph
  for g in graph.values():
    ret += g + "\n"

  ret += '''\nLedgend:   --- : Sunny   === : Clouded   ### : Rain/snow

Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK.'''

  return ret

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

  print get_pyyrascii(location)
  sys.exit(0)

