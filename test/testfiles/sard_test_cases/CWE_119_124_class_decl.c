#include "std_testcase.h"

#include <wchar.h>

namespace CWE124_Buffer_Underwrite__char_alloca_memmove_82
{

class CWE124_Buffer_Underwrite__char_alloca_memmove_82_base
{
public:
    /* pure virtual function */
    virtual void action(char * data) = 0;
};

#ifndef OMITBAD

class CWE124_Buffer_Underwrite__char_alloca_memmove_82_bad : public CWE124_Buffer_Underwrite__char_alloca_memmove_82_base
{
public:
    void action(char * data);
};

#endif /* OMITBAD */

#ifndef OMITGOOD

class CWE124_Buffer_Underwrite__char_alloca_memmove_82_goodG2B : public CWE124_Buffer_Underwrite__char_alloca_memmove_82_base
{
public:
    void action(char * data);
};

#endif /* OMITGOOD */

}