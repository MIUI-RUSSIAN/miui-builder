#!/bin/bash
( source ~/.bash_aliases ; alias ; sleep 4 ; smartlunch && make.system.userdata ; echo $? ; sleep 5 ) 2>&1 | tee build.log
