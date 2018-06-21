#/usr/bin/env bash

# echo 'spiders'
# cd ../spiders/
# bash run_spiders.sh 

# echo 'compile'
# cd ../compilation/
# python rss_parse.py

awk 'FNR==1 && NR!=1{next;}{print}' ../data/*.csv >> compile.csv