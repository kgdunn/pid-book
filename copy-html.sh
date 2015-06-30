#!/bin/bash

rsync -avvz --delete _build/html/*    		connectmv.com:webapps/newlearnche/pid/
rsync -avvz --delete _build/latex/PID.pdf    	connectmv.com:webapps/newlearnche/pid/
