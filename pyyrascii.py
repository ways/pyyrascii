#!/usr/bin/env python
# -*- coding: UTF-8; -*-

"""
PyYrAscii
-------

PyYrAscii is a simple python grapher for using Yr.no’s weather data API.

You are welcome to participate in this project!
"""

__version__ = '20120310'
__url__ = 'https://github.com/ways/pyyrascii'
__license__ = 'GPL License'

import SocketServer, subprocess, re, sys, string, math
import pyyrlib # https://github.com/ways/pyyrlib
import pyofc # https://github.com/ways/pyofflinefilecache

def wind_symbols():
  return {
    "N":" N", "NNE":"NE", "NE":"NE", "ENE":"NE", \
    "E":" E", "ESE":"SE", "SE":"SE", "SSE":"SE", \
    "S":" S", "SSW":"SW", "SW":"SW", "WSW":"SW", \
    "W":" W", "WNW":"NW", "NW":"NW", "NNW":"NW"}


def get_pyyrascii (location):
  weatherdata, source = pyyrlib.returnWeatherData(location, True)

  if not weatherdata:
    return False, False

  verbose = False
  #verbose = True
  ret = "" #all output goes here
  graph=dict()
  tempheight = 10+1
  timeline = 13
  windline = 15
  windstrline = 16
  rainline = 17
  graph[timeline] = "   " #time
  graph[timeline+1] = " " #spacer
  graph[rainline] = "   " #rain
  graph[windline] = "   " #wind
  graph[windstrline] = "   " #wind strenght
  temphigh = -99
  templow = 99
  tempstep = -1
  hourcount = 22
  screenwidth = 80
  #rain in graph:
  rainheight = 10
  rainstep = -1
  rainhigh = 0
  wind = wind_symbols()

  #collect temps, rain from xml
  for item in weatherdata['tabular'][:hourcount]:
    if int(item['temperature']) > temphigh:
      temphigh = int(item['temperature'])
      #print "h" + item['temperature']

    if int(item['temperature']) < templow:
      templow = int(item['temperature'])
      #print "l" + item['temperature']

    if math.ceil(float(item['precipitation'])) > rainhigh:
      rainhigh = math.ceil(float(item['precipitation']))

  if verbose:
    print "high",temphigh,"low",templow,"rainhigh",rainhigh

  #scale y-axis. default = -1
  if tempheight < (temphigh - templow):
    tempstep = -2
    if verbose:
      print "Upped timestep"

  #scale rain-axis
  #TODO

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
  for i in range(1, tempheight):
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

  #create rainaxis
  #TODO: make this scale
  rainaxis = []
  for r in range(10, 0, rainstep):
    if r <= rainhigh:
      rainaxis.append('%2.0f mm ' % r)
    else:
      rainaxis.append(' ')

  if verbose:
    print "rain axis",str(rainaxis)

  #draw graph elements:
  time=[]
  #for each x (time)
  for item in weatherdata['tabular'][:hourcount]:
    rain = math.ceil(float(item['precipitation']))
    #create rain on x axis
    graph[rainline] += " " + '%2.0f' % rain
    #create wind on x axis
    graph[windline] += " " + \
      (wind[ item['windDirection']['code'] ] \
      if 0 != item['windSpeed']['mps'] else " O")
    #create wind strength on x axis
    graph[windstrline] += " " + '%2.0f' % float(item['windSpeed']['mps'])
    #create time on x axis
    graph[timeline] += " " + str(item['from'])[11:13] #2012-01-17T21:00
    #create time range
    time.append(str(item['from'])[11:13])

    #for each y (temp) look for matching temp, draw graph
    for i in range(1, tempheight):
      #draw temp
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
          if int(item['symbolnumber']) in [3,4]: #parly
            graph[i] += "~~~"
          elif int(item['symbolnumber']) in [5,7,8,9,10,12,13]: #clouded
            graph[i] += "==="
          elif int(item['symbolnumber']) in [6,11,14]: #lightning
            graph[i] += "=/="
          elif int(item['symbolnumber']) == 15: #fog
            graph[i] += "###"
          else: #clear 1,2
            graph[i] += "---"
        else:
          graph[i] += "   "
      except KeyError as err:
        continue

      #compare rain, and print
      #TODO: scaling
      if (rain != 0) and (rain > 10-i):
        if int(item['symbolnumber']) in [5,6,9,10,11,14]:
          rainsymbol = "  |"
        elif int(item['symbolnumber']) in [7,12]:
          rainsymbol = "  ¤"
        elif int(item['symbolnumber']) in [8,13]:
          rainsymbol = "  *"
        graph[i] = graph[i][:-3] + rainsymbol
        #print "Rain " + str(math.trunc(rain)) + " " + str(10-i)

  #  print item
  #  break

  #Legends
  graph[0] = " 'C" + string.rjust('Rain (mm) ', screenwidth-3)
  graph[rainline] +=   " Rain (mm)"
  graph[windline] +=    " Wind dir."
  graph[windstrline] += " Wind(mps)"
  graph[timeline] +=    " Hour"

  #header
  headline = "-= Meteogram for " +\
    str(source)\
    .replace('http://www.yr.no/sted/', '')\
    .replace('http://www.yr.no/place/', '')\
    .replace('/forecast.xml','')\
    .replace('/forecast_hour_by_hour.xml','')
  if location.isdigit():
    headline += " for the next " + str(hourcount) + " hours"
  headline += " =-"
  ret += string.center(headline, screenwidth) + "\n"

  #add rain to graph
  for i in range(1, tempheight):
    try:
      graph[i] += rainaxis[i-1]
    except IndexError:
      pass

  #print graph
  for g in graph.values():
    ret += g + "\n"

  ret += '\nLegend left axis:  - Sunny  ~ Scattered  = Clouded  =/= Lightning  # Fog' +\
         '\nLegend right axis: | Rain   ¤ Sleet      * Snow \n' +\
    'Weather forecast from yr.no, delivered by the Norwegian Meteorological ' +\
    'Institute and the NRK.\n'

  return ret, source


if __name__ == "__main__":
  # Test if location is provided
  if sys.argv[1] == []:
    location = "0458"
  else:
    location = ''.join(sys.argv[1:])

  ret, source = get_pyyrascii(location)
  print ret
  sys.exit(0)
