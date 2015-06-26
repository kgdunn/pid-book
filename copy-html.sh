#!/bin/bash

rsync -avvz --delete _build/html/*    connectmv.com:webapps/learnche/pid/
