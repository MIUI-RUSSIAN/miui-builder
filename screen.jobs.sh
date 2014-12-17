if [ `screen -list | grep "jobs" -c` = 0 ]; then
  screen -S "jobs" -d -m ~/miui-builder/jobs.py
else
  echo "already running jobs"
fi
