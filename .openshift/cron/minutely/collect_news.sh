#!/bin/bash

if [`date +%H:%M` == "00:54"]
then
    sh $OPENSHIFT_DATA_DIR/get_news.sh
fi
