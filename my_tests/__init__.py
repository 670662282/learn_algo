
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
