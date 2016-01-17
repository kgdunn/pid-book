#!/bin/bash

#python create_permalinks.py
rsync -avvz --delete _build/html/*    		connectmv.com:webapps/newlearnche/pid/
rsync -avvz --delete _build/latex/PID.pdf    	connectmv.com:webapps/newlearnche/pid/
scp htaccess connectmv.com:webapps/yint_redirect/pid/.htaccess
rm htaccess
