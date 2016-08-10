#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
//#include <file.h>

#define LOG_NAME  "logfile.txt"
#define MW_TRACE_BUFFER  (1024)

typedef struct tagLog
{
	FILE *p; /* log file pointer */
	char tempBuf[MW_TRACE_BUFFER];

	int (*initLog)(struct tagLog *self);
	int (*writeLog)(struct tagLog *self, const char *format, ...);
}Log;

int initLog(Log *self);
int writeLog(Log *self, const char *format, ...);

int initLog(Log *self)
{
	FILE *p = NULL;
	p = fopen(LOG_NAME, "a");
	if (NULL == p)
	{
		return -1;
	}
	self->p = p;
	memset(self->tempBuf, 0, sizeof(self->tempBuf));
	self->initLog = initLog;
	self->writeLog = writeLog;

	return 0;
}
 

int writeLog(Log *self, const char *format, ...)
{
	va_list mark;
	int tot;
	int oflow = 0;

	va_start(mark, format);
    tot = vsprintf(self->tempBuf, format, mark);
    va_end(mark);

    if(tot >= MW_TRACE_BUFFER) 
	{ 
		self->tempBuf[MW_TRACE_BUFFER - 1] = 0; 
		oflow = 1;	
	}

    for(tot=0; self->tempBuf[tot];tot++)
	{
		fputc(self->tempBuf[tot], self->p);
	}

	return oflow;
}


int main()
{
	Log log;
	int ret;

	ret = initLog(&log);
	printf("init log ret %d\n", ret);
	log.writeLog(&log,"input %d, %d, %c, %s.", 2,1,'t', "end");

	return 0;
}
