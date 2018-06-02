# stat是状态，me是自己的id，desid是des对应的id，des指区域或者纸带，区域为1，纸带为0
# 无路可走返回[‘dis’]为999的字典，已经到达返回['dis']为0的字典(无其他key)
# 如果纸带头紧挨着目标区域，返回['dis']为1，['map']和['map2']为None


def find_path(stat, storage, me, desid, des):
    width = storage['size'][0]  # 场地的宽
    height = storage['size'][1]  # 场地的高
    x = stat['players'][me - 1]['x']  # 己方头部的位置
    y = stat['players'][me - 1]['y']

    if des:
        if stat['fields'][x][y] == desid:  # 头部在己方区域，且寻找到己方区域的最短路径
            return {'dis': 0}
        aim = 'fields'
        destination = desid
    else:
        aim = 'bands'
        destination = 3 - me

    mymap = []  # 记录路径状态，以目标区域为递推起点
    for i in range(width):
        mymap.append([])
        for j in range(height):
            if stat[aim][i][j] == destination:  # 目标区域
                mymap[i].append(0)
            elif stat['bands'][i][j] == me:  # 己方纸带
                mymap[i].append(-1)
            else:
                mymap[i].append(None)
    mymap[x][y] = -1
    if aim == 'bands':  # 搜索到纸带的距离，把头部也当作纸带
        mymap[stat['players'][2 - me]['x']][stat['players'][2 - me]['y']] = 0

    mymap2 = []  # 记录路径状态，从头部开始递推
    for i in range(width):
        mymap2.append([])
        for j in range(height):
            mymap2[i].append(mymap[i][j])

    if x > 0 and mymap[x - 1][y] == 0:  # 纸带头紧挨着目标区域
        return {'dis': 1, 'map': None, 'start': [[x - 1, y]], 'map2': None, 'start2': [[x - 1, y]]}
    if x < width - 1 and mymap[x + 1][y] == 0:
        return {'dis': 1, 'map': None, 'start': [[x + 1, y]], 'map2': None, 'start2': [[x + 1, y]]}
    if y > 0 and mymap[x][y - 1] == 0:
        return {'dis': 1, 'map': None, 'start': [[x, y - 1]], 'map2': None, 'start2': [[x, y - 1]]}
    if y < height - 1 and mymap[x][y + 1] == 0:
        return {'dis': 1, 'map': None, 'start': [[x, y + 1]], 'map2': None, 'start2': [[x, y + 1]]}

    # 以目的地为起点开始搜索
    start = [[], []]  # 记录搜索的起点
    for i in range(width):
        for j in range(height):
            if mymap[i][j] != 0:
                continue

            if (i > 0 and mymap[i - 1][j] is None) \
                    or (i < width - 1 and mymap[i + 1][j] is None) \
                    or (j > 0 and mymap[i][j - 1] is None) \
                    or (j < height - 1 and mymap[i][j + 1] is None):
                start[0].append([i, j])

    stop = []  # 记录搜索的终点
    temp = []  # 记录路径起点
    if x > 0 and mymap[x - 1][y] != -1 and stat['players'][me - 1]['direction'] != 1:
        stop.append([x - 1, y])
    if x < width - 1 and mymap[x + 1][y] != -1 and stat['players'][me - 1]['direction'] != 3:
        stop.append([x + 1, y])
    if y > 0 and mymap[x][y - 1] != -1 and stat['players'][me - 1]['direction'] != 0:
        stop.append([x, y - 1])
    if y < height - 1 and mymap[x][y + 1] != -1 and stat['players'][me - 1]['direction'] != 2:
        stop.append([x, y + 1])
    length = 0  # 当前搜索的路径长度
    while True:  # 搜索路径
        length += 1
        start[length % 2] = []
        for index in range(len(start[1 - length % 2])):  # 遍历当前节点
            i = start[1 - length % 2][index][0]
            j = start[1 - length % 2][index][1]
            if i > 0 and mymap[i - 1][j] is None:
                mymap[i - 1][j] = length
                start[length % 2].append([i - 1, j])
            if i < width - 1 and mymap[i + 1][j] is None:
                mymap[i + 1][j] = length
                start[length % 2].append([i + 1, j])
            if j > 0 and mymap[i][j - 1] is None:
                mymap[i][j - 1] = length
                start[length % 2].append([i, j - 1])
            if j < height - 1 and mymap[i][j + 1] is None:
                mymap[i][j + 1] = length
                start[length % 2].append([i, j + 1])
        ind = 0
        while ind < len(stop):
            if mymap[stop[ind][0]][stop[ind][1]] is not None:
                temp.append(stop.pop(ind))
            else:
                ind += 1
        if len(stop) == 0:
            break
        if len(start[length % 2]) == 0:
            break

    # 以头部为起点开始搜索
    start2 = [[], []]  # 记录搜索的起点
    start2[0].append([x, y])

    stop2 = []  # 记录搜索的终点
    temp2 = []  # 记录路径起点
    for i in range(width):
        for j in range(height):
            if mymap2[i][j] != 0:
                continue
            if i > 0 and mymap2[i - 1][j] is None and [i - 1, j] not in stop2:
                stop2.append([i - 1, j])
            if i < width - 1 and mymap2[i + 1][j] is None and [i + 1, j] not in stop2:
                stop2.append([i + 1, j])
            if j > 0 and mymap2[i][j - 1] is None and [i, j - 1] not in stop2:
                stop2.append([i, j - 1])
            if j < height - 1 and mymap2[i][j + 1] is None and [i, j + 1] not in stop2:
                stop2.append([i, j + 1])

    length = 0  # 当前搜索的路径长度
    while True:  # 搜索路径
        length += 1
        start2[length % 2] = []
        for index in range(len(start2[1 - length % 2])):  # 遍历当前节点
            i = start2[1 - length % 2][index][0]
            j = start2[1 - length % 2][index][1]
            if i > 0 and mymap2[i - 1][j] is None:
                mymap2[i - 1][j] = length
                start2[length % 2].append([i - 1, j])
            if i < width - 1 and mymap2[i + 1][j] is None:
                mymap2[i + 1][j] = length
                start2[length % 2].append([i + 1, j])
            if j > 0 and mymap2[i][j - 1] is None:
                mymap2[i][j - 1] = length
                start2[length % 2].append([i, j - 1])
            if j < height - 1 and mymap2[i][j + 1] is None:
                mymap2[i][j + 1] = length
                start2[length % 2].append([i, j + 1])
        ind = 0
        while ind < len(stop2):
            if mymap2[stop2[ind][0]][stop2[ind][1]] is not None:
                temp2.append(stop2.pop(ind))
            else:
                ind += 1
        if len(stop2) == 0:
            break
        if len(start2[length % 2]) == 0:
            break

    if len(temp) != 0:
        # temp是己方纸带头周围可以走的点的坐标
        return {'dis': mymap[temp[0][0]][temp[0][1]] + 1, 'map': mymap, 'start': temp, 'map2': mymap2,
                'start2': temp2}
    else:
        return {'dis': 99999, 'map': mymap, 'start': None, 'map2': mymap2, 'start2': None}


