INF = 99999999

'''
这里与外部接口的函数是 path_to
path_to
输入：this_type的取值有如下4种：
        'me_me_fields'：我回自己领地
        'me_enemy_bands'：我到敌人纸带
        'enemy_enemy_fields'：敌人回自己领地
        'enemy_me_bands'：敌人到我的纸带
    nodes：假想的墙壁。搜索路径是不能走这里。
输出：
    返回一个元组
    元组的第一个元素代表最短距离。最短距离为0说明在目标区域。最短距离为1说明紧挨着目标区域，最短距离为inf说明无法到达最短区域。
    元组的第二个元素是生成的地图。
    元组的第三个元素是最短路径，最后一个点是目标区域上的点
    元组的第四个元素是最短路径的终点。这一点是目标区域上的点，最短路径的终点(x, y),。如果最短距离是inf, 最后一个值是None
'''


def path_to(stat, storage, this_type, nodes=None):  # 如果算过path_to了，就不算了，如果没算过，就接着算。
    me_id = stat['now']['me']['id']
    enemy_id = stat['now']['enemy']['id']
    # print(this_type)
    # print('enemy_id = %d' % enemy_id)
    # print('me_id = %d' % me_id)

    outcome = None  # 如果到最后outcome还是None，说明没算出来，程序有bug。
    if this_type == 'me_me_fields':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, me_id, me_id, 1, nodes)
    elif this_type == 'enemy_enemy_fields':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, enemy_id, enemy_id, 1, nodes)
    elif this_type == 'me_enemy_bands':
        # print('me_enemy_bands is called')
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = clipped_find_path(stat, storage, me_id, nodes)
            if outcome is None:
                outcome = find_path(stat, storage, me_id, enemy_id, 0, nodes)
    elif this_type == 'enemy_me_bands':
        # print('enemy_me_bands is called')
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = clipped_find_path(stat, storage, enemy_id, nodes)
            if outcome is None:
                outcome = find_path(stat, storage, enemy_id, me_id, 0, nodes)
    return outcome

'''
clipped_find_path 是find_path的剪枝版本, 目前只能处理bands的剪枝
输入：
    - start 是起始的点的id (我的头或者enermy的头)，
输出：
    - 如果可以剪枝，那么返回如下
        - 元组的第一个元素代表最短距离。最短距离为0说明在目标区域。最短距离为1说明紧挨着目标区域，最短距离为inf说明无法到达最短区域。
        - 剪枝没有map, 是字符串 'clipped'
        - 剪枝没有路径，是字符串 'clipped'
        - 返回目标区域上的最短路径终点 (x, y), 如果最短距离是inf, 最后一个值是None
    - 如果暂时不能剪枝，不返回tuple，返回 None
复杂度：
    如果自己纸带长度m，对方纸带长度n，复杂度O(n + m)
'''


