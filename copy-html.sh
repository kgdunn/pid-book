#!/bin/bash

#python create_permalinks.py
rsync -avvz  _build/html/*    		learnche.org:/var/www/learnche.org/pid/
rsync -avvz  _build/latex/PID.pdf	learnche.org:/var/www/learnche.org/pid/
