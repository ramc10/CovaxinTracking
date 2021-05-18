#!/bin/bash

dir=/home/covid/COVID

tail -n+2 $dir/output.csv > $dir/output_temp.csv
cat $dir/output_temp.csv >> $dir/history.csv

rm $dir/output_temp.csv
