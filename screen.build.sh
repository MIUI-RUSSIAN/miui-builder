if [ `screen -list | grep "$2:build" -c` = 0 ]; then
cd "$1" && screen -S "$2:sync" -d -m ~/miui-builder/build.sh
else
echo "already running build on $1"
fi
