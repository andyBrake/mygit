#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int getMax(int* nums, int numsSize, int start, int end, int * result) {
    int k;
    int tempMax;

	int	f[2048][3];
    
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
    
	f[start][0] = nums[0];
    f[start][1] = 1;
	f[start][2] = 1; //f[x][2] 表示是否取联0号位置，1表示qu

	if (nums[1+start] >= nums[start])
	{
		f[start+1][0] = nums[start+1];
		f[start+1][1] = 1;
		f[start+1][2] = 0;
	}
	else
	{
		f[start+1][0] = nums[start];
		f[start+1][1] = 0;
		f[start+1][2] = 1;
	}
    k=-1;
//	printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);
	k=0;
//	printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);

       
	//printf("start!\n");
    for (k=1; k != end ; k=(k+1)%numsSize)
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

		//printf("f[%d] is %d, qu %d, start %d.\n", k+1, f[k+1][0], f[k+1][1], f[k+1][2]);
    }

	//特殊处理一下最后的数，因为他和0号位置相领了
	if (f[numsSize - 1][2] == 1 && f[numsSize - 1][1] == 1)
	{
		//tempMax = f[numsSize - 2][0];
		*result = f[numsSize - 2][0];
		return -1;
	}
	else
	{
		*result = f[numsSize - 1][0];
		return 0;
	}
}


int rob(int* nums, int numsSize) 
{
	int ret1, ret2;
	int result, temp;
	int x;
	ret1 = getMax(nums, numsSize, 0, numsSize - 1, &x);
	ret2 = getMax(nums, numsSize, 1, 0, &x);

	if (0 == ret1)
	{
		return result;
	}
	else
	{
		temp = result;
		ret1 = getMax(nums, numsSize, 1, numsSize - 1, &result);
		if (result > temp)
		{
			return result;
		}
		return temp;
	}
}


int getMax2(int * nums, int numsSize, int start, int end)
{
	int p = 0, q = 0;
	int i;
	int tmp;

    for (i = start; i != end; i = (i + 1) % numsSize)
   	{
        tmp = p;
        p = p > (q + nums[i]) ? p : (q + nums[i]);
        q = tmp;
    }

    return p;

}

int rob2(int *nums, int numsSize)
{
	int res1, res2;
	
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

	res1 = getMax2(nums, numsSize, 0, numsSize-1);
	res2 = getMax2(nums, numsSize, 1, 0);
	//printf("res1 is %d, res2 is %d.\n", res1, res2);

	return res1 > res2 ? res1 : res2;
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
	for (i=1 ; i<=k ; i++)
	{
		ret = rob2(nums, i);

		printf("ret is %d.\n", ret);
	}
	return 0;
}
