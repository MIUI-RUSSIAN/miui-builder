for p in `~/miui-builder/projects.py`
do
  # cd first is important here
  cd $p
  (echo "updating repo branch info: $p" && repo branch ; echo $?) 2>&1 | tee repo.branch.log
  (echo "updating repo diff info: $p" && repo diff ; echo $?) 2>&1 | tee repo.diff.log
done
