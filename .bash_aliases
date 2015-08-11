# golang
GOROOT=/usr/local/go
export GOPATH=/home/eggfly/go
export GOBIN=$GOPATH/bin
PATH=$PATH:$GOBIN:$GOROOT/bin
# revert

PATH=$PATH:~/ssd/adt-bundle-linux-x86_64/sdk/platform-tools/:~/ssd/adt-bundle-linux-x86_64/sdk/tools/

# stderred
# export LD_PRELOAD="/home/eggfly/stderred/build/libstderred.so${LD_PRELOAD:+:$LD_PRELOAD}"

# jdk6
function jdk6() {
. ~/env.sh && echo -e "\e[92m** JDK version was set to jdk6 \e[0m"
}

function jdk7() {
echo -e "\e[92m** JDK version was set to jdk7 \e[0m"
}

function PPath() {
~/product_path.py
}

function tim() {
~/time.py
}

function abandon() {
for b in `repo branch | awk '{print $2}'`; do repo abandon $b; done
}
function abandoncurrent() {
for b in `git branch | awk '{print $2}'`; do echo $b&&repo abandon $b .; done
}

# smartlunch
function smartlunch() {
cd `PPath` && mylunch && cd -
}

# alias
function make.system.9() {
make systemimage -j9
}

function make.system.1() {
make systemimage -j1
}

function make.system.userdata.jN() {
# TODO
make systemimage userdataimage -j8
}

function make.system.userdata() {
make systemimage userdataimage -j8
}

# lunch -> launch
function launch() {
. build/envsetup.sh
lunch $1-userdebug
}

# repo
alias r.upload.='repo upload .'
alias r.sync='repo sync -j8'
alias r.sync.='repo sync . -j8'
alias r.start.alpha='repo start alpha .'
alias r.start.dev='repo start dev .'
# git
alias g.status='git status'
alias g.commit='git commit -s'
alias g.commit.amend='git commit -s --amend'
alias g.commit.amend.no.edit='git commit -s --amend --no-edit'
alias g.reset.0.hard='git reset --hard'
alias g.reset.1.hard='git reset HEAD~ --hard'
alias pull="git pull --rebase"

# adb
alias debug='logcat-color -v time'
alias debugc='adb logcat -c && logcat-color -v time'
alias adb.root.remount='adb root && sleep 2 && adb remount'
alias soft.reboot='adb shell "stop;start;"'
# devices
alias fastboot.reboot='sudo fastboot reboot'
alias bootloader='adb reboot bootloader'
alias rec='adb reboot recovery'
alias flashcancro='~/flash.sh . cancro'
alias flashcancro1='~/flash1.sh . cancro'
alias flashcancro2='~/flash2.sh . cancro'
alias flashcancroerase='~/flash.sh . cancro erase'

alias flasharies='~/flash.sh . aries'
alias flasharies2='~/flash2.sh . aries'
alias flasharieserase='~/flash.sh . aries erase'

alias flashtaurus='~/flash.sh . taurus'
alias flashtaurus2='~/flash2.sh . taurus'
alias flashtauruserase='~/flash.sh . taurus erase'

alias flashpisces='~/flash.sh . pisces'
alias flashpisces2='~/flash2.sh . pisces'
alias flashpisceserase='~/flash.sh . pisces erase'

alias flashmocha='~/flash.sh . mocha'
alias flashmocha2='~/flash2.sh . mocha'
alias flashmochaerase='~/flash.sh . mocha erase'

alias flashvirgo='~/flash.sh . virgo'
alias flashvirgo2='~/flash2.sh . virgo'
alias flashvirgoerase='~/flash.sh . virgo erase'

alias flashleo='~/flash.sh . leo'
alias flashleo2='~/flash2.sh . leo'
alias flashleoerase='~/flash.sh . leo erase'

alias flashthomas_w='~/flash.sh . wt88047'
alias flashthomas_w2='~/flash2.sh . wt88047'
alias flashthomas_w_erase='~/flash.sh . wt88047 erase'

