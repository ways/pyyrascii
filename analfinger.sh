#!/bin/bash

# show daily statistics

logfile="/var/log/fingerd.log /var/log/fingerd.log-$( date +'%Y%m' )*"
today=`date +%Y-%m-%d`
ignore_hosts='178.255.144.1'
public='yes'
greptext='/bin/zgrep --text'

if [[ -n $1 ]]; then
  public=$1
fi

if [[ -n $2 ]]; then
  today=$2
fi

function total {
  echo -n 'Total hits today:'
  $greptext $today ${logfile}|grep -v $ignore_hosts|wc -l
}

function uniqusers {
  echo -n 'Unique IPs today: '
  $greptext $today ${logfile} |grep -v $ignore_hosts | cut -d ' ' -f 4| sort -bg|uniq |wc -l
}

function top_users {
  echo 'Top 10 users with hitcount: '
  $greptext $today ${logfile} |grep -v $ignore_hosts | cut -d ' ' -f 4| sort|uniq -c |sort -bgr|head
  echo "Top 10 users resolved: "
  $greptext $today ${logfile} |grep -v $ignore_hosts | cut -d ' ' -f 4| sort|uniq -c |sort -bgr|head |cut -c9-|xargs -I '{}' host '{}'
}

function top_locations {
  echo "Top 10 locations: "
  $greptext $today ${logfile} |grep -v $ignore_hosts | cut -d ' ' -f 5| sort|uniq -c |sort -bgr|head
}

function total_errors {
#doesn't give anything useful
  echo -n "Total errors: "
  $greptext $today ${logfile} |grep -i "false" -c
}

#go
echo "Date: "$today
total

if [ "no" = "$public" ]; then
  uniqusers;
  top_users;
fi
top_locations
