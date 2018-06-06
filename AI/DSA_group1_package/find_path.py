__doc__ = '''
这里与外部接口的函数是path_to
    type的取值有如下4种：
    'me_me_fields'：我回自己领地
    'me_enermy_bands'：我到敌人纸袋
    'enermy_enermy_fields'：敌人回自己领地
    'enermy_me_bands'：敌人到我的纸袋

find_path的参数定义如下：
    - start 是起始的点的id (我的头或者enermy的头)，
    - target 是目标对应的id
    - type 指区域或者纸带，区域为1，纸带为0
    - route_num 要找到最短路径的条数，尽可能找到的最短路径的条数。最后返回的tuple长度可能小于route_num
返回值定义：
    - 待定返回一个3元tuple组成的list[(shortest_dist, route_list, target_point)]
    - 其中每找到的一个最短路径构成一个tuple, tuple的排列顺序按照路径长度依次递增
        - shortest_dist 是一个int返回最短路径的长度
        - route_list 是一个（x, y）坐标的 list，表示从start开始（不包含）到一个target中的一个点（包含）的路径
        - target_point 是一个点的坐标（x, y），表示这条路径达到的目标点
    返回值特殊情况：
    1. 无路可走
        shortest_dist = INF
        route_list = None
        target = None
    2. 已经到达返回['dis']为0的字典(无其他key)
        shortest_dist = 0
        route_list = None
        target = start(x, y)（开始点坐标）
'''

INF = float("inf")


def path_to(stat, storage, type):

    return 0


def find_path(stat, storage, start, target, type, route_num):

    return 0