alias flashdior='~/flash.sh . dior'
alias flashdior2='~/flash2.sh . dior'
alias flashdiorerase='~/flash.sh . dior erase'

alias flashferrari='~/flash.sh . ferrari'
alias flashferrari2='~/flash2.sh . ferrari'
alias flashferrarierase='~/flash.sh . ferrari erase'

# cd 
alias ..='cd ..'
alias ..2='cd ../..'
alias ..3='cd ../../..'
alias ..4='cd ../../../..'
alias ..5='cd ../../../../..'
alias ..6='cd ../../../../../..'

# send.py
alias r.sync.send='r.sync 2>&1 | tee bulk.txt ; ~/send.py \`pwd\`'

alias repo.status.send='repo status 2>&1 | tee bulk.txt ; ~/send.py \`pwd\`'

alias make.send='smartlunch && make.system.userdata 2>&1 | tee bulk.txt ; ~/send.py \`pwd\`'
alias make.system.userdata.send='make.system.userdata 2>&1 | tee bulk.txt ; ~/send.py \`pwd\`'

# adb shell am
alias am='adb shell am start -n $1'

# adb log by process
alias gallery="debug | grep \`adb shell ps | grep com.xiaomi.gallery| awk '{print \$2}'\`"
alias cloudservice1="debug | grep \`adb shell ps | grep com.miui.cloudservice | awk 'NR==1{print \$2}'\`"
alias cloudbackup="debug | grep \`adb shell ps | grep com.miui.cloudbackup | awk '{print \$2}'\`"
alias cloudservice2="debug | grep \`adb shell ps | grep com.miui.cloudservice | awk 'NR==2{print \$2}'\`"
alias cloudservice_sync="debug | grep \`adb shell ps | grep com.miui.cloudservice:sync | awk '{print \$2}'\`"
alias xmsf="debug | grep \`adb shell ps | grep com.xiaomi.xmsf | awk '{print \$2}'\`"
alias xmaccount="debug | grep \`adb shell ps | grep com.xiaomi.account | awk '{print \$2}'\`"
alias smsdebug="debug | grep \`adb shell ps | grep com.eggfly.sms | awk '{print \$2}'\`"

alias rmsdk="rm -r \`PPath\`/out/target/common/obj/JAVA_LIBRARIES/{com.xiaomi.micloudsdk_intermediates,com.xiaomi.accountsdk_intermediates,cloud-common_intermediates}"
alias mmmsdkinner="mmm packages/apps/XiaomiAccountSdk/base/ packages/apps/MiCloudSDK/ miui/frameworks/opt/cloud/"
alias mmmsdk="cd \`PPath\` && mmmsdkinner && cd -"
alias refreshsdk="rmsdk || mmmsdk"


alias pullAccountDB="adb pull /data/system/users/0/accounts.db"
alias pushAccountDB="adb push accounts.db /data/system/users/0/accounts.db"
alias pullSMSDB='adb pull /data/data/com.android.providers.telephony/databases/mmssms.db'
alias pullContacts2DB="adb pull /data/data/com.android.providers.contacts/databases/contacts2.db"

alias pullSyncAccounts="adb pull /data/system/sync/accounts.xml"

alias cloudAppRestore="adb shell am start -n com.miui.cloudbackup/com.miui.cloudbackup.ui.CloudQueryRestoreAppActivity"
alias cloudAppSpace="adb shell am start -n com.miui.cloudbackup/com.miui.cloudbackup.ui.CloudBackupManageSpaceActivity"

alias pushAndRebootCancro="pushCloudCommonJarCancro && pushCloudServiceApkCancro && pushCloudBackupApkCancro && adb reboot"

# some push
alias pushCloudAppBackupApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/priv-app/CloudAppBackup.apk /system/priv-app"
alias pushCloudAppBackupApkCancro="pushCloudAppBackupApkCancroInner || (adb.root.remount && pushCloudAppBackupApkCancroInner)"

