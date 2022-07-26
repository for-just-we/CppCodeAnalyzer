#include "std_testcase.h"

#include <wchar.h>

#ifndef OMITBAD

void CWE122_Heap_Based_Buffer_Overflow__c_CWE805_char_loop_15_bad()
{
    char * data;
    data = NULL;
    switch(6)
    {
    case 6:
        /* FLAW: Allocate and point data to a small buffer that is smaller than the large buffer used in the sinks */
        data = (char *)malloc(50*sizeof(char));
        if (data == NULL) {exit(-1);}
        data[0] = '\0'; /* null terminate */
        break;
    default:
        /* INCIDENTAL: CWE 561 Dead Code, the code below will never run */
        printLine("Benign, fixed string");
        break;
    }
    {
        size_t i;
        char source[100];
        memset(source, 'C', 100-1); /* fill with 'C's */
        source[100-1] = '\0'; /* null terminate */
        /* POTENTIAL FLAW: Possible buffer overflow if source is larger than data */
        for (i = 0; i < 100; i++)
        {
            data[i] = source[i];
        }
        data[100-1] = '\0'; /* Ensure the destination buffer is null terminated */
        printLine(data);
        free(data);
    }
}

#endif /* OMITBAD */

#ifndef OMITGOOD

/* goodG2B1() - use goodsource and badsink by changing the switch to switch(5) */
static void goodG2B1()
{
    char * data;
    data = NULL;
    switch(5)
    {
    case 6:
        /* INCIDENTAL: CWE 561 Dead Code, the code below will never run */
        printLine("Benign, fixed string");
        break;
    default:
        /* FIX: Allocate and point data to a large buffer that is at least as large as the large buffer used in the sink */
        data = (char *)malloc(100*sizeof(char));
        if (data == NULL) {exit(-1);}
        data[0] = '\0'; /* null terminate */
        break;
    }
    {
        size_t i;
        char source[100];
        memset(source, 'C', 100-1); /* fill with 'C's */
        source[100-1] = '\0'; /* null terminate */
        /* POTENTIAL FLAW: Possible buffer overflow if source is larger than data */
        for (i = 0; i < 100; i++)
        {
            data[i] = source[i];
        }
        data[100-1] = '\0'; /* Ensure the destination buffer is null terminated */
        printLine(data);
        free(data);
    }
}

/* goodG2B2() - use goodsource and badsink by reversing the blocks in the switch */
static void goodG2B2()
{
    char * data;
    data = NULL;
    switch(6)
    {
    case 6:
        /* FIX: Allocate and point data to a large buffer that is at least as large as the large buffer used in the sink */
        data = (char *)malloc(100*sizeof(char));
        if (data == NULL) {exit(-1);}
        data[0] = '\0'; /* null terminate */
        break;
    default:
        /* INCIDENTAL: CWE 561 Dead Code, the code below will never run */
        printLine("Benign, fixed string");
        break;
    }
    {
        size_t i;
        char source[100];
        memset(source, 'C', 100-1); /* fill with 'C's */
        source[100-1] = '\0'; /* null terminate */
        /* POTENTIAL FLAW: Possible buffer overflow if source is larger than data */
        for (i = 0; i < 100; i++)
        {
            data[i] = source[i];
        }
        data[100-1] = '\0'; /* Ensure the destination buffer is null terminated */
        printLine(data);
        free(data);
    }
}

void CWE122_Heap_Based_Buffer_Overflow__c_CWE805_char_loop_15_good()
{
    goodG2B1();
    goodG2B2();
}

#endif /* OMITGOOD */

/* Below is the main(). It is only used when building this testcase on
 * its own for testing or for building a binary to use in testing binary
 * analysis tools. It is not used when compiling all the testcases as one
 * application, which is how source code analysis tools are tested.
 */

#ifdef INCLUDEMAIN

int main(int argc, char * argv[])
{
    /* seed randomness */
    srand( (unsigned)time(NULL) );
#ifndef OMITGOOD
    printLine("Calling good()...");
    CWE122_Heap_Based_Buffer_Overflow__c_CWE805_char_loop_15_good();
    printLine("Finished good()");
#endif /* OMITGOOD */
#ifndef OMITBAD
    printLine("Calling bad()...");
    CWE122_Heap_Based_Buffer_Overflow__c_CWE805_char_loop_15_bad();
    printLine("Finished bad()");
#endif /* OMITBAD */
    return 0;
}