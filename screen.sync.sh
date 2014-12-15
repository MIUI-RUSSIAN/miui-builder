if [ `screen -list | grep "$2:build" -c` = 0 ]; then
cd "$1" && screen -S "$2:build" -d -m ~/miui-builder/sync.sh
else
echo "already running"
fi
