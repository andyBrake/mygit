#! /bin/bash -
echo  "this is test0\b"
printf "test printf string:%s, int:%d \n" hello 201
echo over
printf "enter password:"
stty -echo
read pw < /dev/tty
printf "\nthe ps is :$pw \n"
stty echo

printf "next \n"
find /Users/huangfa/Documents/project/mygit/shell -type d -print | sed 's;/Users/huangfa/Documents/project/mygit/shell;/Users/huangfa/Documents/project/mygit/sx;' | sed 's/^/mkdir /'| sh -x