alias pushCloudBackupApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/priv-app/CloudBackup.apk /system/priv-app"
alias pushCloudBackupApkCancro="pushCloudBackupApkCancroInner || (adb.root.remount && pushCloudBackupApkCancroInner)"

alias pushSettingsApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/priv-app/Settings.apk /system/priv-app"
alias pushSettingsApkCancro="pushSettingsApkCancroInner || (adb.root.remount && pushSettingsApkCancroInner)"

alias pushDeskClockApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/app/DeskClock.apk /system/app"
alias pushDeskClockApkCancro="pushDeskClockApkCancroInner || (adb.root.remount && pushDeskClockApkCancroInner)"

# CloudService
alias pushCloudServiceApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/app/CloudService.apk /system/app"
alias pushCloudServiceApkMochaInner="adb push \`PPath\`/out/target/product/mocha/system/app/CloudService.apk /system/app"
alias pushCloudServiceApkPiscesInner="adb push \`PPath\`/out/target/product/pisces/system/app/CloudService.apk /system/app"
alias pushCloudServiceApkVirgoInner="adb push \`PPath\`/out/target/product/virgo/system/app/CloudService.apk /system/app"
alias pushCloudServiceApkFerrariInner="adb push \`PPath\`/out/target/product/ferrari/system/app/CloudService/CloudService.apk /system/app/CloudService"

alias pushCloudServiceApkCancro="pushCloudServiceApkCancroInner || (adb.root.remount && pushCloudServiceApkCancroInner)"
alias pushCloudServiceApkMocha="pushCloudServiceApkMochaInner || (adb.root.remount && pushCloudServiceApkMochaInner)"
alias pushCloudServiceApkPisces="pushCloudServiceApkPiscesInner || (adb.root.remount && pushCloudServiceApkPiscesInner)"
alias pushCloudServiceApkVirgo="pushCloudServiceApkVirgoInner || (adb.root.remount && pushCloudServiceApkVirgoInner)"
alias pushCloudServiceApkFerrari="pushCloudServiceApkFerrariInner || (adb.root.remount && pushCloudServiceApkFerrariInner)"

# CloudCommon
alias pushCloudCommonJarCancroInner="adb push \`PPath\`/out/target/product/cancro/system/framework/cloud-common.jar /system/framework/"
alias pushCloudCommonJarMochaInner="adb push \`PPath\`/out/target/product/mocha/system/framework/cloud-common.jar /system/framework/"
alias pushCloudCommonJarPiscesInner="adb push \`PPath\`/out/target/product/pisces/system/framework/cloud-common.jar /system/framework/"
alias pushCloudCommonJarVirgoInner="adb push \`PPath\`/out/target/product/virgo/system/framework/cloud-common.jar /system/framework/"
alias pushCloudCommonJarFerrariInner="adb push \`PPath\`/out/target/product/ferrari/system/framework/cloud-common.jar /system/framework/"

alias pushCloudCommonApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/app/CloudCommon.apk /system/app"

alias pushCloudCommonJarCancro="pushCloudCommonJarCancroInner || (adb.root.remount && pushCloudCommonJarCancroInner)"
alias pushCloudCommonJarMocha="pushCloudCommonJarMochaInner || (adb.root.remount && pushCloudCommonJarMochaInner)"
alias pushCloudCommonJarPisces="pushCloudCommonJarPiscesInner || (adb.root.remount && pushCloudCommonJarPiscesInner)"
alias pushCloudCommonJarVirgo="pushCloudCommonJarVirgoInner || (adb.root.remount && pushCloudCommonJarVirgoInner)"
alias pushCloudCommonJarFerrari="pushCloudCommonJarFerrariInner || (adb.root.remount && pushCloudCommonJarFerrariInner)"

alias pushCloudCommonApkCancro="pushCloudCommonApkCancroInner || (adb.root.remount && pushCloudCommonApkCancroInner)"

