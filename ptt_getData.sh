#!/bin/sh
i=10000
n=500
while [ $i -ge 1 ]
  do
    echo "python3 ./crawler.py -d Gossiping ${i} ${n} > ./log/${i}_${n}.log 2>&1 &"
    python3 ./crawler.py -d Gossiping ${i} ${n} > ./log/${i}_${n}.log 2>&1 &
    i=`expr $i - $n`
  done
