[ $# -ge 2 ] || { echo "Usage: $0 branch_dir product_name [erase_data]"; exit 1; }
BRANCH_DIR=$1
PRODUCT_NAME=$2
# [ -d $BRANCH_DIR ] || BRANCH_DIR=~/disk/$1

adb devices
adb reboot bootloader

sudo fastboot erase cache

[ $# -eq 3 ] && sudo fastboot flash userdata $BRANCH_DIR/out/target/product/$PRODUCT_NAME/userdata.img

sudo fastboot flash boot $BRANCH_DIR/out/target/product/$PRODUCT_NAME/boot.img
sudo fastboot flash boot1 $BRANCH_DIR/out/target/product/$PRODUCT_NAME/boot.img
#sudo fastboot flash aboot $BRANCH_DIR/out/target/product/$PRODUCT_NAME/emmc_appsboot.mbn
sudo fastboot flash system $BRANCH_DIR/out/target/product/$PRODUCT_NAME/system.img
sudo fastboot flash system1 $BRANCH_DIR/out/target/product/$PRODUCT_NAME/system.img
#sudo fastboot flash system1 $BRANCH_DIR/out/target/product/$PRODUCT_NAME/system.img
#sudo fastboot flash recovery $BRANCH_DIR/out/target/product/$PRODUCT_NAME/recovery.img
sudo fastboot reboot

