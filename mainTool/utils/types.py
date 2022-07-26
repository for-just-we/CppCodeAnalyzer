from enum import IntEnum, Enum

# label类别: goto label, case label, default
class LabelType(IntEnum):
    Normal = 1
    Case = 2
    Default = 3

# 类定义类型
class ClassType(IntEnum):
    Class = 1  # 类
    Struct = 2 # 结构体
    Enum = 3 # 枚举
    Union = 4 # 联合体

# CFG边类型
class CFGEdgeType:
    EMPTY_LABEL = ""
    TRUE_LABEL = "True"
    FALSE_LABEL = "False"