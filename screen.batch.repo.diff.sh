if [ `screen -list | grep "batch-repo-diff" -c` = 0 ]; then
  screen -S "batch-repo-diff" -d -m ~/miui-builder/batch.repo.diff.sh
else
  echo "already running batch-repo-diff"
fi
