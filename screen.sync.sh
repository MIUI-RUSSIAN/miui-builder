if [ `screen -list | grep "$2:sync" -c` = 0 ]; then
cd "$1" && screen -S "$2:sync" -d -m ~/miui-builder/sync.sh
else
echo "already running sync on $1"
fi
