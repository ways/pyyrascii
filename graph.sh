#!/bin/bash

txtblk='\e[0;30m' # Black - Regular
txtred='\e[0;31m' # Red
txtgrn='\e[0;32m' # Green
txtylw='\e[0;33m' # Yellow
txtblu='\e[0;34m' # Blue
txtpur='\e[0;35m' # Purple
txtcyn='\e[0;36m' # Cyan
txtwht='\e[0;37m' # White
bldblk='\e[1;30m' # Black - Bold
bldred='\e[1;31m' # Red
bldgrn='\e[1;32m' # Green
bldylw='\e[1;33m' # Yellow
bldblu='\e[1;34m' # Blue
bldpur='\e[1;35m' # Purple
bldcyn='\e[1;36m' # Cyan
bldwht='\e[1;37m' # White
unkblk='\e[4;30m' # Black - Underline
undred='\e[4;31m' # Red
undgrn='\e[4;32m' # Green
undylw='\e[4;33m' # Yellow
undblu='\e[4;34m' # Blue
undpur='\e[4;35m' # Purple
undcyn='\e[4;36m' # Cyan
undwht='\e[4;37m' # White
bakblk='\e[40m'   # Black - Background
bakred='\e[41m'   # Red
bakgrn='\e[42m'   # Green
bakylw='\e[43m'   # Yellow
bakblu='\e[44m'   # Blue
bakpur='\e[45m'   # Purple
bakcyn='\e[46m'   # Cyan
bakwht='\e[47m'   # White
txtrst='\e[0m'    # Text Reset

txtgry='\e[90m'

#Local settings
foreground=${txtwht}
refresh=$(( 60*60 ))
location="oslo~80"

[ "" != "$1" ] && \
  location=$1


while :; do

  echo -e "${txtwht}"* $( date)" Loading ..."; 
  cache=$( echo "${location}"|nc graph.no finger )
  clear;
  echo -e "${txtgry}"Updated at $( date); 

  # Show pure version
  #echo -e "${txtgrn}${cache}${txtrst}"

  # Symbols and titles
  cache=$( echo "$cache" | sed "s/'C/\\${txtgry}℃ \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/Hour/\\${txtgry}  ⌚\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/Wind(mps)/\\${txtgry} ㎧\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/Wind dir./\\${txtgry}\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ mm/\\${txtgry} ㎜\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/Rain (mm)/\\${txtgry}Rain (㎜)\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/- Sun/\\${txtylw}☀\\${foreground} Sun/g" )

  # Weather
  cache=$( echo "$cache" | sed "s/=V=/\\${txtylw} ⚡⚡\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/=V/\\${txtylw} ⚡\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\=--/\\${txtblu}☁\\${txtylw}☀\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/---/\\${txtylw} ☀ \\${foreground}/g" )
  #cache=$( echo "$cache" | sed "s/--/\\${txtylw} ☀\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\^^^/\\${txtblu} ☁ \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\^^/\\${txtblu} ☁\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\ ^/\\${txtblu} ☁\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\ = /\\${txtblu}☁☁ \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\===/\\${txtblu}☁☁☁\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/\==/\\${txtblu}☁☁\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/|/\\${txtcyn}☔\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/*/\\${txtwht}☸\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ !/\\${txtwht}☸\\${txtcyn}☔\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/#/\\${txtpur}♒\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/'/\\${txtcyn}☂\\${foreground}/g" )

  # Wind
  cache=$( echo "$cache" | sed "s/NE/\\${txtblu} ↗\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/SE/\\${txtblu} ↘\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/NW/\\${txtblu} ↖\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/SW/\\${txtblu} ↙\\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ E /\\${txtblu} → \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ N /\\${txtblu} ↑ \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ S /\\${txtblu} ↓ \\${foreground}/g" )
  cache=$( echo "$cache" | sed "s/ W /\\${txtblu} ← \\${foreground}/g" )

  # Make negative temperature blue
  cache=$( echo "$cache" | sed -E "s/-[0-9]+/\\${txtcyn}&\\${foreground}/g" )

  readarray -t cachearray <<<"${cache}"
  for line in "${cachearray[@]}"; do

    # Display night in hours
    if [ 1 -eq $( echo "${line}" | grep -c '⌚') ] ; then
      echo -n "    "
      readarray -t fields <<< ${line}
      for field in ${fields[@]}; do
        if [ 1 -eq $( echo "${field}" | grep -c '_') ] ; then
          echo -en "${field} "| sed "s/_/\\ /g "
        else
          echo -en "${txtgry}${field} ${foreground}"
        fi
      done

    # Red on extreme winds
    elif [ 1 -eq $( echo "${line}" | grep -c '㎧') ] ; then
      re='^[0-9]+$'
      echo -n "    "
      readarray -t fields <<< ${line}
      for field in ${fields[@]}; do
        if [[ ${field} =~ $re ]] && [[ 9 -lt ${field} ]] ; then
          echo -en "${txtred}$(printf "%2s" "${field}")${foreground} "
        else
          echo -en " ${field} "
        fi
      done
    else
      echo -e "${line}"
    fi
  done

  echo -e "${txtgry}Next update at "\
    $( date --date="@$(( $( date +"%s" ) + ${refresh} ))" )${txtrst}

  sleep ${refresh}; 
done
