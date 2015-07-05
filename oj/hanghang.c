#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int a[10];
int flag[11];
int ansCnt;

#define EQ1   ((a[0] + a[1] + a[2] + a[3]) == 24)
#define EQ2   ((a[3] + a[4] + a[5] + a[6]) == 24)
#define EQ3   ((a[6] + a[7] + a[8] + a[9]) == 24)

#define TRUE  1
#define FALSE 0

int find(int index)
{
	int i=0;
	int ret;

	if (index > 9)
	{
		if (!EQ3)
		{
			return FALSE;
		}

		for (i=0; i<10; i++)
		{
			printf("%d  ", a[i]);
		}
		printf("\n");
		return TRUE;
	}

	if (index == 4)
	{
		if (!EQ1)
		{
			return FALSE;
		}
	}

	if (index == 7)
	{
		if (!EQ2)
		{
			return FALSE;
		}
	}

	for (i=1; i<=10; i++)
	{
		if (flag[i] == 0)
		{
			flag[i] = 1;
			a[index] = i;
			ret = find(index + 1);
			if (TRUE == ret)
			{
				return TRUE;
			}
			else
			{
				flag[i] = 0;
				//return FALSE;
			}
		//	flag[i] = 0;
		}
	}
	
	//printf("unkown error!\n");

	return FALSE;
		
	

	//return find(index + 1);
}


void allAnswer(int index)
{
	int i;

	if (index > 9)
	{
		if ((!EQ3) || (!EQ2) || (!EQ1))
		{
			return;
		}

		for (i=0; i<10; i++)
		{
			printf("%d  ", a[i]);
		}
		printf("\n");
		ansCnt++;
	}

	for (i=1; i<=10; i++)
	{
		if (flag[i] == 0)
		{
			flag[i] = 1;
			a[index] = i;
			allAnswer(index + 1);
			a[index] = 0;
			flag[i] = 0;
		}
	}

	return;
}



int main()
{
	int i;
	
	//a[10] = {1,2,3,4,5,6,7,8,9};
	ansCnt = 0;
	
	for (i=0; i<10; i++)
	{
		a[i] = 0;
	}
	for (i=0; i<11; i++)
	{
		flag[i] = 0;
	}
	
//	(void)find(0);
	allAnswer(0);
	printf("total have %d answer!\n", ansCnt);

	return 0;
}



