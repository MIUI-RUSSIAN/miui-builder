#!/bin/bash
( source ~/.bash_aliases ; smartlunch && make.system.userdata ; echo $? ) 2>&1 | tee build.log
