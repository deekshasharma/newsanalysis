#!/bin/bash

if [ `date +%H:%M` == "00:00" ]
then
    nohup $OPENSHIFT_DATA_DIR/get_news.sh > $OPENSHIFT_TMP_DIR/logfile 2>&1 &
fi
