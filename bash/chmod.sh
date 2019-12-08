#!/bin/bash

# 「文件权限修改」
# 作者 jitwxs
# 使用说明
# 1. 运行程序：添加可执行权限 sudo chmod +x chmod.sh
#              执行程序 sudo ./chmod path 「注意：路径最后不能包括/」
#					例如：sudo ./chmod ./testDir  √
#						  sudo ./chmod ./testDir/ ×
#
# 2. 改变权限：直接修改file_mode和dir_mode的值即可

file_mode=664
dir_mode=755

function read_dir(){
    for file in `ls $1`
    do
		path=$1"/"$file
        if [ -d $path ]
        then
			chmod $dir_mode $path
			echo $path "修改"$dir_mode"成功"
            read_dir $path
        else
			chmod $file_mode $path
			echo $path "修改"$file_mode"成功"
        fi
    done
}

read_dir $1 

