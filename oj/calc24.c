#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum tagCALC_TYPE_E
{
	CALC_ADD = 0,
	CALC_SUB,
	CALC_MUL,
	CALC_DIV,

	CALC_BUTT
}CALC_TYPE_E;

#define FINISH_INDEX (7)
#define TARGET_RESULT (24)

typedef struct tagINFO_S
{
	int handleIndex;  /* current position, which candidate will be choosed */
	int curIndex;  /* current handle element index 0~6, 7 means finish */
	int leftVal;   /* current result, as next calc left value, initial with 0 */
	int curCalcType; /* current calc type */
	int lastIndex;
	char usedFlag[7][4];
}INFO_S;

int g_num[4] = {8,2,9,1};
int g_flag[4] = {0, 0, 0, 0};

CALC_TYPE_E g_calc[4] = {0, 1, 2, 3};

int getNextNum(INFO_S *info)
{
	int i;

	for (i=info->handleIndex++; i<4; i++)
	{
		if (0 == g_flag[i])
		{
			g_flag[i] = 1;
			return i;
		}

		//if (0 == info->usedFlag[info->curIndex][i])
		//{
		//	info->usedFlag[info->curIndex][i] = 1;
		//	return i;
		//}
	}

	return -1;
}

//todo
int getNextCalcType(INFO_S *info)
{
	int i;

	for (i=0; i<4; i++)
	{
		if (0 == info->usedFlag[info->curIndex][i])
		{
			info->usedFlag[info->curIndex][i] = 1;
			return i;
		}
	}

	return -1;
}

//type 0 : num ; 1:calc type
int getNextElemIndex(INFO_S *info, int *type)
{
	int index;

	if (info->curIndex >= FINISH_INDEX)
	{
		return -1;
	}

	if (info->curIndex % 2 == 0)
	{
		index = getNextNum(info);
		if (index < 0)
		{
			return index;
		}	
		printf("get next num %d, index %d.\n", g_num[index], info->curIndex);
		*type = 0;
		return index;
	}

	index = getNextCalcType(info);
	if (index < 0)
	{
		return index;
	}
	printf("get next calcType %d, index %d.\n", g_calc[index], info->curIndex);

	*type = 1;
	return index;
}

int calc(int left, int right, int calcType)
{
	switch(calcType)
	{
		case 0: return left + right;
		case 1: return left - right;
		case 2: return left*right;
		case 3: return left/right;
		default: return 0;
	}
}

void updataInfo(INFO_S *info, int index, int type)
{
	info->curIndex++;
	
	if (0 == type)
	{
		info->leftVal = calc(info->leftVal, g_num[index], info->curCalcType);
	}
	else
	{
		info->curCalcType = g_calc[index];
	}
}

void backInfo(INFO_S *info, int index, int type)
{
	//info->curIndex--;

	if (0 == type)
	{
		g_flag[index] = 0;
		return;
	}
	
	//info->usedFlag[info->curIndex][index] = 0; 
	int i;
	for (i=0; i<4; i++)
	{
		info->usedFlag[info->curIndex][i] = 0;
	}
	info->curIndex--;
		
	return;
}

void disPlay(INFO_S *info, int index, int type)
{
	if (0 == type)
	{
		printf(" %d ", g_num[index]);
	}
	else
	{
		switch(g_calc[index])
		{
			case 0: printf(" + "); break;
			case 1: printf(" - "); break;
			case 2: printf(" * "); break;
		    case 3: printf(" / ");break;
			default:break;
		}
	}
	//printf("%d -", info->leftVal);
}

int getResult(INFO_S *info)
{
	int curNumIndex, lastChoseIndex;
	int type = 0;
	int ret;

	if (info->curIndex < 0)
	{
		printf("back index to zero!\n");
		return -1;
	}

	//printf("\n");
	//printf("get result index %d.\n", info->curIndex);

	if (FINISH_INDEX == info->curIndex)
	{
		if (TARGET_RESULT == info->leftVal)
		{
			return 0;
		}
		
		backInfo(info, info->lastIndex, 0);

		return -1;
	}

	lastChoseIndex = info->lastIndex ;
	info->handleIndex = 0;

	while(1)
	{
		curNumIndex = getNextElemIndex(info, &type);
		if (curNumIndex < 0)
		{
			backInfo(info, curNumIndex, type);
			//break;
			return -1;
		}

		updataInfo(info, curNumIndex, type);
		info->lastIndex = curNumIndex;

		ret = getResult(info);
		if (0 == ret)
		{
			disPlay(info, curNumIndex, type);
			return 0;
		}
		
		//backInfo(info, curNumIndex, type);
	}
	//printf("flag : %d, %d, %d, %d, index : %d.\n", g_flag[0], g_flag[1], g_flag[2], g_flag[3], info->curIndex);

	type = (info->curIndex % 2 == 0) ? 0 : 1;
	backInfo(info, lastChoseIndex, type);

	printf("flag : %d, %d, %d, %d, index : %d.\n", g_flag[0], g_flag[1], g_flag[2], g_flag[3], info->curIndex);


	return -1;
}

int main()
{
	INFO_S info;
	int ret;

	memset(&info, 0, sizeof(INFO_S));
	ret = getResult(&info);

	printf("ret is %d.\n", ret);
}
