#!/bin/sh
i=22810
n=5
while [ $i -ge 20000 ]
  do
    echo "python3 ./crawler.py -d Gossiping $i 5 > ./log/$i.log 2>&1 &"
    python3 ./crawler.py -d Gossiping $i $n > ./log/$i.log 2>&1 &
    i=`expr $i - $n`
  done
