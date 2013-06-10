#!/bin/bash

if [`date +%H:%M` == "00:48"]
then
    sh $OPENSHIFT_DATA_DIR/get_news.sh
fi
