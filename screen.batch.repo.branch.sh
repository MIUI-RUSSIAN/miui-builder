if [ `screen -list | grep "batch-repo-branch" -c` = 0 ]; then
  screen -S "batch-repo-branch" -d -m ~/miui-builder/batch.repo.branch.sh
else
  echo "already running batch-repo-branch"
fi
