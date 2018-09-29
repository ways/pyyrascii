#!/usr/bin/env python
# -*- coding: UTF-8; -*-

__version__ = '0.3.20120816'
__url__ = ''
__license__ = 'GPL License'

verbose=False
#verbose=True

hostname="graph.no"

import SocketServer, subprocess, pyyrlib, signal, sys, pyyrascii, string, \
  datetime, chardet, operator, re

class FingerHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    username=self.rfile.readline(25)
    username=convert(string.strip(username))

    info = self.find_user_info(username)
    self.wfile.write(info + '\n')


  def find_user_info(self, username):
    source = ""
    ret = ""
    "Return a string containing the desired user information."

    #hammering
    #if self.client_address[0] in [ '185.52.1.1' ]:
    #if self.client_address[0].startswith("93.219."):
    #  ret += ":( Stop hammering! A few request pr 10 minutes is max. (The weather data is cached for ~20 min anyway). If you want to be unlocked, send a mail to finger@falkp.no begging for forgiveness."
    #  print str(datetime.datetime.now()) + " Client " + self.client_address[0] + " " + username + " is hammering. "
    #  return ret

    if "time" == username or "date" == username or "coffee" == username or \
          "nrk" == username or "news" == username:
      cmd=["/local/bin/pyr/cmd-screensaver.sh", username]
      process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
      output = process.communicate()
      ret += output[0]

#    elif "test" == username:
#      ret += "Unicode? \u2600"

    elif "about" == username:
      ret += """Finger server @graph.no
-------------------------
Issues, bugs, requests; mail me at finger@falk-petersen.no.
This server is in development. Expect unstabillity.
Source code at https://github.com/ways/
See also finger @graph.no
"""

    elif username.isdigit() and 4 < len(username):
      ret += "US zip codes not supported. See finger @graph.no."

    elif username.isdigit() or 2 <= len(username):
      short = False
      offset = 0
      hourstep = 1
      screenwidth = 80
      imperial = False
      if verbose:
        print "username",username

      #split string
      #re.split('(\W+)', 'o:0344+80~60')
      #['o', ':', '0344', '+', '80', '~', '60']
      fields = re.split('(\W+)', username)
      if verbose:
        print fields

      for i, f in enumerate(fields):
        if ':' == f:
          short = fields[i-1]
          fields[i-1] = ''
          fields[i] = ''
          if verbose:
            print "short:",username,"|",str(short)
        elif '^' == f: # imperial
          imperial = fields[i]
          fields[i] = ''
          if verbose:
            print "imperial:",username,"|",str(imperial)
        elif '+' == f:
          offset = fields[i+1]
          fields[i] = ''
          fields[i+1] = ''
          if verbose:
            print "offset:",username,"|",str(offset)
            print fields
        elif '%' == f:
          hourstep = fields[i+1]
          fields[i] = ''
          fields[i+1] = ''
          if verbose:
            print "hourstep:",username,"|",str(hourstep)
        elif '~' == f:
          screenwidth = fields[i+1]
          fields[i] = ''
          fields[i+1] = ''
          if verbose:
            print "screenwidth:",username,"|",str(screenwidth)

      username = ''.join(fields)

      #short text output
      if short:
        if verbose:
          print "short selected:",username
        out, source = pyyrascii.get_pyyrshort (username, offset, hourstep, screenwidth)
      else: #standard output
        out, source = pyyrascii.get_pyyrascii (username, offset, hourstep, screenwidth, imperial)

      if out and 0 < len(out):
        ret += out
      else:
        ret += usage()
          
    else: #catch-all
      ret += usage()

    #log
    print str(datetime.datetime.now()) + " Client " + self.client_address[0] + " " + username + \
    ", " + str(source)\
      .replace('http://www.yr.no/sted/', '')\
      .replace('http://www.yr.no/place/', '')\
      .replace('/forecast.xml','')\
      .replace('/forecast_hour_by_hour.xml','')

    return ret


def usage(username = ""):
  ret = ""
  if username:
    ret += "Error; no weather data for selected location " + username + ".\n\n"

  ret = "yr.no is having technical problems, or you specified an unknown location.\n\n"

  ret += "Usage:\n\n" +\
    " * finger <city name>@" + hostname + " (world weather forecast, no spaces)\n" +\
    "   Example: finger newyork@" + hostname + " \n\n" +\
    " Advanced usage:\n\n" +\
    " * finger o:<city name>@" + hostname + " (a one-line forecast)\n" +\
    "   Example: finger o:newyork@" + hostname + " \n\n" +\
    " * finger ^<city name>@" + hostname + " (Imperial units)\n" +\
    "   Example: finger ^newyork@" + hostname + " \n\n" +\
    " * finger <city name>+5@" + hostname + " (forecast from 5 hrs ahead in time (max:26))\n" +\
    "   Example: finger northpole+5@" + hostname + " \n\n" +\
    " * finger <city name>~160@" + hostname + " (set screen width)\n" +\
    "   Example: finger southpole~160@" + hostname + " \n\n" +\
    " * finger <city name>%2@" + hostname + " (forecast for every second hour [Norway])\n" +\
    "   Example: finger oslo%2@" + hostname + " \n\n" +\
    " * finger <post code>@" + hostname + " (norwegian weather forecast)\n" +\
    "   Example: finger 0458@" + hostname + " \n\n" +\
    " Other: \n\n" +\
    " * finger news@" + hostname + " (latest headlines from NRK)\n" +\
    " * finger time@" + hostname + " (server local time)\n" +\
    " * finger date@" + hostname + " (server local date)\n" +\
    " * finger about@" + hostname + """ (contact information)

International names comes from http://fil.nrk.no/yr/viktigestader/verda.txt.
"""
  return ret          


def convert(str):
  #attempt to convert string str from iso-8859-1/windows-1252
  newstr=str

  result = chardet.detect(str)
  if verbose:
    print "result"
    print result,"-",result['encoding']

  #return str.decode(result['encoding']).encode("UTF-8")
  try:
    #print "result:",str.decode('iso-8859-1').encode("UTF-8")
    newstr = str.decode('utf-8').encode("UTF-8")
  except UnicodeDecodeError as e:
    #print "Err",e,str
    newstr = str.decode('iso-8859-1').encode("UTF-8")
  #except UnicodeEncodeError as e:

  return newstr


def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  sys.exit(0)


if __name__=='__main__':
  sys.stdout = open('/var/log/fingerd.log', 'a', 1)

  server=SocketServer.TCPServer( ('', 79), FingerHandler)

  signal.signal(signal.SIGINT, signal_handler)
  server.serve_forever()
