#include "header.h"

#define MAX_REC  (100)

typedef struct tagNODE_INFO_S
{
	int x;
	int y;
	int value; /* 该点的值，为正表示加血，为负表示减血 */

	int r[MAX_REC]; /* 走到该点时剩余生命值 */
	int minHp[MAX_REC]; /* 到达该点所需要的最低hp，初始化为0 */
	int sum[MAX_REC];   /* 从上方到达该点的路径累加值 */
	int recCnt; //纪录个数

	}NODE_INFO_S;

/* 根据上一个节点的相关信息计算本节点的最小hp */
int calcMinHp(NODE_INFO_S * lastMapNodeInfo, NODE_INFO_S * curMapNodeInfo)
{
	int preMinHp, preSum, curValue;
	int lastCnt, curCnt;
	int tmp;
	int i;

	lastCnt = lastMapNodeInfo->recCnt;
	curValue = curMapNodeInfo->value;
	curCnt = curMapNodeInfo->recCnt;

	for (i=0; i<lastCnt; i++)
	{
		curCnt = curMapNodeInfo->recCnt;
		preMinHp = lastMapNodeInfo->minHp[i];
		preSum = lastMapNodeInfo->sum[i];
		//preRer = lastMapNodeInfo->r[i];
	
		tmp = curValue + preSum;
		
		/* 如果当前node的sum是正数，则minhp不变 */
		if (tmp > 0)
		{
			curMapNodeInfo->sum[curCnt] = tmp;
			curMapNodeInfo->minHp[curCnt] = preMinHp;	
			curMapNodeInfo->r[curCnt] = 
				curMapNodeInfo->sum[curCnt] + curMapNodeInfo->minHp[curCnt];

			curMapNodeInfo->recCnt = ++curCnt;

			continue;
		}
		/* 当前node的sum为负数，纪录 */
		tmp = abs(tmp) + 1;
		tmp = tmp > preMinHp 
				? tmp : preMinHp;

		curMapNodeInfo->sum[curCnt] = curValue + preSum;
		curMapNodeInfo->minHp[curCnt] = tmp;	

		curMapNodeInfo->r[curCnt] = curMapNodeInfo->sum[curCnt] + curMapNodeInfo->minHp[curCnt];
				curMapNodeInfo->recCnt = ++curCnt;

		//handleNodeInfo(curMapNodeInfo);
		//curMapNodeInfo.minHp = tmp;
	}
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

		mapNodeInfo[0].minHp[0] = mapNodeInfo[0].value <= 0 ? 1 + abs(mapNodeInfo[0].value) : 1;
		mapNodeInfo[0].sum[0] = mapNodeInfo[0].value;
		mapNodeInfo[0].r[0] = mapNodeInfo[0].minHp[0] + mapNodeInfo[0].sum[0];
		mapNodeInfo[0].recCnt = 1;
		//printf("00 is %d.\n", mapNodeInfo[0].value);
		return;
	}
	/* 第一行的点特殊处理 */
	if (i == 0)
	{

		preIndex = j - 1;
		//tempSum = mapNodeInfo[curIndex].value + mapNodeInfo[preIndex].sum;
		//mapNodeInfo[curIndex].sum = tempSum;

		calcMinHp(&mapNodeInfo[preIndex], &mapNodeInfo[curIndex]);

		return;
	}

	/* 第一列的点特殊处理 */
	if (j == 0)
	{

		preIndex = (i-1)*colSize;
		calcMinHp(&mapNodeInfo[preIndex], &mapNodeInfo[curIndex]);

		return;
	}
	/* 其他内部节点需要考虑从两个方向分别得到的解，然后取最优解 */
	preIndex = (i-1)*colSize + j; /* 上方的点 */
	otherPreIndex = (i*colSize) + j - 1;  /* 左方的点 */

	calcMinHp(&mapNodeInfo[preIndex], &mapNodeInfo[curIndex]);

	calcMinHp(&mapNodeInfo[otherPreIndex], &mapNodeInfo[curIndex]);
	
	return;
}

//In order to reach the princess as quickly as possible, 
//the knight decides to move only rightward or downward in each step.
int calculateMinimumHP(int** dungeon, int dungeonRowSize, int dungeonColSize) 
{
	NODE_INFO_S * mapNodeInfo;
	int i, j;
	int ret;

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
			mapNodeInfo[i*dungeonColSize + j].recCnt = 0;
			/* 逐行计算minhp */
			getMinHp(i, j, mapNodeInfo, dungeonRowSize, dungeonColSize);

			printf("i=%d, j=%d:\n", i, j);
			for (ret=0; ret<mapNodeInfo[i*dungeonColSize + j].recCnt; ret++)
			{
				printf("pos(%d, %d) minHp is %d, sum is %d, reserved is %d.\n", 
					i, j, 
					mapNodeInfo[i*dungeonColSize + j].minHp[ret], 
					mapNodeInfo[i*dungeonColSize + j].sum[ret],
					mapNodeInfo[i*dungeonColSize + j].r[ret]);
			}
			
		}
	}

	ret = mapNodeInfo[dungeonColSize*dungeonRowSize -1].minHp[0];
	for (i=1; i<mapNodeInfo[dungeonColSize*dungeonRowSize -1].recCnt; i++)
	{
		//printf("");
		if (ret > mapNodeInfo[dungeonColSize*dungeonRowSize -1].minHp[i])
		{
			ret = mapNodeInfo[dungeonColSize*dungeonRowSize -1].minHp[i];
		}
	}
	return ret; 
}


int main()
{
	int ret, i, j;
	int rowSize = 3, colSize = 3;
	//int test[1][7] = {0, 1, 1, -10, 9, -2, -20};
	int test[][3] = {

		{1, -3, 3},
		{0, -2, 0},
		{-3, -3, -3}
	};
	int *ppTest[7];
	int *p;

	printf("the array is :\n");
	for (i=0; i<rowSize; i++)
	{
		for (j=0; j<colSize; j++)
		{
			printf("%2d\t", test[i][j]);
		}
		printf("\n");
	}

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
	printf("ret = %d.\n", ret);
}
