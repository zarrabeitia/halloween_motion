#!/bin/sh

motion -c motion.conf &
python play.py
killall motion

