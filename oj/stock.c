#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
  prices[]  all input prices
  n         prices[] size
  k         the Kth day

  profit[k] is global variable, record the max profit of start to k days.
 * */
void dpGetMaxProfig(int *prices, int n, int k,
		           int *buyIndex, int * profit, int *lastBuyIndex)
{
	int tempBuyIndex = 0;

	tempBuyIndex = *lastBuyIndex;

	if (k + 1 >= n)
	{
		return;
	}

	//the prices is same as last day, don't do anything	
	if (prices[k + 1] == prices[k])
	{
		profit[k + 1] = profit[k];
		buyIndex[k + 1] = buyIndex[k];

		return;
	
	}

	/* 股价上涨考虑收益增加，以及检查上次买入操作 */
	if (prices[k + 1] > prices[k])
	{
		if (prices[k + 1] - prices[tempBuyIndex] 
			> profit[k])
		{
			profit[k + 1] = prices[k + 1] - prices[tempBuyIndex];
			buyIndex[k + 1] = tempBuyIndex;
	
		}
		else
		{
			profit[k + 1] = profit[k];
			buyIndex[k + 1] = buyIndex[k];
	
		}
		return;
	}


	/* 股价下跌的时候考虑纪录tempbuyindex */
	if (prices[k + 1] < prices[k])
	
	{
		if (prices[k + 1] < prices[tempBuyIndex])
		{
			tempBuyIndex = k + 1;
		}
		profit[k + 1] = profit[k];
		buyIndex[k + 1] = buyIndex[k];
		*lastBuyIndex = tempBuyIndex;

		return;
	}

	return;
}

int maxProfit(int* prices, int pricesSize) 
{
	int *buyIndex;
   	int *profit;

	int i, lastBuyIndex = 0;

	buyIndex = (int *)malloc(sizeof(int) * pricesSize);
	profit = (int *)malloc(sizeof(int) * pricesSize);

	buyIndex[0] = 0;
	profit[0] = 0;

	for (i=0; i<pricesSize; i++)
	{
		dpGetMaxProfig(prices, pricesSize, i,
		           buyIndex, profit, &lastBuyIndex);
	}

	return profit[pricesSize - 1];
}


int main()
{
	int testPri[] = {2,3,4,3,2,1,3,5,7,9,8,5};
	int res;//should be 9-1=8

	res = maxProfit(testPri, sizeof(testPri)/sizeof(int));
	printf("get max profit is %d\n", res);

	return 0;
}
