
# index_dict = [{}] * 10
#
# for api in data[1:]:
#     request_url = self.extractor.search_lazy(api)['url']
#     url_list = _get_url_path(request_url)[1:].split('/')
#     for index, value in enumerate(url_list):
#         try:
#             dict_ = index_dict[index]
#         except IndexError:
#             break
#         times = dict_.get(value, 0)
#         if times > 0:
#             dict_[value] = times + 1
#         else:
#             dict_[value] = 1
#
#
# # 统计所有url 每个子路径 不重复的数量
# len_list = []
# for dict_ in index_dict:
#     len_list.append(len(dict_))
#
# # 收集len_list每项和前一项的差值
# prev = 0
# difference_list = []
# for num in len_list:
#     difference_list.append(num - prev)
#     prev = num
#
# # 找到difference_list 中最大的值和他所在在位置
# index = difference_list.index(max(difference_list))
import random
from functools import lru_cache


@lru_cache()
def test_cache(a=1, b=2):
    return a+b


def log(text="ada"):
    def decorator(func):

        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper
    return decorator


@log()
def now():
    print('2015-3-25')


def gen_randoms():
    r = []
    for _ in range(100):
        r.append(random.randint(1, 1000))
    return r


if __name__ == '__main__':
    result = test_cache(2, 3)
    result2 = test_cache(2, 3)
    print(result)
    print(result2)
    print(test_cache.cache_info().hits)

    now()
