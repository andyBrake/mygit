#include <stdio.h>
#include <stdlib.h>

typedef struct tagPoint
{
	int x;
	int y;
}Point;

typedef struct tagLine
{
	int k;
	int b;
}Line;

/* 通过两个点计算出line的斜率和偏移，但是可能都是分数 */
void getLineStruct(Point *p0, Point *p1, Line *line)
{
	int x, y;

	x = p0->x - p1->x;
	y = p0->y - p1->y;

	
}

/**
 *
 * Definition for a point.
 * struct Point {
 *     int x;
 *     int y;
 * }
 */
int maxPoints(struct Point* points, int pointsSize) {
    
}


int main()
{

	
}
