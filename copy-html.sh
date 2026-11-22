#!/bin/bash
# Manual deploy, for when CI is not available. The normal path is the
# build-deploy.yml workflow on every push to main.
# The site lives on the Hetzner host since 2026-11-22.

HOST=deploy@178.104.167.195
DEST=/home/deploy/learnche/site/pid/

#python create_permalinks.py
rsync -avvz  _build/html/*    		"$HOST:$DEST"
rsync -avvz  _build/latex/PID.pdf	"$HOST:$DEST"
