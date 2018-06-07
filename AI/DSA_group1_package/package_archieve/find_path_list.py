# stat是状态，me是自己的id，desid是des对应的id，des指区域或者纸带，区域为1，纸带为0
# 无路可走返回[‘dis’]为999的字典，已经到达返回['dis']为0的字典(无其他key)
# 如果纸带头紧挨着目标区域，返回['dis']为1，['map']为None
# 把stop的部分改一改。在循环里调用判断stop的条件，判断stop点的值
# 学习c和python的接口
# 针对某些调用次数多的路径进行优化


def find_path(stat, storage, me, desid, des, route_num):
    import queue
    import time
    width = stat['size'][0]  # 场地的宽
    height = stat['size'][1]  # 场地的高
    x = stat['now']['players'][me - 1]['x']   # 己方头部的位置
    y = stat['now']['players'][me - 1]['y']
    ex = stat['now']['players'][2 - me]['x']  # 敌方头部位置
    ey = stat['now']['players'][2 - me]['y']

    if des:
        if stat['now']['fields'][x][y] == desid:  # 头部在己方区域，且寻找到己方区域的最短路径
            return {'dis': 0}
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
    mymap = []  # 记录路径状态，以目标区域为递推起点
    for i in range(width):
        mymap.append([])
        for j in range(height):
            if stat['now'][aim][i][j] == destination:  # 目标区域-2
                mymap[i].append(-2)
            elif stat['now']['bands'][i][j] == me:     # 己方纸带-1
                mymap[i].append(-1)
            else:                                      # 空白区域-4
                mymap[i].append(-4)
    mymap[x][y] = 0                                    # 己方头部0
    if aim == 'bands':  # 搜索到纸带的距离，把头部也当作纸带
        mymap[ex][ey] = -2                             # 对方头部-2

    t2 = time.time()

    # 纸带头紧挨着目标区域
    if x > 0 and mymap[x - 1][y] == -2 and stat['now']['players'][me - 1]['direction'] != 0:
        return {'dis': 1, 'map': None, 'start': [[x - 1, y]]}
    if x < width - 1 and mymap[x + 1][y] == -2 and stat['now']['players'][me - 1]['direction'] != 2:
        return {'dis': 1, 'map': None, 'start': [[x + 1, y]]}
    if y > 0 and mymap[x][y - 1] == -2 and stat['now']['players'][me - 1]['direction'] != 1:
        return {'dis': 1, 'map': None, 'start': [[x, y - 1]]}
    if y < height - 1 and mymap[x][y + 1] == -2 and stat['now']['players'][me - 1]['direction'] != 3:
        return {'dis': 1, 'map': None, 'start': [[x, y + 1]]}

    # 以头部为起点开始搜索，纸带头不紧挨目标区域
    start = queue.Queue()                # 记录搜索的起点
    start.put([x, y])

    count = 0
    temp = []
    while (not start.empty()) and (count < 5):             # 搜索路径
        current = start.get()
        i = current[0]
        j = current[1]
        index = mymap[i][j] + 1
        if i > 0:
            if mymap[i - 1][j] == -4:
                mymap[i - 1][j] = index
                start.put([i - 1, j])
            elif mymap[i - 1][j] == -2:
                count += 1
                temp.append([i, j])
                continue
        if i < width - 1:
            if mymap[i + 1][j] == -4:
                mymap[i + 1][j] = index
                start.put([i + 1, j])
            elif mymap[i + 1][j] == -2:
                count += 1
                temp.append([i, j])
                continue
        if j > 0:
            if mymap[i][j - 1] == -4:
                mymap[i][j - 1] = index
                start.put([i, j - 1])
            elif mymap[i][j - 1] == -2:
                count += 1
                temp.append([i, j])
                continue
        if j < height - 1:
            if mymap[i][j + 1] == -4:
                mymap[i][j + 1] = index
                start.put([i, j + 1])
            elif mymap[i][j + 1] == -2:
                count += 1
                temp.append([i, j])
                continue

    t3 = time.time()

    storage['copytime'] += t2 - t1
    storage['caltime'] += t3 - t2

    if len(temp) != 0:
        # temp是目标区域可以出发的坐标
        return {'dis': mymap[temp[0][0]][temp[0][1]] + 1, 'map': mymap, 'start': temp}
    else:
        return {'dis': 99999, 'map': mymap, 'start': None}


def path_to(stat, storage, person, owner, area_type):
    FIELDS = 1
    BANDS = 0

    flag = True
    for x in stat['now'][area_type]:
        for y in x:
            if y == stat['now'][owner]['id']:
                flag = False
                break
    if flag:
        return {'dis': 99999}
    if person == 'me':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['me']['me'][0]:
                    return storage['path']['me']['me'][0]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['me']['id'], FIELDS)
                storage['path']['me']['me'][0] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['me']['enemy'][0]:
                    return storage['path']['me']['enemy'][0]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['enemy']['id'], FIELDS)
                storage['path']['me']['enemy'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['me']['enemy'][1]:
                    return storage['path']['me']['enemy'][1]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['enemy']['id'], BANDS)
                storage['path']['me']['enemy'][1] = a
                return a
    elif person == 'enemy':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['enemy']['me'][0]:
                    return storage['path']['enemy']['me'][0]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['me']['id'], FIELDS)
                storage['path']['enemy']['me'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['enemy']['me'][1]:
                    return storage['path']['enemy']['me'][1]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['me']['id'], BANDS)
                storage['path']['enemy']['me'][1] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['enemy']['enemy'][0]:
                    return storage['path']['enemy']['enemy'][0]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['enemy']['id'], FIELDS)
                storage['path']['enemy']['enemy'][0] = a
                return a
