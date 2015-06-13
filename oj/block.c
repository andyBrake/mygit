#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define RETURN_OK  (0)
#define RETURN_ERROR  (-1)

typedef struct tagBLOCK_S
{
	int *array;
	int rowSize;
	int colSize;

	int (* setPosValue)(struct tagBLOCK_S * block, int x, int y, int value);
	int (* getPosValue)(struct tagBLOCK_S * block, int x, int y);
	void (* rotateLeft90)(struct tagBLOCK_S * block); /* 向左，即逆时针旋转90度 */
	void (* rotateRight90)(struct tagBLOCK_S * block); /* 向右，即顺时针旋转90度 */
	void (* display)(struct tagBLOCK_S * block);
}BLOCK_S;

int setPosValue(struct tagBLOCK_S * block, int x, int y, int value);
int getPosValue(struct tagBLOCK_S * block, int x, int y);
void rotateLeft90(struct tagBLOCK_S * block); /* 向左，即逆时针旋转90度 */
void rotateRight90(struct tagBLOCK_S * block); /* 向右，即顺时针旋转90度 */
void display(struct tagBLOCK_S * block);


BLOCK_S * createBlock(int rowSize, int colSize)
{
	int *array;
	BLOCK_S *block;
	
	array = (int *)malloc(sizeof(int) * rowSize * colSize);
	if (NULL == array)
	{
		return NULL;
	}

	block = (BLOCK_S *)malloc(sizeof(BLOCK_S));
	if (NULL == block)
	{
		free(array);
		return NULL;
	}

	memset(array, 0, sizeof(int) * rowSize * colSize);
	block->array = array;
	block->rowSize = rowSize;
	block->colSize = colSize;

	/* register methods */
	block->setPosValue = setPosValue;
	block->getPosValue = getPosValue;
	block->rotateLeft90 = rotateLeft90;
	block->rotateRight90 = rotateRight90;
	block->display = display;


	return block;
}

void delBlock(BLOCK_S * block)
{
	int * array;

	if (NULL == block)
	{
		return;
	}

	array = block->array;
	free(array);
	free(block);
}

/* set pos(x,y) as value */
int setPosValue(struct tagBLOCK_S * block, int x, int y, int value)
{
	int *array;

	if (NULL == block)
	{
		return RETURN_ERROR;
	}
	if (NULL == block->array)
	{
		return RETURN_ERROR;
	}

	if (x < 0 || x > block->rowSize)
	{
		return RETURN_ERROR;
	}

	if (y < 0 || y > block->colSize)
	{
		return RETURN_ERROR;
	}

	array = block->array;
	//printf("set pos(%d,%d) as %d. \n", x, y, value);
	*(array + x * block->colSize + y) = value;

	return RETURN_OK;
}

int getPosValue(struct tagBLOCK_S * block, int x, int y)
{
	int *array;

	if (NULL == block)
	{
		return RETURN_ERROR;
	}
	if (x < 0 || x > block->rowSize)
	{
		return RETURN_ERROR;
	}
	if(y < 0 || y > block->colSize)
	{
		return RETURN_ERROR;
	}

	array = block->array;

	return *(array + block->colSize * x + y);
}

/* 向右，即顺时针旋转90度 */
void rotateRight90(struct tagBLOCK_S * block)
{
	int *desArray;
	int *array;
	int rowSize, colSize;
	int i, j;

	if (NULL == block)
	{
		return;
	}

	rowSize = block->rowSize;
	colSize = block->colSize;
	array = block->array;
	desArray = (int *)malloc(sizeof(int) * rowSize * colSize);
	if (NULL == desArray)
	{
		return;
	}
		
	for (i=0; i<rowSize; i++)
	{
		for (j=0; j<colSize; j++)
		{
			*(desArray + i*colSize + j) = *(array + colSize * (colSize - 1 - j) + i);
		}
	}

	block->array = desArray;
	free(array);

	return;
}

/* 向左，即逆时针旋转90度 */
void rotateLeft90(struct tagBLOCK_S * block)
{
	int *desArray;
	int *array;
	int rowSize, colSize;
	int i, j;

	if (NULL == block)
	{
		return;
	}

	rowSize = block->rowSize;
	colSize = block->colSize;
	array = block->array;
	desArray = (int *)malloc(sizeof(int) * rowSize * colSize);
	if (NULL == desArray)
	{
		return;
	}
		
	for (i=0; i<rowSize; i++)
	{
		for (j=0; j<colSize; j++)
		{
			*(desArray + i*colSize + j) = *(array + colSize * j + (rowSize - 1 - i));
		}
	}
	block->array = desArray;
	free(array);

	return;
}

void display(struct tagBLOCK_S * block)
{
	int i, j;

	if (NULL == block)
	{
		printf("NULL\n");
		return;
	}

	printf("the block is:\n");
	for (i=0; i<block->rowSize; i++)
	{
		for (j=0; j<block->colSize; j++)
		{
			printf("%3d  ", *(block->array + block->colSize * i + j));
		}
		printf("\n");
	}
}

int main()
{
	BLOCK_S * block;
	int rowSize = 4, colSize = 4;
	int i, j, value=1;

	block = createBlock(rowSize, colSize);
	
	for (i=0; i<rowSize; i++)
	{
		for (j=0; j<colSize; j++)
		{
			block->setPosValue(block, i, j, value++);
		}
	}

	block->display(block);

	printf("start to rotate right 90.\n");

	block->rotateRight90(block);

	block->display(block);

	printf("start to rotate left 90.\n");

	block->rotateLeft90(block);
	block->display(block);
}
