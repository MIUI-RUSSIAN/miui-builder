#!/bin/bash
# also write to build.log here..
(echo 'rm -rf out' && rm -rf out && source ~/.bash_aliases ; smartlunch && make.system.userdata ; echo $? ) 2>&1 | tee build.log
