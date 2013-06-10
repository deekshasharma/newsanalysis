#!/bin/bash

if [`date +%H:%M` == "00:35"]
then
    curl -X POST http://newsanalysis-namepsace.rhcloud.com/add
fi
