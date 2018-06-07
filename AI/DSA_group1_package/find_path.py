# debug
from AI.DSA_group1_package.package_archieve.find_path_list import find_path
# debug

INF = float("inf")
ROUTE_NUM = 5

'''
这里与外部接口的函数是 path_to
path_to
输入：this_type的取值有如下4种：
    'me_me_fields'：我回自己领地
    'me_enemy_bands'：我到敌人纸带
    'enemy_enemy_fields'：敌人回自己领地
    'enemy_me_bands'：敌人到我的纸带
输出：
    是线面两种情况中的一个，但是不管怎么样，都输出一个list，其中至少有一个tupple。
'''


def path_to(stat, storage, this_type):  # 如果算过path_to了，就不算了，如果没算过，就接着算。

    me_id = stat['now']['me']['id']
    enemy_id = stat['now']['enemy']['id']

    outcome = None  # 如果到最后outcome还是None，说明没算出来，程序有bug。
    if this_type == 'me_me_fields':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, me_id, me_id, 'fields', ROUTE_NUM)
    elif this_type == 'enemy_enemy_fields':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, enemy_id, enemy_id, 'fields', ROUTE_NUM)
    elif this_type == 'me_enemy_bands':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = clipped_find_path(stat, storage, me_id)
            if outcome is None:
                outcome = find_path(stat, storage, me_id, enemy_id, 'bands', ROUTE_NUM)
    elif this_type == 'enemy_me_bands':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = clipped_find_path(stat, storage, enemy_id)
            if outcome is None:
                outcome = find_path(stat, storage, me_id, enemy_id, 'bands', ROUTE_NUM)

    return outcome


'''
clipped_find_path 是find_path的剪枝版本, 目前只能处理bands的剪枝
输入：
    - start 是起始的点的id (我的头或者enermy的头)，
    - target 是目标对应的id
输出：
    - 如果可以剪枝，那么返回如下
        一个list，其中只有一个tuple
        - shortest_dist 是一个int返回最短路径的长度
        - route_list = 'clipped'
        - target_point 是一个点的坐标（x, y），表示这条路径达到的目标点
    - 返回值特殊情况 
        1. 无路可走，或者说是找不到。
        shortest_dist = INF
        route_list = None
        target = None
    - 如果暂时不能剪枝，返回 None
复杂度：
    如果自己纸带长度m，对方纸带长度n，复杂度O(n * m)
'''


def clipped_find_path(stat, storage, start_id):
    # 确定起始点，起始纸带和目标纸带
    if start_id == stat['now']['me']['id']:
        start_x = stat['now']['me']['x']
        start_y = stat['now']['me']['y']
        start_bands = storage['bands']['me']
        target_bands = storage['bands']['enemy']
    else:
        start_x = stat['now']['enemy']['x']
        start_y = stat['now']['enemy']['y']
        start_bands = storage['bands']['enemy']
        target_bands = storage['bands']['me']

    # 寻找离自己距离最近的纸带上的点
    target_x = None
    target_y = None
    min_dist = INF
    for i in range(0, len(target_bands)):  # 此处包括对方的头，对方头下一回合变成纸带
        px = target_bands[i][0]
        py = target_bands[i][1]
        temp = abs(start_x - px) + abs(start_y - py)
        if temp < min_dist:
            min_dist = temp
            target_x = px
            target_y = py
    if min_dist == INF:  # 说明没有对方的纸带，这时候直接返回找不到
        outcome = (INF, None, None)
        return outcome

    # 看看有几个自己的纸带在所形成的方格之内
    count = 0
    for j in range(len(start_bands) - 2, -1, -1):
        # 此处不包括自己的head，并且从后往前找，越是后面的，月容易堵自己。
        if start_x <= start_bands[j][0] <= target_x \
                and start_y <= start_bands[j][1] <= target_y:
            # 如果自己纸带在两方的head行程的rectangular中，++
            count += 1
            if count >= 3:
                break

    # 判断是否能够使用剪枝，并且根据情况计算返回值
    def sgn(x, y):
        if x > y:
            return 1
        else:
            return -1

    outcome = None
    min_abs = min(abs(start_x - target_x), abs(start_y - target_y))
    if min_abs == 0:  # 在一条直线上
        if count == 0:  # rectangular中有0个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', (target_x, target_y))
    elif min_abs == 1:  # 错开一格
        if count <= 1:  # rectangular中有0-1个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', (target_x, target_y))
    else:  # 至少错开两格
        '''如果有dead_check，这里可以剪枝更多，考虑到count = 3的情况，待定。'''
        if count <= 1:  # rectangular中有0-1个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', (target_x, target_y))
        elif count == 2:
            dx = sgn(target_x, start_x)
            dy = sgn(target_y, start_y)
            point_dx = (start_x + dx, start_y)
            point_dy = (start_x, start_y + dy)
            if stat['now']['bands'][point_dx[0]][point_dx[1]] != start_id \
                    or stat['now']['bands'][point_dy[0]][point_dy[1]] != start_id:
                # 如果朝向目标的两边的相邻两格，至少有一个不是我的纸带，那么可以剪枝
                outcome = (min_dist, 'clipped', (target_x, target_y))

    return outcome


'''
find_path
输入参数定义如下：
    - start 是起始的点的id (我的头或者enermy的头)，
    - target 是目标对应的id
    - this_type 指区域或者纸带，区域为'field'，纸带为'bands'
    - route_num 要找到最短路径的条数，尽可能找到的最短路径的条数。最后返回的tuple长度可能小于route_num
返回值定义：
    - 待定返回一个3元tuple组成的list[(shortest_dist, route_list, target_point)]
    - 其中每找到的一个最短路径构成一个tuple, tuple的排列顺序按照路径长度依次递增
        - shortest_dist 是一个int返回最短路径的长度
        - route_list 是一个（x, y）坐标的 list，表示从start开始（不包含）到一个target中的一个点（包含）的路径
        - target_point 是一个点的坐标（x, y），表示这条路径达到的目标点
    返回值特殊情况：
    1. 无路可走，或者说是找不到。
        shortest_dist = INF
        route_list = None
        target = None
    2. 已经到达返回['dis']为0的字典(无其他key)
        shortest_dist = 0
        route_list = None
        target = start(x, y)（开始点坐标）
'''


# def find_path(stat, storage, start, target, this_type, route_num):
#
#     return 0
