#!/usr/bin/env python
# -*- coding: utf-8 -*-
#depends: python-pymetar

import sys, string, pymetar, os, time, getopt


def drawWeather(type):
  if 'scattered clouds' == type.lower() or 'few clouds' == type.lower():
    print '''
    _        _
   ( )_     ( )_
  (____)   (____)
          '''
  elif 'clear sky' == type.lower():
    print '''

    '''

  elif 'Clouds' == type:
    print '''
     __
   _(  )_
  (______\ 
          '''
  elif 'Light rain' == type:
    print '''
     __
   _(  )_
  (______\ 
    ` ` ` '''
  elif type.lower().startswith("showers"):
    print '''
    _
   ( )_
  (____) 
    ` `  '''
  elif type.lower().find("fog"):
    print '''
  - - -
  - - -
  - - -  '''
  elif 'Sunny' == type:
    print '''
   
  ` _ 
  -(_)-
  ,   `
      '''
  else:
    print "can't draw unknown weather " + type


def drawStation(pr):
  print '''  |>
 _|_____    Station: ''' + pr.getStationName() + '''
 | # # |    Position: %s
 |_____|    Time: %s''' % (pr.getStationPosition(), pr.getTime())


def getWeather(station):
  rf=pymetar.ReportFetcher(station)
  rep=rf.FetchReport()
  rp=pymetar.ReportParser()
  return rp.ParseReport(rep)


def printStation(station, pr):
  print "Station: %s\nTime: %s\nPosition: %s" % (pr.getStationName(), pr.getTime(), pr.getStationPosition())


def printWeather(station, pr, simple = False):
  if simple:
    print 'Station: ' + pr.getStationName()
    print 'Time: %s' % pr.getTime()

  print "Weather: %s" % pr.getWeather()
  print "Temperature: %s, Dew point: %s" % (pr.getTemperatureCelsius(), pr.getDewPointCelsius())
  if not simple:
    print "Wind direction: %s, Speed: %s" % (pr.getWindDirection(), pr.getWindSpeed())
    print "Pressure: %s, Humidity: %s" % (pr.getPressure(), pr.getHumidity())
    print "Visibility: %s, Sky: %s" % (pr.getVisibilityKilometers(), pr.getSkyConditions())


def clearScreen():
  if os.name == "posix":
    # Unix/Linux/MacOS/BSD/etc
    os.system('clear')
  elif os.name in ("nt", "dos", "ce"):
    # DOS/Windows
    os.system('CLS')


def showWeather(station, pr, simple = False):
  if not simple:
    clearScreen()
    drawStation(pr)
    drawWeather(pr.getWeather())
  printWeather(station, pr, simple)


def usage():
  print '''Usage: weather.py -l <station code>
Look up your station code at http://www.nws.noaa.gov/tg/siteloc.shtml '''

def main(argv):
  station='ENGM' # http://www.nws.noaa.gov/tg/siteloc.shtml
  refresh = False
  simple = False

  try:
    opts, args = getopt.getopt(argv, "hlsr:", ["help"])
  except getopt.GetoptError:
    #using default
    print ''
    #usage()
    #sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()                     
      sys.exit()
    elif opt in ("-l"):
      station = arg
    elif opt in ("-s"):
      simple = True
    elif opt in ("-r"):
      refresh = arg

  pr = current_pr = False
  while True:
    current_pr = pr

    pr=getWeather(station)
 
    if False == current_pr:
      showWeather(station, pr, simple)
    elif pr.getTime() != current_pr.getTime():
      showWeather(station, pr)

    if refresh > 0:
      time.sleep(900)
    else:
      break

if __name__ == '__main__':
  main(sys.argv[1:])
