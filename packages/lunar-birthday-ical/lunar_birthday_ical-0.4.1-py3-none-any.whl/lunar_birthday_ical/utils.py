from collections import deque
from collections.abc import Mapping


def deep_merge(d1, d2):
    merged = d1.copy()  # 复制 d1 以免修改原字典
    for k, v in d2.items():
        if isinstance(v, Mapping) and k in merged and isinstance(merged[k], Mapping):
            merged[k] = deep_merge(merged[k], v)  # 递归合并
        else:
            merged[k] = v  # 直接覆盖
    return merged


def deep_merge_iterative(d1, d2):
    merged = d1.copy()  # 复制 d1 以免修改原字典
    stack = deque([(merged, d2)])  # 使用 deque 作为堆栈, 存储要合并的字典对

    while stack:
        current_d1, current_d2 = stack.pop()  # 取出一对字典

        for k, v in current_d2.items():
            if (
                isinstance(v, Mapping)
                and k in current_d1
                and isinstance(current_d1[k], Mapping)
            ):
                # 如果两个字典的该键都是字典, 则推入栈中, 等待后续合并
                stack.append((current_d1[k], v))
            else:
                # 否则, 直接更新
                current_d1[k] = v

    return merged
