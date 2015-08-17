#include "header.h"
typedef struct tagMEM_S
{
	int key;
	int data;
}MEM_S;

int tmpCmp(void * a, void * b);

void swap(char * arr, int unitSize, int i, int j)
{
	char * temp;
	char *pi, *pj;

	pi = (char *)(arr + unitSize * i);
	pj = (char *)(arr + unitSize * j);
	temp = (char *)malloc(unitSize);

	memcpy(temp, pi, unitSize);
	memcpy(pi, pj, unitSize);
	memcpy(pj, temp, unitSize);
	
	return;	
}

void generalQuickSort(char *arr, int unitNum, int unitSize, 
		int (* cmp)(void *a, void *b), 
		int start, int end)
{
	char *pi, *pj, *pKey;
	int i, j;

	//递归退出条件：只有一个元素时
	if(start >= end)
	{   		
		return;
    }

	/* 第一个元素作为基本比较key */
	pKey = (char *)(arr + unitSize * start);
    i = start;

    for(j = start+1; j <= end; j++)
	{
		pj = (char *)(arr + unitSize * j);
        
		if (cmp((void *)pj, (void *)pKey) < 0)
		{                    
			i++;    //a[i] is bigger than pivot

            if(i!=j)
			{
				//Swap(arr[i], arr[j]);
				swap(arr, unitSize, i, j);
            }
		}
    }
	//Swap(arr[start], arr[i]);    //Swap pivot to middle position
	swap(arr, unitSize, start, i);

	//进行分化(partition),递归
    generalQuickSort(arr, unitNum, 
			sizeof(MEM_S), 
			tmpCmp,
			start,i-1);

    generalQuickSort(arr, unitNum, 
			sizeof(MEM_S), 
			tmpCmp,

			i+1,end);
	
	return;
}

//a < b return -1
int tmpCmp(void * a, void * b)
{
	MEM_S * pa, *pb;

	pa = (MEM_S *)a;
	pb = (MEM_S *)b;

	if (pa->key < pb->key)
	{
		return -1;
	}

	if (pa->key == pb->key)
	{
		return 0;
	}

	return 1;
}

int main()
{
	MEM_S * test;
	int num = 50000;
	int i, j;


	test = (MEM_S *)malloc(sizeof(MEM_S) * num);

	for (i=0; i<num; i++)
	{
		test[i].key = num - i;
		test[i].data = 10 + i;
	}

	printf("the src array is :\n");
//	for (i=0; i<num; i++)
	{
		//printf("index %d, key=%d, data=%d.\n", i, test[i].key, test[i].data);
	}

	printf("the sorted array is :\n");
	generalQuickSort((char *)test, num, 
			sizeof(MEM_S), 
			tmpCmp,
			0, num-1);
//	for (i=0; i<num; i++)
	{
	//	printf("index %d, key=%d, data=%d.\n", i, test[i].key, test[i].data);
	}

	return 0;
}
