
# BM 算法 基本原理
"""
模式串和主串的匹配过程，看作模式串在主串中不停地往后滑动。

坏后缀规则
倒叙比较模式串中的字符， 如果比较发现字符不同， 这个不同字符在模式串下标为J，判断主串中的这个值是否在模式串中，
如果不在 则移动J+1
如果在，则直接对齐模式串（查找这个值在模式串中的下标i）移动位置 j - i

问题：计算得到的往后滑动的位数，有可能是负数的情况。

好后缀规则
倒叙比较模式串中的字符，找到后缀连续匹配的字符， 如果这段连续的字符串，在模式串还存在，则对齐位置。
如果不存在， 则移动Len(模式串)

问题：
但是如果这段连续的字符串 在主串中有部分重合的时候，并且重合的部分相等的时候，就有可能移动过多

所以：
如果不存在， 则找到模式串最长 能和连续字符串子串匹配的位置，移动到这个位置


如何选择用好后缀规则还是坏字符规则
我们可以分别计算好后缀和坏字符往后滑动的位数，
然后取两个数中最大的，作为模式串往后滑动的位数。
这种处理方法还可以避免我们前面提到的，根据坏字符规则，计算得到的往后滑动的位数，有可能是负数的情况。
"""
