# JDK 1.6
export JAVA_HOME=/opt/jdk1.6.0_45

# JDK 1.7
#export JAVA_HOME=/opt/jdk1.7.0_71

# common
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$PATH

# bin
PATH=/home/eggfly/bin:$PATH
# PATH=/home/eggfly/bin:/home/eggfly/ssd/adt-bundle-linux-x86_64-20131030/sdk/platform-tools:$PATH
