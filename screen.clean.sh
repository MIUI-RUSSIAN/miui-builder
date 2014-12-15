if [ `screen -list | grep "$2:clean" -c` = 0 ]; then
cd "$1" && screen -S "$2:clean" -d -m ~/miui-builder/clean.sh
else
echo "already running clean on $1"
fi
