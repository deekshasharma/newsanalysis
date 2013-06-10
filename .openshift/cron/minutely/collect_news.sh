#!/bin/bash

if [ `date +%H:%M` == "01:05" ]
then
    sh $OPENSHIFT_DATA_DIR/get_news.sh
fi