def path_to(stat, storage, person, owner, area_type):
    FIELDS = 1
    BANDS = 0

    flag = True
    for x in stat[area_type]:
        for y in x:
            if y == stat[owner]['id']:
                flag = False
                break
    if flag:
        return {'dis': 99999}
    if person == 'me':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['me']['me'][0]:
                    return storage['path']['me']['me'][0]
                a = find_path(stat, storage, stat['me']['id'], stat['me']['id'], FIELDS)
                storage['path']['me']['me'][0] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['me']['enemy'][0]:
                    return storage['path']['me']['enemy'][0]
                a = find_path(stat, storage, stat['me']['id'], stat['enemy']['id'], FIELDS)
                storage['path']['me']['enemy'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['me']['enemy'][1]:
                    return storage['path']['me']['enemy'][1]
                a = find_path(stat, storage, stat['me']['id'], stat['enemy']['id'], BANDS)
                storage['path']['me']['enemy'][1] = a
                return a
    elif person == 'enemy':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['enemy']['me'][0]:
                    return storage['path']['enemy']['me'][0]
                a = find_path(stat, storage, stat['enemy']['id'], stat['me']['id'], FIELDS)
                storage['path']['enemy']['me'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['enemy']['me'][1]:
                    return storage['path']['enemy']['me'][1]
                a = find_path(stat, storage, stat['enemy']['id'], stat['me']['id'], BANDS)
                storage['path']['enemy']['me'][1] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['enemy']['enemy'][0]:
                    return storage['path']['enemy']['enemy'][0]
                a = find_path(stat, storage, stat['enemy']['id'], stat['enemy']['id'], FIELDS)
                storage['path']['enemy']['enemy'][0] = a
                return a
