for p in `~/miui-builder/projects.py`
do
  # cd first is important here
  cd $p
  (echo "updating repo diff info: $p" && repo diff ; echo $?) 2>&1 | tee repo.diff.log
done