# 这个函数写完了，上面的path_to还没有写。
def clipped_find_path(stat, storage, start_id, nodes=None):
    # print('clipped_find_path is called')
    # print('start_id = %d' % start_id)
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
    for i in range(0, len(target_bands)):
        # 此处包括对方的头，对方头下一回合变成纸带。如果对方的头在自己领地，那么target_bands是空，不会有bug。
        px = target_bands[i][0]
        py = target_bands[i][1]
        temp = abs(start_x - px) + abs(start_y - py)
        if temp < min_dist:
            min_dist = temp
            target_x = px
            target_y = py
    if nodes is not None:
        # 这里如果nodes不是空的，说明，需要把自己回家的路径当做，别人的头撞自己的墙
        for i in range(0, len(nodes) - 1):  # 最后一步是回家的点，不需要设置成墙。
            px = nodes[i][0]
            py = nodes[i][1]
            temp = abs(start_x - px) + abs(start_y - py)
            if temp < min_dist:
                min_dist = temp
                target_x = px
                target_y = py

    if min_dist == INF:  # 说明没有对方的纸带，这时候直接返回找不到
        outcome = (INF, 'clipped', 'clipped', None)
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
        elif x == y:
            return 0
        else:
            return -1

    outcome = None
    min_abs = min(abs(start_x - target_x), abs(start_y - target_y))
    dx = sgn(target_x, start_x)
    dy = sgn(target_y, start_y)

    # 这里考虑自己的初始方向，可能会变成一堵墙。其实如果真的加了一堵墙，说明上一次在家里，说明现在没有纸带，count=0,现在+1，只对一条直线有影响。
    dx_wall = {1: 2, -1: 0}
    dy_wall = {1: 3, -1: 1}
    this_player = stat['now']['players'][start_id - 1]

    # print('start_id = %d' % start_id)
    # print(this_player)

    this_dirc = this_player['direction']
    if dx != 0:
        wall_dirc = dx_wall[dx]
        if this_dirc == wall_dirc:
            # 有可能count+1了
            point_dx = (start_x + dx, start_y)
            if stat['now']['bands'][point_dx[0]][point_dx[1]] != start_id:  # 如果dx的方向还不是我的纸带，那么多了一堵墙
                count += 1  # 相当于多了一堵墙
    if dy != 0:
        wall_dirc = dy_wall[dy]
        if this_dirc == wall_dirc:
            # 有可能count+1了
            point_dy = (start_x, start_y + dy)
            if stat['now']['bands'][point_dy[0]][point_dy[1]] != start_id: # 如果dy的方向还不是我的纸带，那么多了一堵墙
                count += 1  # 相当于多了一堵墙

    if min_abs == 0:  # 在一条直线上
        if count == 0:  # rectangular中有0个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', 'clipped', (target_x, target_y))
    elif min_abs == 1:  # 错开一格
        if count <= 1:  # rectangular中有0-1个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', 'clipped', (target_x, target_y))
    else:  # 至少错开两格
        '''如果有dead_check，这里可以剪枝更多，考虑到count = 3的情况，待定。'''
        if count <= 1:  # rectangular中有0-1个自己纸带才能坐标相减
            outcome = (min_dist, 'clipped', 'clipped', (target_x, target_y))
        elif count == 2:
            point_dx = (start_x + dx, start_y)
            point_dy = (start_x, start_y + dy)
            if stat['now']['bands'][point_dx[0]][point_dx[1]] != start_id \
                    or stat['now']['bands'][point_dy[0]][point_dy[1]] != start_id:
                # 如果朝向目标的两边的相邻两格，至少有一个不是我的纸带，那么可以剪枝
                outcome = (min_dist, 'clipped', 'clipped', (target_x, target_y))

    return outcome


