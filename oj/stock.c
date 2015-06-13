#include <stdio.h>


int dpGetMaxProfig()
{
	int tempBuyIndex = 0;

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

		return;
	}

	return;
}

int maxProfit(int* prices, int pricesSize) 
{
	int i;

	if ()
	{}
}


int main()
{
	return 0;
}
