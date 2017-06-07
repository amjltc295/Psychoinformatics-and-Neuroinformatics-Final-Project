#!/bin/sh
i=22810
while [ $i -ge 1 ]
  do
    echo "python3 ./crawler.py -d Gossiping $i 5 > ./log/$i.log 2>&1 &"
    python3 ./crawler.py -d Gossiping $i 5 > ./log/$i.log 2>&1 &
    i=`expr $i - 10`
  done
