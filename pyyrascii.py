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
    return False

  verbose = False
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
  temphigh = -99
  templow = 99
  tempstep = -1
  hourcount = 22

  headline = "Meteogram for " + location
  if location.isdigit():
    headline += " for the next " + str(hourcount) + " hours."
  ret += string.center(headline, 80) + "\n"

  wind={
    "N":" N", "NNE":"NE", "NE":"NE", "ENE":"NE", \
    "E":" E", "ESE":"SE", "SE":"SE", "SSE":"SE", \
    "S":" S", "SSW":"SW", "SW":"SW", "WSW":"SW", \
    "W":" W", "WNW":"NW", "NW":"NW", "NNW":"NW"}

  #collect temps from xml, 
  for item in weatherdata['tabular'][:hourcount]:
    if int(item['temperature']) > temphigh:
      temphigh = int(item['temperature'])
      #print "h" + item['temperature']

    if int(item['temperature']) < templow:
      templow = int(item['temperature'])
      #print "l" + item['temperature']

  if verbose:
    print "high",temphigh,"low",templow

  #scale y-axis. default = -1
  if tempheight < (temphigh - templow):
    tempstep = -2
    if verbose:
      print "Upped timestep"

  if temphigh == templow:
    templow = temphigh-1

  temps=[]
  #create temp range
  for t in range(int(temphigh), int(templow)-1, tempstep):
    temps.append(t)

  if verbose:
    print "temps",temps

  #extend temp range
  #temps = [ (temps[0] +1) ] + temps
  for t in range(0, tempheight):
    if len(temps)+1 < tempheight:
      if t%2 == 0: #extend down
        temps.append( temps[len(temps)-1] - abs(tempstep) )
      else: #extend up
        temps = [ temps[0] + abs(tempstep) ] + temps
  #temps.append( temps[len(temps)-1] -1 ) #TODO:remove me?

  if verbose:
    print "temps",temps

  #write temps to graph
  for i in range(1, tempheight+abs(tempstep)):
    #print i
    try:
      graph[i] = str(temps[i-1]).rjust(3, ' ')
    except KeyError as (errno, strerror):
      print "err ",i,errno,strerror
      pass
    except IndexError as err: #list empty
      #print "err ",err
      pass

  #print "graph",graph

  time=[]

  #draw graph elements
  for item in weatherdata['tabular'][:hourcount]:
    #create rain on x axis
    graph[rainline] += " " + '%2.0f' % float(item['precipitation'])
    #create wind on x axis
    graph[windline] += " " + \
      (wind[ item['windDirection']['code'] ] \
      if 0 != item['windSpeed']['mps'] else " O")
    #create time on x axis
    graph[timeline] += " " + str(item['from'])[11:13] #2012-01-17T21:00
    #create time range
    time.append(str(item['from'])[11:13])

    #for each y look for matching temp, draw graph
    for i in range(1, hourcount):
      if tempheight < i:
        break

      try:
        #parse out numbers to be compared
        temptomatch = [ int(item['temperature']) ]
        tempingraph = int(graph[i][:3].strip())

        if tempstep < -1: #TODO: this should scale higher than one step
          temptomatch.append(temptomatch[0] - 1)

        #print "temptomatch",temptomatch
        #print "graph",tempingraph

        if tempingraph in temptomatch:
          #print temptomatch, graph[i][:3].strip()
          if int(item['symbolnumber']) in [3,4,15]: #parly
            graph[i] += "==="
          elif int(item['symbolnumber']) in [5,6,7,8,9,10,11,12,13,14]: #clouded
            graph[i] += "###"
          else: #clear
            graph[i] += "---"
        else:
          graph[i] += "   "
      except KeyError as err:
        #print err
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