# XiaomiAccount
alias pushXiaomiAccountApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/app/XiaomiAccount.apk /system/app/"
alias pushXiaomiAccountApkMochaInner="adb push \`PPath\`/out/target/product/mocha/system/app/XiaomiAccount.apk /system/app/"
alias pushXiaomiAccountApkPiscesInner="adb push \`PPath\`/out/target/product/pisces/system/app/XiaomiAccount.apk /system/app/"
alias pushXiaomiAccountApkFerrariInner="adb push \`PPath\`/out/target/product/ferrari/system/app/XiaomiAccount/XiaomiAccount.apk /system/app/XiaomiAccount"

alias pushXiaomiAccountApkCancro="pushXiaomiAccountApkCancroInner || (adb.root.remount && pushXiaomiAccountApkCancroInner)"
alias pushXiaomiAccountApkMocha="pushXiaomiAccountApkMochaInner || (adb.root.remount && pushXiaomiAccountApkMochaInner)"
alias pushXiaomiAccountApkPisces="pushXiaomiAccountApkPiscesInner || (adb.root.remount && pushXiaomiAccountApkPiscesInner)"
alias pushXiaomiAccountApkFerrari="pushXiaomiAccountApkFerrariInner || (adb.root.remount && pushXiaomiAccountApkFerrariInner)"

# XiaomiServiceFramework
alias pushXMSFApkAriesInner="adb push \`PPath\`/out/target/product/aries/system/app/XiaomiServiceFramework.apk /system/app/"
alias pushXMSFApkCancroInner="adb push \`PPath\`/out/target/product/cancro/system/app/XiaomiServiceFramework.apk /system/app/"
alias pushXMSFApkMochaInner="adb push \`PPath\`/out/target/product/mocha/system/app/XiaomiServiceFramework.apk /system/app/"
alias pushXMSFApkPiscesInner="adb push \`PPath\`/out/target/product/pisces/system/app/XiaomiServiceFramework.apk /system/app/"

alias pushXMSFApkAries="pushXMSFApkAriesInner || (adb.root.remount && pushXMSFApkAriesInner)"
alias pushXMSFApkCancro="pushXMSFApkCancroInner || (adb.root.remount && pushXMSFApkCancroInner)"
alias pushXMSFApkMocha="pushXMSFApkMochaInner || (adb.root.remount && pushXMSFApkMochaInner)"
alias pushXMSFApkPisces="pushXMSFApkPiscesInner || (adb.root.remount && pushXMSFApkPiscesInner)"


# cd paths
alias cdcs="cd \`PPath\`/packages/apps/CloudService"
alias cdxmaccount="cd \`PPath\`/packages/apps/XiaomiAccount"
alias cdcc="cd \`PPath\`/miui/frameworks/opt/cloud"
alias cdxmaccountsdk="cd \`PPath\`/packages/apps/XiaomiAccountSdk"
alias cdp="cd \`PPath\`/packages/apps/\$1"

# try start lunch
function mylunch {
# jdk6 or jdk7
case "$PWD" in 
  *-jb*)
    jdk6
    ;;
  *-kk*)
    jdk6
    ;;
  *-l*)
    jdk7
    ;;
  *)
    jdk7
    ;;
esac

case "$PWD" in 
  *mione*)
    product=mione_plus
    ;;
  *cancro*)
    product=cancro
    ;;
  *aries*)
    product=aries
    ;;
  *mocha*)
    product=mocha
    ;;
  *pisces*)
    product=pisces
    ;;
  *virgo*)
    product=virgo
    ;;
  *dior*)
    product=dior
    ;;
  *gucci*)
    product=gucci
    ;;
  *wt86047*)
    # thomas_td 4g
    product=wt86047
    ;;
  *wt88047*)
    # thomas_w 4g
    product=wt88047
    ;;
  *lte26007*)
    # H2X(联芯)
    product=full_lte26007
    ;;
  *ferrari*)
    product=ferrari
    ;;
  *leo*)
    product=leo
    ;;
  *libra*)
    product=libra
    ;;
