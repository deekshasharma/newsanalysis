#!/bin/bash

if [ `date +%H:%M` == "00:59" ]
then
    sh $OPENSHIFT_DATA_DIR/get_news.sh
fi
