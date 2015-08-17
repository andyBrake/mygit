#include "header.h"


typedef struct tagITEM_S
{
	int start;
	int num;

	struct tagITEM_S * next;
	struct tagITEM_S * pre;
}ITEM_S;

/* 判断int a是否可以扩展item德边界，是则扩展item并返回1，否返回0 */
int canExpItem(ITEM_S * item, int a)
{
	if (a < item->start - 1
		|| a > item->start + item->num)
	{
		return 0;
	}

	if (a == item->start - 1)
	{
		item->start = a;
		item->num++;

		return 1;
	}

	if (a == item->start + item->num)
	{
		item->num++;

		return 1;
	}

	return 1;
}

void delItem(ITEM_S * item)
{
	ITEM_S *preItem, *nextItem;

	if (NULL == item)
	{
		return;
	}
	preItem = item->pre;
	nextItem = item->next;

	if (NULL != preItem)
	{
		preItem->next = nextItem;
	}
	if (NULL != nextItem)
	{
		nextItem->pre = preItem;
	}

	return;
}

/* 判断item是否可以跟他德前后两个item合并 */
void mergeItem(ITEM_S *item)
{ 
	ITEM_S *preItem, *nextItem;

	if (NULL == item)
	{
		return;
	}
	preItem = item->pre;
	nextItem = item->next;

	if (NULL != preItem)
	{
		if (preItem->start + preItem->num == item->start)
		{
			preItem->num += item->num;
			delItem(item);
			item = NULL;
		}
	}

	if (NULL != nextItem && NULL != item)
	{
		if (item->start + item->num == nextItem->start)
		{
			item->num += nextItem->num;
			delItem(nextItem);
			nextItem = NULL;
		}
	}

	return;
}

void addItem(ITEM_S * newItem, ITEM_S ** lastHeadItem)
{
	ITEM_S * preItem, *headItem;

	headItem = *lastHeadItem;

	if (NULL == newItem)
	{
		return;
	}
	//printf("want add item %d, num %d, head %d, num %d.\n", 
	//		newItem->start, newItem->num, headItem->start, headItem->num);
	
	while (headItem != NULL)
	{
		if (newItem->start < headItem->start)
		{
			preItem = headItem->pre;

			if (NULL != preItem)
			{
				preItem->next = newItem;
				newItem->pre = preItem;
			}
			headItem->pre = newItem;
			newItem->next = headItem;

			/* 如果原来德链表头发生了变化，需要更新 */
			if (headItem == *lastHeadItem)
			{
				*lastHeadItem = newItem;
			}
			/* 插入完成 */
			//printf("add before start %d, num %d.\n", headItem->start, headItem->num);
			return;
		}
		preItem = headItem;
		headItem = headItem->next;
	}
	/* 插入最后一个item后面 */
	preItem->next = newItem;
	newItem->pre = preItem;

	return;
}



int firstMissingPositive(int* nums, int numsSize) {
	int i, j;
	ITEM_S * headItem = NULL, *tmpItem = NULL, *newItem = NULL;
	int canExp;

	for (i=0; i<numsSize; i++)
	{
		if (nums[i] <= 0)
		{
			continue;
		}

		if (NULL == headItem)
		{
			headItem = (ITEM_S *)malloc(sizeof(ITEM_S));
			memset(headItem, 0, sizeof(ITEM_S));
			headItem->start = nums[i];
			headItem->num = 1;
			continue;
		}

		tmpItem = headItem;
		canExp = 0;
		while(tmpItem != NULL)
		{
			canExp = canExpItem(tmpItem, nums[i]);
			/* 扩展了某个item边界，则要考虑合并边界 */
			if (1 == canExp)
			{
				break;
			}
			if (nums[i] < tmpItem->start)
			{
				canExp = 0;
				break;
			}

			tmpItem = tmpItem->next;
		}

		if (1 == canExp)
		{
			mergeItem(tmpItem);
		}
		else
		{
			newItem = (ITEM_S *)malloc(sizeof(ITEM_S));
			memset(newItem, 0, sizeof(ITEM_S));
			newItem->start = nums[i];
			newItem->num = 1;
			/* 插入可以优化一下，不用每次从头找插入位置 */
			addItem(newItem, &headItem);
		}	
	}
	/* 所有输入数据处理完成，得到missing number */
	tmpItem = headItem;
	printf("head is start %d, num %d.\n", headItem->start, headItem->num);
	if(tmpItem != NULL)
	{
		if (tmpItem->start != 1)
		{
			return 1;
		}

		return tmpItem->start + tmpItem->num;
	}
	/* 空数组输入，缺少德就是1 */
	return 1;
}


int main()
{
	int ret;
	int test[] = {0, 1, 2};
	int numsSize = sizeof(test)/sizeof(test[0]);

	ret = firstMissingPositive(test, numsSize);

	printf("ret = %d.\n", ret);
}
