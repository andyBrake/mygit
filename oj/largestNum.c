#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void dispatchNum(int num, char *str, int *radix)
{
	int i = 0;

	if (0 == num)
	{
		//printf(" get zero\n");
		str[0] = 0;
		*radix = 1;

		return;
	}

	while(num != 0)
	{
		str[i++] = num%10;
		num = num/10;
	}

	*radix = i;
}

/* aRadix must larger than bRadix */
int handleRestPart(int aRadix, char *str4a, int bRadix, char *str4b)
{
	int tempA, tempB;
	int i = 0, j = 0;

	tempA = str4a[aRadix - bRadix - 1];
	//tempB = str4b[bRadix - 1];
	tempB = str4a[aRadix - 1];

	do
	{
		if (tempB < tempA) 
		{
			return 1;
		}
		else if(tempA == tempB) 
		{
			i++;
			if (aRadix - bRadix - i -1 < 0)
			{
				if (aRadix - 1 - j < 0)
				{
					return 0;
				}

				tempA = str4a[aRadix - 1 - j];
				tempB = str4a[aRadix - 2 - j];
				j++;
				continue;
			}
			else
			{
				tempA = str4a[aRadix - bRadix - i -1];
				tempB = str4a[aRadix - i - 1];
			}
		}
		else
		{
			return 0;
		}
	}while(1);

	return 0;
}

/* if a radix larger than b, return true, else false */
int isLarger(int a, int b)
{
	int aRadix, bRadix, minRadix;
	char str4a[32] = {0};
	char str4b[32] = {0};
	int i = 0;

	if (b < 0)
	{
		return 1;
	}

	dispatchNum(a, str4a, &aRadix);
	dispatchNum(b, str4b, &bRadix);

	minRadix = aRadix < bRadix ? aRadix : bRadix;

	while(minRadix != 0)
	{
		if (str4a[aRadix - 1 - i] > str4b[bRadix - 1 - i])
		{
			return 1;
		}	
		else if (str4a[aRadix - 1 - i] < str4b[bRadix - 1 - i])
		{
			return 0;
		}

		minRadix--;
		i++;
	}
	/* 走到这里说明前面等长的部分完全相同 */

	if (aRadix == bRadix)
	{
		return 0;
	}

	if (aRadix > bRadix)
	{
		return handleRestPart(aRadix, str4a, bRadix, str4b);
	}

	if (aRadix < bRadix)
	{
		i = handleRestPart(bRadix, str4b, aRadix, str4a);
		if (0 == i)
		{
			return 1;
		}
		return 0;
	}

	return 0;
}

int getLargestElement(int * nums, int * flag, int arrSize)
{
	int i;
	int max = -1;
	int index4Max = -1;

	for (i = 0; i<arrSize; i++)
	{
		if (flag[i] != 0)
		{
			continue;
		}

		if (isLarger(nums[i], max))
		{
			max = nums[i];
		    index4Max = i;	
		}
	}

	if (index4Max < 0)
	{
		printf("\nfatal error!\n");
		return 0;
	}

	//printf("index is %d, %d.\n", index4Max, max);

	flag[index4Max] = 1;
	return max;
}


char* largestNumber(int* nums, int numsSize) {
	int i;
    int *flag;
	char *outRes = NULL; /* output string */
    char str[32]; /* element to string */
    int temp;     /* element int */
    int total = numsSize;

    if (numsSize <= 0)
    {
        return NULL;
    }
  
    flag = (int *)malloc(sizeof(int) * numsSize);
    if (NULL == flag)
    {
        return NULL;
    }    
    memset(flag, 0, sizeof(int) * numsSize);
  
    outRes = (char *)malloc(1024);
    if (NULL == outRes)
    {
  	    return NULL;
    }
	outRes[0] = '\0';
  
	while (total != 0)
	{
		/* get largest element */
	    temp = getLargestElement(nums, flag, numsSize);
		total--;
			
		memset(str, 0, sizeof(str));
		sprintf(str, "%d", temp);		
		strcat(outRes, str);
		//printf("stelen : %lu\n", strlen(outRes));
	}

	if ('0' == outRes[0])
	{
		outRes[1] = '\0';
	}
  
	return outRes;
}


