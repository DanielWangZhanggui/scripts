#!/bin/bash
YYYY=`date +%Y`
MM=`date +%m`
DD=`date +%d`
export DIR="y=${YYYY}\/m=${MM}\/d=${DD}"
sed "s/DATE_TO_BE_CHNAGED/$DIR/g" logstash.conf.tpl > logstash.conf
