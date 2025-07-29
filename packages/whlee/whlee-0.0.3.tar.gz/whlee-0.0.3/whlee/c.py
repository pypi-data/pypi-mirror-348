import itertools, collections
import numpy as np

def counteree(data):
    """
    description
    -----------
    collections.Counter 计算纯数字的pd.Series时，会出现np.nan无法合并统计。
    """
    data_list = []
    for i in data:
        if isinstance(i, float) and np.isnan(i):  # np.isnan just 只能判断数值，且对于np.array会广播，所以要限制类型。
            data_list.append(np.nan)
        else:
            data_list.append(i)
    return collections.Counter(data_list)


# _______________________________________________________________________


def chainee(datas):
    """
    description
    -----------
    原始chain只能处理iterable对象，这里可以自动将非iterable对象放入列表，然后进行chain。
    """
    dt = [x if isinstance(x, collections.Iterable) else [x] for x in datas]
    rst = itertools.chain(*dt)
    return rst