int main()
{
	int i = 0;
	int cmp;
	//int testNum[] = {999999998, 999999997, 999999999};
	//int testNum[] = {830, 8308};
	//int testNum[] = {4704,6306,9385,7536,3462,4798,5422,5529,8070,6241,9094,7846,663,6221,216,6758,8353,3650,3836,8183,3516,5909,6744,1548,5712,2281,3664,7100,6698,7321,4980,8937,3163,5784,3298,9890,1090,7605,1380,1147,1495,3699,9448,5208,9456,3846,3567,6856,2000,3575,7205,2697,5972,7471,1763,1143,1417,6038,2313,6554,9026,8107,9827,7982,9685,3905,8939,1048,282,7423,6327,2970,4453,5460,3399,9533,914,3932,192,3084,6806,273,4283,2060,5682,2,2362,4812,7032,810,2465,6511,213,2362,3021,2745,3636,6265,1518,8398};

	//char rel[] = "98909827968595339456944893859149094902689398937839883538183810810780707982784676057536747174237321720571007032685668066758674466986636554651163276306626562416221603859725909578457125682552954605422520849804812479847044453428339323905384638363699366436503636357535673516346233993298316330843021297028227452732697246523622362231322   281  216213206020001921763154815181495141713801147114310901048";
//	char exp[] = "98909827968595339456944893859149094902689398937839883538183810810780707982784676057536747174237321720571007032685668066758674466986636554651163276306626562416221603859725909578457125682552954605422520849804812479847044453428339323905384638363699366436503636357535673516346233993298316330843021297028227452732697246523622362231322812216213206020001921763154815181495141713801147114310901048";


	int testNum[] = {9051,5526,2264,5041,1630,5906,6787,8382,4662,4532,6804,4710,4542,2116,7219,8701,8308,957,8775,4822,396,8995,8597,2304,8902,830,8591,5828,9642,7100,3976,5565,5490,1613,5731,8052,8985,2623,6325,3723,5224,8274,4787,6310,3393,78,3288,7584,7440,5752,351,4555,7265,9959,3866,9854,2709,5817,7272,43,1014,7527,3946,4289,1272,5213,710,1603,2436,8823,5228,2581,771,3700,2109,5638,3402,3910,871,5441,6861,9556,1089,4088,2788,9632,6822,6145,5137,236,683,2869,9525,8161,8374,2439,6028,7813,6406,7519};
	char rel[] = 	"995998549642963295795569525905189958985890288238775871870185978591838283748308308827481618052787813771758475277519744072727265721971071006861683682268046787640663256310614560285906582858175752573156385565552654905441522852245213513750414822478747104662455545424532434289408839763963946391038663723370035134023393328828692788270926232581243924362362304226421162109163016131603127210891014";
	char exp[] =    "995998549642963295795569525905189958985890288238775871870185978591838283748308830827481618052787813771758475277519744072727265721971071006861683682268046787640663256310614560285906582858175752573156385565552654905441522852245213513750414822478747104662455545424532434289408839763963946391038663723370035134023393328828692788270926232581243924362362304226421162109163016131603127210891014";




	char *out = NULL;
	//printf("num is %lu\n", sizeof(testNum)/sizeof(int));
	out = largestNumber(testNum, sizeof(testNum)/sizeof(int));

	printf("\nout is %s.\nstrlen is %lu.\n", out, strlen(out));	
//#if 0	
	cmp = strcmp(out, exp);
	if (0 != cmp)
	{
		printf("\n----------------------------ok, cmp %d.\n", cmp);
	}

	while(exp[i] != '\0')
	{
		if (out[i] != exp[i])
		{
			printf("index %d is not same. %c : %c \n", i, out[i], exp[i]);
		}
		i++;
	}
//#endif
//	printf("\nnot find dif, i = %d \n", i);
	return 0;
}
