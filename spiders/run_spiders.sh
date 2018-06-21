#!/usr/bin/env bash

# -P flag indicates how many to run at once
# Should be equal to amount of cores on system
cores=$(getconf _NPROCESSORS_ONLN)
find . -maxdepth 1 -type f -print0 | xargs -0 -n 1 -P $cores scrapy runspider
# for f in *.py; do
   # scrapy runspider $f &
 # done