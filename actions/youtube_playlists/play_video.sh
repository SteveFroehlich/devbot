#!/bin/sh

VIDEO_URL=$1
nohup ffplay -i $(youtube-dl --format 140 --get-url $VIDEO_URL) >/dev/null 2>&1 &
