if [ `screen -list | grep "batch-repo-infos" -c` = 0 ]; then
  screen -S "batch-repo-infos" -d -m ~/miui-builder/batch.repo.infos.sh
else
  echo "already running batch-repo-infos"
fi
