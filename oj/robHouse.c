#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int rob(int* nums, int numsSize) {
    int k;
    //int *odd, *even;
   // int **f;
    int temp;

	int	f[20][3];
    
    if (numsSize <= 0)
    {

        return 0;
    }
    
    if (numsSize == 1)
    {

        return nums[0];
    }
    if (numsSize == 2)
    {

        return nums[0] > nums[1] ? nums[0] : nums[1];
    }
    
   // f[0] = (int *)malloc(sizeof(int) * numsSize);
   // f[1] = (int *)malloc(sizeof(int) * numsSize);
    //even = (int *)malloc(sizeof(int) * numsSize);
    printf("malloc\n");

	f[0][0] = nums[0];
    f[0][1] = 1;
	f[0][2] = 1; //f[x][2] 表示是否取联0号位置，1表示qu

	if (nums[1] >= nums[0])
	{
		f[1][0] = nums[1];
		f[1][1] = 1;
		f[1][2] = 0;
	}
	else
	{
		f[1][0] = nums[0];
		f[1][1] = 0;
		f[1][2] = 1;
	}
    k=-1;
	printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);
	k=0;
	printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);

       
	//printf("start!\n");
    for (k=1; k<numsSize-1; k++)
    {
        if (f[k][1] == 1)
        {
			if (f[k][0] >= f[k - 1][0] + nums[k+1])
            {
                f[k+1][0] = f[k][0];
                f[k+1][1] = 0;
				f[k+1][2] = f[k][2];
            }
            else
            {
                f[k+1][0] = f[k-1][0] + nums[k+1];
                f[k+1][1] = 1;
				f[k+1][2] = f[k-1][2];
            }
        }
        else
        {
            f[k+1][0] = f[k][0] + nums[k+1];
            f[k+1][1] = 1;
			f[k+1][2] = f[k][2];
        }

		printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);
    }

	//特殊处理一下最后的数，因为他和0号位置相领了
	if (f[numsSize - 1][2] == 1 && f[numsSize - 1][1] == 1)
	{
		return f[numsSize - 2][0];
	}
	else
	{
		return f[numsSize - 1][0];
	}
}

int main()
{
	int ret;
	int i;
	//int nums[] = {1, 1, 1,2};
	int nums[] = {1,1,3,6,7,10,7,1,8,5,9,1,4,4,3};

	int k = sizeof(nums)/sizeof(int);
	for (i=0; i<k; i++)
	{
		printf("%d ", nums[i]);
	}
	printf("\n");
	
	ret = rob(nums, k);

	printf("ret is %d.\n", ret);

	return 0;
}
