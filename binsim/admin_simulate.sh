#!/usr/bin/env bash

n=10
delay=1

for i in $(seq 1 $n)
do
    echo "$((n-i)): simulating hard for $delay second(s).... "
    sleep $delay
done

