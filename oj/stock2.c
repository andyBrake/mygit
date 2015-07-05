#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times). However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
*/


/* 不限次数的交易，获取最大利润 */
int maxProfit(int* prices, int pricesSize) 
{
	int i;
	int flag = 0; //0 is will buy, 1 will sell
	int isAscend = 0; // 1 is in ascend
	int maxProfit = 0, buyPrice, lastPrice;

	if (pricesSize <= 1)
	{
		return 0;
	}

	lastPrice = prices[0];
	for (i=1; i<pricesSize; i++)
	{
		if (lastPrice == prices[i])
		{
			if (pricesSize - 1 == i)
			{
				if (flag == 1)
				{
					maxProfit += (prices[i] - buyPrice);
				}
				else 
				{
					//maxProfit += (prices[i] - lastPrice);
					printf("error!\n");
				}
			}

		}
		//股价上涨
		else if (lastPrice < prices[i])
		{
			//起始位置特殊处理
			if (1 == i)
			{
				buyPrice = lastPrice;
				flag = 1;

				if (pricesSize - 1 == i)
				{
					return prices[i]- lastPrice;
				}
			}
			//终点位置特俗处理
			else if (pricesSize - 1 == i)
			{
				if (flag == 1)
				{
					maxProfit += (prices[i] - buyPrice);
				}
				else //终点位置，且是股价上涨趋势的时候，如果还是准备买入阶段，则买入点即使上一个点
				{
					maxProfit += (prices[i] - lastPrice);
					//printf("error!\n");
				}
			}
			//之前的趋势是下跌，如果之前趋势是上涨，则无操作
			else if (isAscend != 1)
			{
				//目前状态是准备买入，如果目前状态是准备卖出，则无操作
				if (flag == 0)
				{
					buyPrice = lastPrice;
					flag = 1;
				}
			}

			isAscend = 1;
		}
		//股价下跌
		else
		{
			//之前趋势是上涨，如果之前趋势是跌，则无操作
			if (isAscend)
			{
				//目前状态是准备卖出，如果目前状态为准备买入，则无操作
				if (flag == 1)
				{
					maxProfit += (lastPrice - buyPrice);
					flag = 0;
				}
			}

			isAscend = 0;
		}

		lastPrice = prices[i];
	}

	return maxProfit;
}



int main()
{
	int testPri[] = {2,3,4,3,2,1,3,5,7,9,8,5};
	int test2[] = {1,2,3,4,5,6,7,8,9};
	int test3[] = {9,8,7,6,5,4,3,2,1};
	int test4[] = {1,9,6,9,1,7,1,1,5,9,9,9};
	int res;//should be 9-1=8

	//res = maxProfit(testPri, sizeof(testPri)/sizeof(int));
	//printf("get max profit is %d\n", res);

	res = maxProfit(test2, sizeof(test2)/sizeof(int));
	printf("get max profit is %d\n", res);

	//res = maxProfit(test3, sizeof(test3)/sizeof(int));
	//printf("get max profit is %d\n", res);
	
	res = maxProfit(test4, sizeof(test4)/sizeof(int));
	printf("get max profit is %d\n", res);


	return 0;
}
