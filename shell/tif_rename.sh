#!/usr/bin/env bash

for i in *.tif; do
  temp1=${i//\%/} # cut out "%" characters
  temp1=${temp1//\#/} # cut out "#" characters
  temp2=${temp1:(-7)}
  mv $i $temp2
done
