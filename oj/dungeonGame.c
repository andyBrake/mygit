#include "header.h"

typedef struct tagNODE_INFO_S
{
	int x;
	int y;
	int value; /* 该点的值，为正表示加血，为负表示减血 */
	int sum;   /* 到达该点产生minhp的路径累加值 */
	int minHp; /* 到达该点所需要的最低hp，初始化为0 */
}NODE_INFO_S;

/* 根据上一个节点的相关信息计算本节点的最小hp */
int calcMinHp(int preMinHp, int preValue, int preSum, int curValue)
{
	int curMinHp;
	int tmp;

	tmp = curValue + preSum;
	//mapNodeInfo[curIndex].sum = tempSum;

	if (tmp > 0)
	{
		return preMinHp;
	}
	tmp = abs(tmp) + 1;
	tmp = tmp > preMinHp 
			? tmp : preMinHp;
	return tmp;
}

void getMinHp(int i, int j, NODE_INFO_S * mapNodeInfo, int rowSize, int colSize)
{
	int tempSum, tempSum2;
	int preIndex, curIndex;
	int otherPreIndex;

	curIndex = (i*colSize) + j;

	/* 第一个点特殊处理 */
	if (i == 0 && j == 0)
	{
		mapNodeInfo[0].minHp = mapNodeInfo[0].value <= 0 ? 1 + abs(mapNodeInfo[0].value) : 0;
		mapNodeInfo[0].sum = mapNodeInfo[0].value;
		//printf("00 is %d.\n", mapNodeInfo[0].value);
		return;
	}
	/* 第一行的点特殊处理 */
	if (i == 0)
	{
		preIndex = j - 1;
		tempSum = mapNodeInfo[curIndex].value + mapNodeInfo[preIndex].sum;
		mapNodeInfo[curIndex].sum = tempSum;

		if (tempSum > 0)
		{
			mapNodeInfo[curIndex].minHp = mapNodeInfo[preIndex].minHp;
			return;
		}
		else
		{
			tempSum = abs(tempSum) + 1;
			tempSum = tempSum > mapNodeInfo[preIndex].minHp 
							? tempSum : mapNodeInfo[preIndex].minHp;
			mapNodeInfo[curIndex].minHp = tempSum;
			return;
		}

		return;
	}

	/* 第一列的点特殊处理 */
	if (j == 0)
	{
		preIndex = (i-1)*colSize;
		tempSum = mapNodeInfo[curIndex].value + mapNodeInfo[preIndex].sum;
		mapNodeInfo[curIndex].sum = tempSum;

		if (tempSum > 0)
		{
			mapNodeInfo[curIndex].minHp = mapNodeInfo[preIndex].minHp;
			return;
		}
		else
		{
			tempSum = abs(tempSum) + 1;
			tempSum = tempSum > mapNodeInfo[preIndex].minHp 
						? tempSum : mapNodeInfo[preIndex].minHp;
			mapNodeInfo[curIndex].minHp = tempSum;
			return;
		}

		return;
	}
	/* 其他内部节点需要考虑从两个方向分别得到的解，然后取最优解 */
	preIndex = (i-1)*colSize + j; /* 上方的点 */
	otherPreIndex = (i*colSize) + j - 1;  /* 左方的点 */


	return;
}

//In order to reach the princess as quickly as possible, 
//the knight decides to move only rightward or downward in each step.
int calculateMinimumHP(int** dungeon, int dungeonRowSize, int dungeonColSize) 
{
	NODE_INFO_S * mapNodeInfo;
	int i, j;

	mapNodeInfo = (NODE_INFO_S *)malloc(sizeof(NODE_INFO_S)*dungeonRowSize*dungeonColSize);
	if (NULL == mapNodeInfo)
	{
		return -1;
	}
	/* 初始化全局信息 */
	for (i=0; i<dungeonRowSize; i++)
	{
		for (j=0; j<dungeonColSize; j++)
		{
			mapNodeInfo[i*dungeonColSize + j].x = i;
			mapNodeInfo[i*dungeonColSize + j].y = j;
			mapNodeInfo[i*dungeonColSize + j].value = dungeon[i][j];
			/* 逐行计算minhp */
			getMinHp(i, j, mapNodeInfo, dungeonRowSize, dungeonColSize);

			printf("pos(%d, %d) minHp is %d, sum is %d.\n", 
					i, j, 
					mapNodeInfo[i*dungeonColSize + j].minHp, 
					mapNodeInfo[i*dungeonColSize + j].sum);
		}
	}

	return 0;	
}

	/*
	 -2, -3, 3
	 -5, -10,1
	 10, 30,-5
	 * */

int main()
{
	int ret, i, j;
	int rowSize = 3, colSize = 3;
	//int test[1][7] = {0, 1, 1, -10, 9, -2, -20};
	int test[][3] = {
		{-2, -3, 3},
		{-5, -10, 1},
		{10, 30, -5}
	};
	int *ppTest[7];
	int *p;

	for (i=0; i<rowSize; i++)
	{
		p = (int *)malloc(sizeof(int) * colSize);
		ppTest[i] = p;

		for (j=0; j<colSize; j++)
		{
			ppTest[i][j] = test[i][j];
		}
	}


	ret = calculateMinimumHP(ppTest, rowSize, colSize); 
}
