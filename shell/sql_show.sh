#!/bin/bash

#cat sql.txt
VOLINDEX_TABLE="status clone_index clone_id"
LUN_TABLE="status lunId"

TABLE_ITEM=$LUN_TABLE

echo ${TABLE_ITEM[0]} ${TABLE_ITEM[1]}

cnt=0
item=1

while read -r line
do
	echo $cnt  "line raw is: " $line
	#echo $cnt " after split:"
#echo $line | awk -v DES={"status", "ss", } '{split($0,a,"|" );} { for(i=1;i<=3;i++)  printf("%s:%s ",DES[i], a[i])} {printf("\n")}'
    item=1
    for i in $TABLE_ITEM
    do
        echo -n $i " : "
        echo $line | cut -d "|" -f ${item}
    ((item++))
    done

	((cnt++))	
done<sql.txt

echo "end"