# stat是状态，me是自己的id，desid是des对应的id，des指区域或者纸带，区域为1，纸带为0
def find_path(stat, storage, me, desid, des, nodes=None):
    import queue
    width = stat['size'][0]                   # 场地的宽
    height = stat['size'][1]                  # 场地的高
    if me == stat['now']['me']['id']:
        x = stat['now']['me']['x']                # 己方头部的位置
        y = stat['now']['me']['y']
        ex = stat['now']['enemy']['x']            # 敌方头部位置
        ey = stat['now']['enemy']['y']
    else:
        ex = stat['now']['me']['x']               # 敌方头部的位置
        ey = stat['now']['me']['y']
        x = stat['now']['enemy']['x']             # 己方头部位置
        y = stat['now']['enemy']['y']

    mymap = []                                # 记录路径状态，以目标区域为递推起点
    try:
        storage['test']
    except KeyError:
        storage['test'] = []
    storage['test'] = []
    try:
        storage['num']
    except KeyError:
        storage['num'] = 0

    class Node:
        def __init__(self, nodex, nodey):
            self.nodex = nodex
            self.nodey = nodey
            self.cmp = 3 * (abs(self.nodex - x) + abs(self.nodey - y)) + mymap[self.nodex][self.nodey]

        def __lt__(self, other):
            return self.cmp < other.cmp

    storage['num'] += 1
    if des:
        if stat['now']['fields'][x][y] == desid:              # 头部在己方区域，且寻找到己方区域的最短路径
            return 0, None, None, None
        aim = 'fields'
        destination = desid
    else:
        aim = 'bands'
        destination = 3 - me

    for i in range(width):
        mymap.append([])
        for j in range(height):
            if stat['now'][aim][i][j] == destination:  # 目标区域0
                mymap[i].append(0)
            elif stat['now']['bands'][i][j] == me:     # 己方纸带-1
                mymap[i].append(-1)
            else:                                      # 空白区域-4
                mymap[i].append(-4)
    mymap[x][y] = -2                                   # 己方头部-2
    if aim == 'bands':                                 # 搜索到纸带的距离，把头部也当作纸带
        mymap[ex][ey] = 0                              # 对方头部0
    if nodes is not None:
        for index in nodes:
            mymap[index[0]][index[1]] = 0


    # 纸带头紧挨着目标区域
    if x > 0 and mymap[x - 1][y] == 0 and stat['now']['players'][me - 1]['direction'] != 0:
        return 1, None, [[x - 1, y]], [x - 1, y]
    if x < width - 1 and mymap[x + 1][y] == 0 and stat['now']['players'][me - 1]['direction'] != 2:
        return 1, None, [[x + 1, y]], [x + 1, y]
    if y > 0 and mymap[x][y - 1] == 0 and stat['now']['players'][me - 1]['direction'] != 1:
        return 1, None, [[x, y - 1]], [x, y - 1]
    if y < height - 1 and mymap[x][y + 1] == 0 and stat['now']['players'][me - 1]['direction'] != 3:
        return 1, None, [[x, y + 1]], [x, y + 1]

    # 以区域边缘为起点开始搜索，纸带头不紧挨目标区域
    start = queue.PriorityQueue()  # 记录搜索的起点
    for i in range(width):
        for j in range(height):
            if mymap[i][j] == 0:
                if (i > 0 and mymap[i-1][j] == -4) or (i < width-1 and mymap[i+1][j] == -4) or \
                        (j > 0 and mymap[i][j-1] == -4) or (j < height-1 and mymap[i][j+1] == -4):
                    start.put(Node(i, j))

    if start.empty():                                    # 没有目标区域，比如没有纸带
        return INF, mymap, None, None

    count = False
    temp = []
    while (not start.empty()) and not count:             # 搜索路径
        current = start.get()
        i = current.nodex
        j = current.nodey
        index = mymap[i][j] + 1
        if i > 0:
            if mymap[i - 1][j] == -4:
                mymap[i - 1][j] = index
                start.put(Node(i - 1, j))
            elif mymap[i - 1][j] == -2:
                count = True
                temp.append([i, j])
                continue
        if i < width - 1:
            if mymap[i + 1][j] == -4:
                mymap[i + 1][j] = index
                start.put(Node(i + 1, j))
            elif mymap[i + 1][j] == -2:
                count = True
                temp.append([i, j])
                continue
        if j > 0:
            if mymap[i][j - 1] == -4:
                mymap[i][j - 1] = index
                start.put(Node(i, j - 1))
            elif mymap[i][j - 1] == -2:
                count = True
                temp.append([i, j])
                continue
        if j < height - 1:
            if mymap[i][j + 1] == -4:
                mymap[i][j + 1] = index
                start.put(Node(i, j + 1))
            elif mymap[i][j + 1] == -2:
                count = True
                temp.append([i, j])
                continue


    if len(temp) != 0:
        # temp是头部周围可以走的坐标
        # 函数从来没有运行到这里
        try:
            storage['test']
        except KeyError:
            storage['test'] = []
        paths = [temp[0]]
        index = mymap[paths[0][0]][paths[0][1]] - 1
        i = paths[0][0]  # 记录起点坐标
        j = paths[0][1]
        while index >= 0:
            if i > 0 and mymap[i - 1][j] == index:
                paths.append([i - 1, j])
                i = i - 1
            elif i < width - 1 and mymap[i + 1][j] == index:
                paths.append([i + 1, j])
                i = i + 1
            elif j > 0 and mymap[i][j - 1] == index:
                paths.append([i, j - 1])
                j = j - 1
            elif j < height - 1 and mymap[i][j + 1] == index:
                paths.append([i, j + 1])
                j = j + 1
            index -= 1
        # storage['test'].append(paths)
        return mymap[paths[0][0]][paths[0][1]] + 1, mymap, paths, paths[-1]
    else:
        return INF, mymap, None, None
