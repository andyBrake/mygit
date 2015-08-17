#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sort(int *a, int left, int right)
{
    int i = left;
    int j = right;
    int key = a[left];
    
    if(left >= right)/*如果左边索引大于或者等于右边的索引就代表已经整理完成一个组了*/
    {
        return ;
    }
     
    while(i < j)                               /*控制在当组内寻找一遍*/
    {
        while(i < j && key <= a[j])
        /*而寻找结束的条件就是，1，找到一个小于或者大于key的数（大于或小于取决于你想升
        序还是降序）2，没有符合条件1的，并且i与j的大小没有反转*/ 
        {
            j--;/*向前寻找*/
        }
         
        a[i] = a[j];
        /*找到一个这样的数后就把它赋给前面的被拿走的i的值（如果第一次循环且key是
        a[left]，那么就是给key）*/
         
        while(i < j && key >= a[i])
        /*这是i在当组内向前寻找，同上，不过注意与key的大小关系停止循环和上面相反，
        因为排序思想是把数往两边扔，所以左右两边的数大小与key的关系相反*/
        {
            i++;
        }
         
        a[j] = a[i];
    }
     
    a[i] = key;/*当在当组内找完一遍以后就把中间数key回归*/
    sort(a, left, i - 1);/*最后用同样的方式对分出来的左边的小组进行同上的做法*/
    sort(a, i + 1, right);/*用同样的方式对分出来的右边的小组进行同上的做法*/
                       /*当然最后可能会出现很多分左右，直到每一组的i = j 为止*/
}

int binarySearch(int* nums, int start, int end, int key)
{
    int mid;
    
    while (start <= end)
    {

        mid = (start+end)/2;
		//printf("%d, %d, %d \n", start, mid, end);
        
        if (key == nums[mid])
        {
            return mid;
        }
        if (nums[mid] > key)
        {
            end = mid-1;
            continue;
        }
        if (nums[mid] < key)
        {
            start = mid+1;
            continue;
        }
    }
    
    return -1;
}

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target) {
    int i, j, ret;
    int remindTar;
    
    int *retMem;
    retMem = (int *)malloc(sizeof(int) * 2);
    
    
    sort(nums, 0, numsSize - 1);
	printf("after sort.\n");
    //优化算法：先对输入数组进行排序，然后再找index2的时候可以用二分查找
    
    
    
    for (i=0; i<numsSize; i++)
    {

        remindTar = target - nums[i];
        
        ret = binarySearch(nums, i, numsSize-1, remindTar);
		printf("after search.\n");
        if (ret >= 0)
        {
            retMem[0] = i+1;
            retMem[1] = ret+1;
            return retMem;
        }
    }
    
    retMem[0] = 0;
    retMem[1] = 1;
    
    return retMem;
}

int main()
{
	int * ret;
	int test[] = {3, 2, 4};
	int target = 6;

	ret = twoSum(test, sizeof(test)/sizeof(int), target);
	printf("index0 = %d, index1 = %d.\n", ret[0], ret[1]);
}
