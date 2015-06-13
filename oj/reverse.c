#include "stdio.h"
#include <stdlib.h>


struct ListNode {
  int val;
  struct ListNode *next;
};

 
struct ListNode *reverseKGroup(struct ListNode *head, int k) {
    struct ListNode *start,*end;
    struct ListNode *tempNode = NULL, *retList = NULL;
    struct ListNode *first, *mid, *last, *tempStart, *tempEnd;
    struct ListNode * tail, *ret;
	int cnt = 0;

    ret = head;
    cnt = 0;

	if (k <= 1)
        return head;
    /* while k=1, the while loop will unbreak */
    while(head != NULL)
    {
    	start = head;  
        cnt = 0;
		
        /* get the reverse cycle */
        while(head != NULL && cnt != k)
        {
            end = head; /* now, end is head pre node */
            head = head->next;
            cnt++;
        }
        /* run to the tail of list */
        if (cnt < k)
        {
            break;
        }

        /* reverse start to end */
        tempStart = start;
        tempEnd = end;
            
        tail = end->next;
                					    
        for (first = start, mid = start->next, last = mid->next;
             last != tail;
             first = mid, mid = last, last = last->next)
    	{
             mid->next = first;
    	}
        end->next = first;
        start->next = last;
        ret =  end;

        start = tempStart;
        end = tempEnd;
        			  

        if (retList != NULL)
        {
            tempNode->next = ret;
        }
        else
        {
            retList =  ret;
        }

        if (end != NULL)
        {
            tempNode = start;
        }
    }
	
	/* return the reversed list */
    if (NULL == retList)
    {
        return ret;
    }
    return retList;
}

struct ListNode * createList(int nodeCnt)
{
    /* from 0 to nodeCnt */
    int i;
    struct ListNode * node, *headNode, *lastNode;

    headNode = (struct ListNode *)malloc(sizeof(struct ListNode));
    memset(headNode, 0, sizeof(struct ListNode));

    lastNode= headNode;
    lastNode->val = 0;

    for(i=1; i<nodeCnt; i++)
    {
        node = (struct ListNode *)malloc(sizeof(struct ListNode));
        memset(node, 0, sizeof(struct ListNode));
        node->val = i;

        lastNode->next = node;

        lastNode = node;
    }

    return headNode;
}


void display(struct ListNode * list)
{
	printf("\n{");
	while(list != NULL)
	{
		printf("%d, ", list->val);
		list = list->next;
	}
	printf("}\n");

}

int main()
{
    struct ListNode * list, *output;

    list = createList(8);
	display(list);
	
	output = reverseKGroup(list, 1);
	display(output);
    
	printf("\nexit\n");
	getchar();
    return 0;
}
