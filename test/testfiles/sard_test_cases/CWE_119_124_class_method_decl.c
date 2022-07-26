#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE124_Buffer_Underwrite__char_alloca_memmove_82.h"

namespace CWE124_Buffer_Underwrite__char_alloca_memmove_82
{

void CWE124_Buffer_Underwrite__char_alloca_memmove_82_bad::action(char * data = NULL)
{
    {
        char source[100];
        memset(source, 'C', 100-1); /* fill with 'C's */
        source[100-1] = '\0'; /* null terminate */
        /* POTENTIAL FLAW: Possibly copying data to memory before the destination buffer */
        memmove(data, source, 100*sizeof(char));
        /* Ensure the destination buffer is null terminated */
        data[100-1] = '\0';
        printLine(data);
    }
}

}