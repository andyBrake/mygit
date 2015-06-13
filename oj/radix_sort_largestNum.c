#include <stdlib.h>
#include <stdio.h>
#include <string.h>



typedef unsigned char byte;

void numToDigits(int num, byte digits[]) {
    static int num_stack[32];
    int top = -1;
    int i = 1;

    if (num == 0) {
        digits[0] = 1;
        return;
    }

    while (num) {
        num_stack[++top] = num % 10;
        num /= 10;  
    }

    digits[0] = top+1;

    while (top > -1) {
        digits[i++] = num_stack[top--]; 
    }
}

/* 
 * num[x] 表示一个数的各位数字数组
 * n 表示有多少个数
 * digit用于递归，表示第几位
 * lenmax表示数字最长有多少位
 * */
void radixSort(byte **num, int n, int digit, int len_max) {
    byte *tmp[n];

    int count[10], count2[10];
    int i, k;

    memset(count, 0, sizeof(count));
    memset(count2, 0, sizeof(count2));

    for (i = 0; i < n; ++ i) {
        k = num[i][0];  /* k表示这个数字有多少位 */

        if (digit > k)/* 比如12扩展成为1212 */
            num[i][digit] = num[i][digit%k? digit%k: k];

		/* k这里又表示数字num［i］的第digit位 */
        k = num[i][digit];

        ++count[k];
        ++count2[k];
    }


    for (i = 1; i < 10; ++ i) {
        count[i] += count[i-1];
        count2[i] += count2[i-1];
    }

    for (i = n-1; i >= 0; -- i) 
	{
        k = num[i][digit];

        tmp[count[k]-1] = num[i];
		
        --count[k];
    }

    for (i = 0; i < n; ++ i)
   	{
        num[i] = tmp[i];
    }

// recursive
    if (count2[0] > 0 && digit <= len_max)
   ｛
        radixSort(num, count2[0], digit+1, len_max);
	｝

    for (i = 1; i < 10; ++ i) 
	{
        if (count2[i] > count2[i-1] + 1 && digit <= len_max) {
            radixSort(num+count2[i-1], count2[i]-count2[i-1], digit+1, len_max);
        }
    }
}

char *largestNumber(int *num, int n) {
    int i, j, length, len_max;
    char *result, *p;

    byte *digits[n];

    length = 0;
    len_max = 0;
	/* revert each number to digits */
    for (i = 0; i < n; ++ i) {
        digits[i] = (byte*)malloc(sizeof(byte)*32);
        memset(digits[i], 0, sizeof(byte)*32);
        numToDigits(num[i], digits[i]);
        len_max = len_max > digits[i][0]? len_max: digits[i][0];
        length += digits[i][0];
    }

	/* start to sort */
    radixSort(digits, n, 1, len_max);

    result = (char*)malloc(sizeof(char)*(length+1));
    p = result;

    for (i = n-1; i >= 0; -- i) 
	{
        for (j = 1; j <= digits[i][0]; ++ j)
            *p++ = digits[i][j] + '0';
    }
    *p = '\0';

    for (i = 0; i < n; ++ i) 
	{
        free(digits[i]);
    }
    if (*result == '0') *(result+1) = '\0'; 
    return result;
}


int main()
{
	int test[] = {3, 2, 1};
	char * p;

	p = largestNumber(test, sizeof(test)/sizeof(int));
	printf("result is : %s\n", p);

	return 0;
}
