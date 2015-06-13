#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void getDirPos(int * x, int * y, int dir, int i, int j)
{
	switch (dir)
	{
		case 0: //up
			*x = i;
			*y = j + 1;
			break;

		case 1: //right
			*x = i + 1;
			*y = j;
			break;

		case 2: //down
			*x = i;
			*y = j - 1;
			break;

		case 3: //left
			*x = i - 1;
			*y = j;
			break;

		default:
			*x = -1;
			*y = -1;
			break;
	}

	return;
}

void dfs(int x, int y, char* grid, int gridRowSize, int gridColSize)
{
	int dir;
	int i, j;

	//printf("x=%d, y=%d\n", x, y);
	
	if (x < 0 || x >= gridRowSize)
	{
		return;
	}

	if (y < 0 || y >= gridColSize)
	{
		return;
	}

	if ('1' != grid[x * gridColSize + y])
	{
		return;
	}

	grid[x * gridColSize + y] = '2';
	
	/* 对4个方向进行递归搜索 */
	for (dir=0; dir<4; dir++)
	{
		//printf("x=%d, y=%d\n", x, y);
		getDirPos(&i, &j, dir, x, y);
	//	printf("x=%d, y=%d\n", x, y);
		//getchar();

		dfs(i, j, grid, gridRowSize, gridColSize);
	}

	return;
}




int numIslands(char* grid, int gridRowSize, int gridColSize)
{
    int treeCnt = 0;
	int i, j;
	//char *color;
	
	if (NULL == grid)
	{
		return 0;
	}
	if (gridRowSize < 0 || gridColSize < 0)
	{
		return 0;
	}

//	printf("-----grid[][] = %p, %p, %p, %p\n", grid[0], grid[1], grid[2], grid[3]);
//	printf("char grid = %c\n", grid[0]);

	//color = (char *)malloc(sizeof(char)* gridRowSize * gridColSize);
	//memset(color, 0, sizeof(char)* gridRowSize * gridColSize);

	for (i=0; i<gridRowSize; i++)
	{
		for (j=0; j<gridColSize; j++)
		{
			if (grid[i * gridColSize + j] == '1')
			{
				
				treeCnt++;

				dfs(i, j, grid, gridRowSize, gridColSize);
			}
		}
	}

	return treeCnt;
}


int main()
{
	int ret;
	int gridRowSize;
	int gridColSize;

	char test[] = "11110110101100000000";
	char test1[] = "010101010";

	//char *test1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

	gridRowSize = 3;
	gridColSize = 3;

	ret = numIslands(test1, gridRowSize, gridColSize);
	
	printf("ret = %d\n", ret);

	return 0;
}
