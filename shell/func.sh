#!/bin/bash

calc ()
{
	local t
	t=$[$1 + $2]
	echo "in func t is" $t
	#printf "in func t is %d" $t
	return $t
}

fu()
{
	return 10
}
calc 1 2
res=$?

printf "print res is %d\n"  $res

fu
res=$?
echo "fu is :" $res
