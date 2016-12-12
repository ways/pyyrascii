#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyYrAscii
-------

PyYrAscii is a simple python grapher for using Yr.no’s weather data API.

You are welcome to participate in this project!
"""

__version__ = '20161212'
__url__ = 'https://github.com/ways/pyyrascii'
__license__ = 'GPL License'

import SocketServer, subprocess, re, sys, string, math, random
import pyyrlib # https://github.com/ways/pyyrlib
import pyofc # https://github.com/ways/pyofflinefilecache

verbose = False
#verbose = True

def wind_symbols():
  return {
    "N":" N", "NNE":"NE", "NE":"NE", "ENE":"NE", \
    "E":" E", "ESE":"SE", "SE":"SE", "SSE":"SE", \
    "S":" S", "SSW":"SW", "SW":"SW", "WSW":"SW", \
    "W":" W", "WNW":"NW", "NW":"NW", "NNW":"NW"}


def get_pyyrascii (location, offset = 0, hourstep = 1, screenwidth = 80):
  weatherdata, source = pyyrlib.returnWeatherData(location, True)

  if not weatherdata:
    return False, False

  if verbose:
    print "offset",offset
    print "hourstep",hourstep

  offset = int(offset)
  hourstep = int(hourstep)
  screenwidth = int(screenwidth)

  ret = "" #all output goes here
  graph=dict()
  tempheight = 10+1
  timeline = 13
  windline = 15
  windstrline = 16
  rainline = 17
  graph[timeline] = "   " #time
  graph[timeline+1] = " " #spacer
  graph[windline] = "   " #wind
  graph[windstrline] = "   " #wind strenght
  temphigh = -99
  templow = 99
  tempstep = -1
  hourcount = (screenwidth-14)/3 + offset

  #rain in graph:
  rainheight = 10
  rainstep = -1
  rainhigh = 0 #highest rain on graph
  wind = wind_symbols()
  sunrise = None
  sunset = None

  if verbose:
    print "hourcount", hourcount

  #collect temps, rain from xml
  for item in weatherdata['tabular'][offset:hourcount]:
    if int(item['temperature']) > temphigh:
      temphigh = int(item['temperature'])

    if int(item['temperature']) < templow:
      templow = int(item['temperature'])

    if math.ceil(float(item['precipitation'])) > rainhigh:
      rainhigh = math.ceil(float(item['precipitation']))

    rainhighmax = 0
    try:
      rainhighmax = math.ceil(float(item['precipitationmax']))
    except KeyError:
        pass
    if rainhighmax > rainhigh:
      rainhigh = rainhighmax

  if verbose:
    print "high",temphigh,"low",templow,"rainhigh",rainhigh

  #scale y-axis. default = -1
  if tempheight <= (temphigh - templow):
    tempstep = -2
    if verbose:
      print "Upped tempstep"

  #sunrise
  if weatherdata['sunrise']:
    sunrise = str(weatherdata['sunrise'])[11:13] #2014-11-21T08:28:42
  if weatherdata['sunset']:
    sunset = str(weatherdata['sunset'])[11:13] #2014-11-21T08:28:42
    if verbose:
      print 'sunrise' + sunrise + 'sunset' + sunset

  if temphigh == templow:
    templow = temphigh-1

  temps=[]
  #create temp range
  for t in range(int(temphigh), int(templow)-1, tempstep):
    temps.append(t)

  if verbose:
    print "temps",temps

  #extend temp range
  for t in range(0, tempheight):
    if len(temps)+1 < tempheight:
      if t%2 == 0: #extend down
        temps.append( temps[len(temps)-1] - abs(tempstep) )
      else: #extend up
        temps = [ temps[0] + abs(tempstep) ] + temps

  if verbose:
    print "temps",temps

  #write temps to graph
  for i in range(1, tempheight):
    try:
      graph[i] = str(temps[i-1]).rjust(3, ' ')
    except KeyError as (errno, strerror):
      print "err ",i,errno,strerror
      pass
    except IndexError as err: #list empty
      pass

  #create rainaxis
  #TODO: make this scale
  rainaxis = []
  for r in range(rainheight, 0, rainstep):
    if r <= rainhigh: # + 1
      rainaxis.append('%2.0f mm ' % r)
    else:
      rainaxis.append(' ')

  if verbose:
    print "rain axis",str(rainaxis)

  #draw graph elements:
  time=[]
  for item in weatherdata['tabular'][offset:hourcount:hourstep]:
    rain = math.ceil(float(item['precipitation']))
    rainmax = 0 #max rain for this hour
    try:
      if verbose:
        print "prec", rain
      rainmax = math.ceil(float(item['precipitationmax']))
      if verbose:
        print "precmax", rainmax
    except KeyError:
      pass

    #create wind on x axis
    graph[windline] += " " + \
      (wind[ item['windDirection']['code'] ] \
      if 0.0 != float(item['windSpeed']['mps']) else " O")

    #create wind strength on x axis
    graph[windstrline] += " " + '%2.0f' % float(item['windSpeed']['mps'])

    #create time on x axis
    spacer=' '
    hour=str(item['from'])[11:13] #2012-01-17T21:00
    if sunrise and sunset and \
      int(sunrise) < int(hour) and \
      int(sunset) > int(hour):
      spacer='_'
    graph[timeline] += spacer + hour

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

        if tempingraph in temptomatch:
          if int(item['symbolnumber']) in [3,4]: #partly
            graph[i] += "^^^"
          elif int(item['symbolnumber']) in [5,7,8,9,10,12,13]: #clouded
            graph[i] += "==="
          elif int(item['symbolnumber']) in [6,11,14,20,21,22,23]: #lightning
            graph[i] += "=V="
          elif int(item['symbolnumber']) == 15: #fog
            graph[i] += "###"
          elif int(item['symbolnumber']) == 2: #light clouds
            graph[i] += "=--"
          elif int(item['symbolnumber']) in [1]: #clear
            graph[i] += "---"
          else: #Shouldn't hit this
            graph[i] += "???"
        else:
          graph[i] += "   "
      except KeyError as err:
        continue

      #compare rain, and print
      #TODO: scaling
      if (rain != 0) and (rain > 10-i):
        if int(item['symbolnumber']) in [7,12]: #sleet
          rainsymbol = "!"
        elif int(item['symbolnumber']) in [8,13]: #snow
          rainsymbol = "*"
        else: #if int(item['symbolnumber']) in [5,6,9,10,11,14]: #rain
          rainsymbol = "|"

        if 0 > int(item['temperature']): #rain but cold
          rainsymbol = "*"

        if verbose:
          print "rainmax: ", rainmax,"i",i,"rain",rain
        #if overflow, print number at top
        if rain > 10 and i == 1:
          rainsymbol = '%2.0f' % rain
          graph[i] = graph[i][:-2] + rainsymbol
        else:
          #print rainmax if larger than rain.
          if rainmax > rain:
            try:
              graph[i-1] = graph[i-1][:-1] + "'"
            except UnboundLocalError:
              print "Err2: " + str(item['symbolnumber'])
            except KeyError:
              pass
          
          #print rain
          try:
            graph[i] = graph[i][:-1] + rainsymbol
          except UnboundLocalError:
            print "Err: " + str(item['symbolnumber'])

  #Legends
  graph[0] = " 'C" + string.rjust('Rain (mm) ', screenwidth-3)
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

  #legend
  ret += "\nLegend left axis:   - Sunny   ^ Scattered   = Clouded   =V= Thunder   # Fog" +\
         "\nLegend right axis:  | Rain    ! Sleet       * Snow\n"

  appendix = list()
  appendix.append('[Weather forecast from yr.no, delivered by the Norwegian Meteorological ' +\
    'Institute and the NRK.]')
  appendix.append('[Try finger @graph.no for more info.]')
  appendix.append('[Mail a "thank you" to finger@falkp.no if you like the service.]')
  #appendix.append('[Version ' + __version__ + ']')
  appendix.append('[Project home: ' + __url__ + ']')
  #appendix.append('[Hi mom!]')
  #appendix.append('[Your ad here? (Forget it!)]')
  appendix.append('[Blog at http://0p.no]')
  #appendix.append('[Finger not available? Use echo oslo|nc graph.no finger]')
  #appendix.append('[Thumbs up for open data.]')
  #appendix.append('[Served to you by GNU/Linux.]')
  #appendix.append('[Want to help? This service sucks for non-norwegian forecast.]')
  appendix.append("[You can not use US zip codes here. Try finger @graph.no.]")
  appendix.append('[The _ in front of hours means the sun is up.]')
  #appendix.append('[This service now has a client, check out the github repo.]')
  #appendix.append('[Ask me again, I dare you!]')
  appendix.append('[Data is cached for 20 minutes, please dont hammer.]')
  #appendix.append('[Sorry for the instability. Daily requests recently went up tenfold.]')
  #appendix.append('[Data is cached for 20 minutes. No use in asking every second...]')
  #appendix.append('[My bitcoin, flatter, patreon IDs are... Nah, keep your money.]')
  #appendix.append('[Peace, love, linux.]')
  #appendix.append('[Rate limited to survive twitter storm. Max 3 connections pr. 30 seconds.]')
  appendix.append('[Pipe finger to head -n19 to remove this message.]')
  appendix.append('[Hosted by copyleft.no]')
  #appendix.append('[Source data has changed. Sunrise info missing for now.]')

  # Add a random appendix
  ret += appendix [ random.randint( 0, len(appendix)-1 ) ]

  return ret, source


def get_pyyrshort (location, offset = 0, hourstep = 1, screenwidth = 80):
  weatherdata, source = pyyrlib.returnWeatherData(location, True)

  if not weatherdata:
    return False, False

  offset = int(offset)

  ret = "" #all output goes here

  if verbose:
    print "weather"
    print weatherdata['tabular'][offset]
    print weatherdata['tabular'][offset]['temperature']
    print weatherdata['tabular'][offset]['precipitation']
    print weatherdata['tabular'][offset]['windSpeed']['mps']
    print weatherdata['tabular'][offset]['windDirection']['code']

  ret += '%(location)s at %(from)s: %(temp)s C' % \
    {"location": location, 
    "from": weatherdata['tabular'][offset]['from'][11:16],
    "temp": str(weatherdata['tabular'][offset]['temperature'])
    }

  if 0 < float(weatherdata['tabular'][offset]['precipitation']):
    precipitation = "rain"
    if 0 > float (weatherdata['tabular'][offset]['temperature']):
      precipitation = "snow"
    ret += ', %(precipitation)s mm %(name)s' % \
      {"precipitation": str(math.ceil(float(weatherdata['tabular'][offset]['precipitation']))),
      "name": precipitation}

  if 0 < float(weatherdata['tabular'][offset]['windSpeed']['mps']):
    ret += ', %(speed)s mps wind from %(direction)s' % \
      {"speed": str(weatherdata['tabular'][offset]['windSpeed']['mps']),
      "direction": weatherdata['tabular'][offset]['windDirection']['code']}

  ret += "."

  return ret, source


if __name__ == "__main__":
  # Test if location is provided
  if sys.argv[1] == []:
    location = "0458"
  else:
    location = ''.join(sys.argv[1:])

  ret, source = get_pyyrascii(location)
  print ret

  ret, source = get_pyyrshort(location)
  print ret
  sys.exit(0)
