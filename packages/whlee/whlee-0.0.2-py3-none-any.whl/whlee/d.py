import itertools, collections
import numpy as np

class dictee(dict):
    """
    反转时行为
    ----------
    要求 value 可 hash。否则请用 invert_unhashable。
    value 重复时合并，取最后出现的 key。np.nan 重复也会合并。
    输出类型仍是 idict。

    固化顺序
    --------
    输出为嵌套元组

    example
    -------
    vd = idict(name='Allen', age=np.nan, gender='male', gende=np.nan) 
    vd.invert
    vd.invert_unhashable
    vd.preserve
    vd.invert.preserve
    vd.invert_unhashable.preserve
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    @property
    def invert(self):
        return self.__class__({v: k for k, v in self.items()})
    @property
    def invert_unhashable(self):
        return self.__class__({str(v): k for k, v in self.items()})
    @property
    def preserve(self):
        return tuple(self.items())
