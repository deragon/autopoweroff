#!/bin/bash
# This script suspends the system during day to ram, and wakes up the device at
# 22:59. After 23:00 will the system be suspended  to disk.

current_time=$(date '+%H%M')
if [[ ${current_time} -ge 2259 ]] || [[ ${current_time} -le 600 ]]
then
   systemctl hibernate
else
   rtcwake -m mem -l -t "$(date -d 'today 23:00:00' '+%s')"
fi
