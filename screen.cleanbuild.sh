if [ `screen -list | grep "$2:cleanbuild" -c` = 0 ]; then
cd "$1" && screen -S "$2:cleanbuild" -d -m ~/miui-builder/cleanbuild.sh
else
echo "already running cleanbuild on $1"
fi