esac
launch $product
if [ "$product" ];then
   echo -e "\e[92m** Auto product lunched: "$product"\e[0m"
fi
}

# mylunch
# manually smartlunch now

alias capture='adb shell screenrecord /sdcard/recording.mp4'

# touch and keys
alias home='adb shell input keyevent 3'
alias tap='adb shell input tap \$1 \$2'
alias back='adb shell input keyevent 4'

function activesync () {
adb shell am broadcast -a android.intent.action.SYNC_STATE_CHANGED -ez active true -ez failing false
}

function cloudbackup_restore () {
adb shell am start -n com.miui.cloudbackup/com.miui.cloudbackup.ui.CloudQueryRestoreAppActivity
}
function syncdatasettings () {
adb shell am start com.miui.cloudservice/.ui.SyncDataSettingsActivity
}

function verboseMicloud () {
adb shell setprop log.tag.Micloud VERBOSE
}

function awsubuntu () {
ssh -i ~/aws.pem ubuntu@aws.eggfly.tk
}

function awseggfly () {
ssh eggfly@aws.eggfly.tk
}

function dinning_mail () {
python /home/eggfly/dinning/1/dinning_mailer.py
}

function dumpSync () {
adb shell dumpsys | grep -i "Active Syncs" -A 200
}

function cleanJava() {
rm -r out/target/{product/$TARGET_PRODUCT,common}/obj/{JAVA_LIBRARIES,APPS}
}

color()(set -o pipefail;"$@" 2>&1>&3|sed $'s,.*,\e[31m&\e[m,'>&2)3>&1

function grepSettingsBackupPrepare () {
adb shell setprop log.tag.SettingsBackup VERBOSE
adb logcat -c
}

function grepSettingsBackup () {
adb shell setprop log.tag.SettingsBackup VERBOSE
adb logcat -v time | grep SettingsBackup
}

function settingsDump () {
grepSettingsBackupPrepare
adb shell am startservice -a com.miui.cloudbackup.DUMP_SETTINGS -e device $1
grepSettingsBackup
}

function settingsDump_device_43e771f058d29ed46cda3b3053c94121_with_glass () {
settingsDump 43e771f058d29ed46cda3b3053c94121
}

function settingsDump_device_6e528692dc16e98b191ab7b76a871c0b () {
settingsDump 6e528692dc16e98b191ab7b76a871c0b
}

function settingsBackupByPackage () {
grepSettingsBackupPrepare
adb shell am startservice -a com.miui.cloudbackup.DEBUG_BACKUP -e packageName $1
grepSettingsBackup
}

function settingsRestoreByDeviceAndPackage () {
grepSettingsBackupPrepare
adb shell am startservice -a com.miui.cloudbackup.DEBUG_RESTORE -e device $1 -e packageName $2
grepSettingsBackup
}
function settingsRestoreByDeviceAndPackage_device_43e771f058d29ed46cda3b3053c94121 () {
grepSettingsBackupPrepare
adb shell am startservice -a com.miui.cloudbackup.DEBUG_RESTORE -e device 43e771f058d29ed46cda3b3053c94121 -e packageName $1
grepSettingsBackup
}
function copyToNginx() {
cp ../../../out/target/product/$TARGET_PRODUCT/system/priv-app/XiaomiGallery.apk /usr/share/nginx/html/com.xiaomi.gallery/com.xiaomi.gallery-`date "+%Y%m%d"`Build$1.apk
}
function genOTA() {
/usr/share/nginx/html/gen_ota.py $1
ln -sf /usr/share/nginx/html/com.xiaomi.gallery/com.xiaomi.gallery-`date "+%Y%m%d"`Build$1.apk /usr/share/nginx/html/gallery-latest.apk
}
function genOTAChangelog() {
vim /usr/share/nginx/html/com.xiaomi.gallery/com.xiaomi.gallery-`date "+%Y%m%d"`Build$1.txt
}
