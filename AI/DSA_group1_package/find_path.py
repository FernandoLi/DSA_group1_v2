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
    nodes：假想的墙壁。搜索路径是不能走这里。
输出：
    返回一个元组
    元组的第一个元素代表最短距离。最短距离为0说明在目标区域。最短距离为1说明紧挨着目标区域，最短距离为inf说明无法到达最短区域。
    元组的第二个元素是生成的地图。
    元组的第三个元素是最短路径
    元组的第四个元素是最短路径的终点。这一点是紧挨着目标区域的的点，不是目标区域上的点。
'''


def path_to(stat, storage, this_type, nodes=None):  # 如果算过path_to了，就不算了，如果没算过，就接着算。
    me_id = stat['now']['me']['id']
    enemy_id = stat['now']['enemy']['id']

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
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, me_id, enemy_id, 0, nodes)
    elif this_type == 'enemy_me_bands':
        if storage[this_type] is not None:
            outcome = storage[this_type]
        else:
            outcome = find_path(stat, storage, enemy_id, me_id, 0, nodes)
    return outcome


# stat是状态，me是自己的id，desid是des对应的id，des指区域或者纸带，区域为1，纸带为0
def find_path(stat, storage, me, desid, des, nodes=None):
    import queue
    import time
    width = stat['size'][0]                   # 场地的宽
    height = stat['size'][1]                  # 场地的高
    x = stat['now']['me']['x']                # 己方头部的位置
    y = stat['now']['me']['y']
    ex = stat['now']['enemy']['x']            # 敌方头部位置
    ey = stat['now']['enemy']['y']
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
        if stat['now']['fields'][x][y] == desid:  # 头部在己方区域，且寻找到己方区域的最短路径
            return 0, None, None, None
        aim = 'fields'
        destination = desid
    else:
        aim = 'bands'
        destination = 3 - me

    try:
        storage['copytime']
    except KeyError:
        storage['copytime'] = 0

    try:
        storage['caltime']
    except KeyError:
        storage['caltime'] = 0

    t1 = time.time()
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

    t2 = time.time()

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
                if (i > 0 and mymap[i-1][j] == -4) or (i < width-1 and mymap[i+1][j] == -4) or (j > 0 and mymap[i][j-1] == -4) or (j < height-1 and mymap[i][j+1] == -4):
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
    t3 = time.time()

    storage['copytime'] += t2 - t1
    storage['caltime'] += t3 - t2

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
        while index > 0:
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
