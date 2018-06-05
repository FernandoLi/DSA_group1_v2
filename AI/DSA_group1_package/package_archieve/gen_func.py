LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'
direction_dict = {LEFT: -1, MIDDLE: 0, RIGHT: 1}


def move(nowx, nowy, direction):
    if direction < 0:
        direction += 4
    if direction > 3:
        direction -= 4
    if direction == 0:
        return nowx + 1, nowy
    if direction == 1:
        return nowx, nowy + 1
    if direction == 2:
        return nowx - 1, nowy
    if direction == 3:
        return nowx, nowy - 1


def fail_check(stat, storage, inx, iny):
    from time import time
    t0 = time()
    # 返回0，死亡；返回1，目前不会死亡或获胜
    if inx < 0 or iny < 0 or inx >= stat['size'][0] or iny >= stat['size'][1]:
        t1 = time()
        storage['dead_time'].append(t1-t0)
        return 0
    if stat['now']['bands'][inx][iny] == stat['now']['me']['id']:
        t1 = time()
        storage['dead_time'].append(t1 - t0)
        return 0
    if stat['now']['fields'][inx][iny] == stat['now']['enemy']['id'] and stat['now']['enemy']['x'] == inx and stat['now']['enemy']['y'] == iny:
        t1 = time()
        storage['dead_time'].append(t1 - t0)
        return 0
    if inx == stat['now']['enemy']['x'] and iny == stat['now']['enemy']['y']:
        if stat['now']['enemy']['direction'] == stat['now']['me']['direction']:
            count = fields_count(stat, storage)
            if count[0] < count[1]:
                t1 = time()
                storage['dead_time'].append(t1 - t0)
                return 0
    test1 = move(inx, iny, stat['now']['me']['direction'])
    test2 = move(test1[0] ,test1[1] ,stat['now']['me']['direction'] + direction_dict[LEFT])
    test3 = move(test1[0], test1[1], stat['now']['me']['direction'] + direction_dict[RIGHT])
    flag = False
    for point in [test1,test2,test3]:
        if point[0] < 0 or point[1] < 0 or point[0] >= stat['size'][0] or point[1] >= stat['size'][1]:
            flag = True
            break
        if stat['now']['bands'][point[0]][point[1]] == stat['now']['me']['id']:
            flag = True
            break
    if not flag:
        t1 = time()
        storage['dead_time'].append(t1 - t0)
        return 1
    alist = [[None] * stat['size'][1] for i in range(0, stat['size'][0])]
    temp = space_check(stat, storage, inx, iny, alist)
    t1 = time()
    storage['dead_time'].append(t1 - t0)
    if temp:
        return 1
    return 0


# 计算双方的领地大小，二元tuple，第一个为自己
def fields_count(stat, storage):
    if storage['fields_count']:
        return storage['fields_count']
    res = [0, 0]
    for x in range(stat['size'][0]):
        for y in range(stat['size'][1]):
            if stat['now']['fields'][x][y]:
                if stat['now']['fields'][x][y] == stat['now']['me']['id']:
                    res[0] += 1
                else:
                    res[1] += 1
    storage['fields_count'] = res
    return res


def space_check(stat, storage, x, y, find_list):
    now_list = [(x, y)]
    find_all = 0
    while True:
        if find_all > stat['now']['turnleft'][1]:
            return True
        if now_list == []:
            return False
        new_list = []
        for element in now_list:
            x = element[0]
            y = element[1]
            if x < 0 or y < 0 or x >= stat['size'][0] or y >= stat['size'][1]:
                pass
            elif stat['now']['fields'][x][y] == stat['now']['me']['id']:
                find_all = 10000
                break
            elif stat['now']['bands'][x][y] == stat['now']['me']['id'] or find_list[x][y] is True or (
                    stat['now']['me']['x'] == x and stat['now']['me']['y'] == y):
                pass
            else:
                find_all += 1
                find_list[x][y] = True
                new_list.append((x + 1, y,))
                new_list.append((x - 1, y,))
                new_list.append((x, y + 1,))
                new_list.append((x, y + 1,))
        now_list = new_list


# 立即胜利情形，很罕见
def win_check(stat , storage , inx ,iny):
    #  立即获胜返回True，否则False
    if stat['now']['bands'][inx][iny] == stat['now']['enemy']['id']:
        return True
    if inx == stat['now']['enemy']['x'] and iny == stat['now']['enemy']['y']:
        if stat['now']['enemy']['direction'] != stat['now']['me']['direction']:
            return True
        count = fields_count(stat, storage)
        if count[0] > count[1]:
            return True
    return False
