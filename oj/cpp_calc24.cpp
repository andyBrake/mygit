//
//  cpp_calc24.cpp
//  calc24
//
//  Created by huangfa on 16/8/9.
//  Copyright (c) 2016年 huangfa. All rights reserved.
//

#include <stdio.h>
#include <vector>
#include <string>
#include "cpp_calc24.h"
#include <stack>

using namespace std;


double g_num[4] = {10,8,12,6};//{1,5,8,6};//{1,5,5,5};//{10,10,4,4};//{3, 5, 7, 2};//{10,8,12,6}; {1,5,8,6}
int g_flag[4] = {0, 0, 0, 0};

vector<string> g_calcStepString;
stack<string>  g_step;

CALC_TYPE_E g_calc[4] = {CALC_ADD, CALC_SUB, CALC_MUL, CALC_DIV};

int getNextNum(INFO_S *info, int startIndex)
{
    int i;
    
    for (i=startIndex; i<4; i++)
    {
        if (0 == g_flag[i])
        {
            g_flag[i] = 1;
            return i;
        }
    }
    
    return -1;
}

/* 获取下一个运算符号 */
int getNextCalcType(INFO_S *info, int startIndex)
{
    int i;
    
    for (i=startIndex; i<4; i++)
    {
        if (0 == info->usedFlag[info->curIndex][i])
        {
            info->usedFlag[info->curIndex][i] = 1;
            return i;
        }
    }
    //printf("curIndex %d, can't find calcType.\n", info->curIndex);
    
    return -1;
}

//type 0 : num ; 1:calc type
/* 获取下一个操作元素，数字或者运算符 */
int getNextElemIndex(INFO_S *info, int *type, int startIndex)
{
    int index;
    
    if (info->curIndex >= FINISH_INDEX)
    {
        return -1;
    }
    
    if (startIndex >= 4)
    {
        return -1;
    }
    
    if (info->curIndex % 2 == 0)
    {
        index = getNextNum(info, startIndex);
        if (index < 0)
        {
            return index;
        }
        //printf("get next num %d, curIndex %d.\n", g_num[index], info->curIndex);
        *type = 0;
        return index;
    }
    
    index = getNextCalcType(info, startIndex);
    if (index < 0)
    {
        return index;
    }
    //printf("get next calcType %d, curIndex %d.\n\n", g_calc[index], info->curIndex);
    
    *type = 1;
    return index;
}

double calc(double left, double right, int calcType)
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
    
    //printf("updateinfo : curIndex %d, leftVal %d, curCalcType %d\n", info->curIndex, info->leftVal, info->curCalcType);
}

void backInfo(INFO_S *info, int index, int type)
{
    /* 刚刚用的数字则将数字标记为未使用 */
    if (0 == type)
    {
        g_flag[index] = 0;
        info->curIndex--;
        
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

void refreshCalcType(INFO_S *info)
{
    int i;
    
    if (0 == info->curIndex%2)
    {
        return;
    }
    
    for (i=0; i<4; i++)
    {
        info->usedFlag[info->curIndex][i] = 0;
    }
}

void disPlay(INFO_S *info, int index, int type)
{
    char tmpStr[20] = {0};
    
    if (0 == type)
    {
        sprintf(tmpStr, "%f", g_num[index]);
    }
    else
    {
        switch(g_calc[index])
        {
            case 0: sprintf(tmpStr, "%s", "+");
                break;
                
            case 1: sprintf(tmpStr, "%s", "-");
                break;
                
            case 2: sprintf(tmpStr, "%s", "*");
                break;
                
            case 3: sprintf(tmpStr, "%s", "/");
                break;
                
            default:break;
        }
    }
    //strcat(g_calcStepString, tmpStr);
    string strObj(tmpStr);
    g_step.push(strObj);
    return;
    //printf("%d -", info->leftVal);
}

int getResult(INFO_S *info)
{
    int curNumIndex;
    int type = 0;
    int startIndex = 0;
    int ret;
    double lastResult;
    int lastCalcType;
    
    //printf("\n");
    //printf("\n  get result index %d, leftVal %d.\n", info->curIndex, info->leftVal);
    
    if (FINISH_INDEX == info->curIndex)
    {
        if (TARGET_RESULT == info->leftVal)
        {
            return 0;
        }
        //printf("\n\t\terror result: %f\n\n", info->leftVal);
        return -1;
    }
    
    //lastChoseIndex = info->lastIndex ;
    refreshCalcType(info);
    
    while(1)
    {
        curNumIndex = getNextElemIndex(info, &type, startIndex);
        if (curNumIndex < 0)
        {
            return -1;
        }
        
        lastResult = info->leftVal;
        lastCalcType = info->curCalcType;
        
        updataInfo(info, curNumIndex, type);
        
        ret = getResult(info);
        if (0 == ret)
        {
            disPlay(info, curNumIndex, type);
            return 0;
        }
        
        backInfo(info, curNumIndex, type);
        info->leftVal = lastResult;
        info->curCalcType = lastCalcType;
        startIndex = curNumIndex;
        startIndex++;
        
        if (startIndex < 4)
        {
            //printf("try next, curIndex %d, startIndex %d, leftVal %d, curCalcType %d.\n",
            //       info->curIndex, startIndex, info->leftVal, info->curCalcType);
            
            //printf("flag : %d, %d, %d, %d, index : %d.\n", g_flag[0], g_flag[1], g_flag[2], g_flag[3], info->curIndex);
        }
        
    }
    
    
    //type = (info->curIndex % 2 == 0) ? 0 : 1;
    //backInfo(info, lastChoseIndex, type);
    
    //printf("flag : %d, %d, %d, %d, index : %d.\n", g_flag[0], g_flag[1], g_flag[2], g_flag[3], info->curIndex);
    
    
    //return -1;
}

void showCalcStep()
{
    while(!g_step.empty())
    {
        printf(" %s ", g_step.top().c_str());
        g_step.pop();
    }
}

int main()
{
    INFO_S info;
    int ret;
    
    //memset(g_calcStepString, 0, sizeof(g_calcStepString));
    memset(&info, 0, sizeof(INFO_S));
    ret = getResult(&info);
    
    if (0 == ret)
    {
        showCalcStep();
    }
    else
    {
        printf("\nret is %d.\n", ret);
    }
    
    return 0;
}