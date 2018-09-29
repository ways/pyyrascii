#!/usr/bin/env python
# -*- coding: UTF-8; -*-

# http://om.yr.no/forklaring/symbol/

def get_wind (direction = ""):
  arr = dict()
  arr["N"] = '''
  ^  
 /|\ 
  |  
  |  

  '''
  arr["S"] = '''
  |  
  | 
 \|/ 
  v  

  '''
  arr["W"] = '''
 
   
<--- 
   

  '''

  try:
    return arr[direction]
  except KeyError:
    return ""

def get_symbol (symbolnum = 0):
  arr = []
  #0 noop
  arr.append("0")
  #1 Sun
  arr.append ('''
  `__, 
 -/  \-
  \__/
  ,  . 

  ''')
  #2 Fair
  arr.append('''
    _ `__, 
  _( \/  \-
 (_____\_/ 
         . 

  ''')
  #3 Partly cloudy
  arr.append('''
    _ `__, 
  _(  \_ \-
 (_____ \/ 
           

  ''')
  #4 Cloudy
  arr.append('''
    _
  _( \
 (_____\


  ''')
  #5 Rain showers
  arr.append('''
    _ `__, 
  _(  \_ \-
 (______\/ 
   ` `

  ''')
  #6 Rain showers with thunder
  arr.append('''
    _
  _( \
 (_____\
  /_` `
   /
  ''')
  #7 Sleet showers
  arr.append('''
    _ `__, 
  _(  \_ \-
 (______\/ 
   * `  

  ''')
  #8 Snow showers
  arr.append('''
    _
  _( \
 (_____\
   * *  

  ''')
  #9 Rain
  arr.append('''
    _
  _( \
 (_____\
   ' '

  ''')
  #10 Heavy rain
  arr.append('''
    _
  _( \
 (_____\
  ' ' '

  ''')
  #11 Rain and thunder
  arr.append('''
    _
  _( \
 (_____\
  /_' '
   /
  ''')
  #12 Sleet
  arr.append('''
    _    
  _(  \_ 
 (______\
   * ' * 

  ''')
  #13 Snow
  arr.append('''
    _    
  _(  \_ 
 (______\
   * * * 

  ''')
  #14 Snow and thunder
  arr.append('''
    _    
  _(  \_ 
 (______\
  /_ * * 
   /     
  ''')
  #15 Fog
  arr.append('''
    _    
  _(\\\_ 
 (\\\\\\\\


  ''')

  return arr[int(symbolnum)]

