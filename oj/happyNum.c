#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef int bool;

#define true  1
#define false 0

bool isAppered(int n, int * array, int * num)
{

    int i;
    printf("find %d in %d item.\n", n, *num);
    for (i=0; i< *num; i++)
    {
        if (n == array[i])
        {
            return true;
        }
    }
    if (i > 4095)
    {
        return true;
    }
    array[*num] = n;
    (*num)++;
    return false;
}

bool isHappy(int n) {
    int powN[] = {0, 1, 4, 9, 16, 25, 36, 49, 64, 81};
    int digit[32] = {0};
    int i = 0;
    int array[4096];
    int num = 0;
    
    if (n <= 0)
    {

        return false;
    }
    
    while(1)
 
 	{
		i = 0;
		
        while (n != 0)
 		{
            digit[i++] = n%10;
            n = n/10;
        }
        
        for (i--; i>=0; i--)
 
 		{
            n += powN[digit[i]];
        }
        printf("%d \n", n);
		getchar();//system("pause");
		
        if (1 == n)
 
 		{
            return true;
        }
        
        if (isAppered(n, array, &num))
        {

            return false;
        }
    }
}


int main()
{
	int n=2;
	bool ret;

	ret = isHappy(n);

	printf("%d is %s happy number!\n", n, ret==true ? "YES" : "NO");
}
