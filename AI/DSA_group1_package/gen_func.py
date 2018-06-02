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
    # 返回0，死亡；返回1，目前不会死亡或获胜
    if inx < 0 or iny < 0 or inx >= storage['size'][0] or iny >= storage['size'][1]:
        return 0
    if stat['bands'][inx][iny] == stat['me']['id']:
        return 0
    if stat['fields'][inx][iny] == stat['enemy']['id'] and stat['enemy']['x'] == inx and stat['enemy']['y'] == iny:
        return 0
    if inx == stat['enemy']['x'] and iny == stat['enemy']['y']:
        if stat['enemy']['direction'] == stat['me']['direction']:
            count = fields_count(stat, storage)
            if count[0] < count[1]:
                return 0
    alist = [[None] * storage['size'][1] for i in range(0, storage['size'][0])]
    temp = space_check(stat, storage, inx, iny, alist)
    if temp:
        return 1
    return 0


# 计算双方的领地大小，二元tuple，第一个为自己
def fields_count(stat, storage):
    if storage['fields_count']:
        return storage['fields_count']
    res = [0, 0]
    for x in range(storage['size'][0]):
        for y in range(storage['size'][1]):
            if stat['fields'][x][y]:
                if stat['fields'][x][y] == stat['me']['id']:
                    res[0] += 1
                else:
                    res[1] += 1
    storage['fields_count'] = res
    return res


def space_check(stat, storage, x, y, find_list):
    now_list = [(x, y)]
    find_all = 0
    while True:
        if find_all > stat['turnleft'][1]:
            return True
        if now_list == []:
            return False
        new_list = []
        for element in now_list:
            x = element[0]
            y = element[1]
            if x < 0 or y < 0 or x >= storage['size'][0] or y >= storage['size'][1]:
                pass
            elif stat['fields'][x][y] == stat['me']['id']:
                find_all = 10000
                break
            elif stat['bands'][x][y] == stat['me']['id'] or find_list[x][y] is True or (
                    stat['me']['x'] == x and stat['me']['y'] == y):
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
    if stat['bands'][inx][iny] == stat['enemy']['id']:
        return True
    if inx == stat['enemy']['x'] and iny == stat['enemy']['y']:
        if stat['enemy']['direction'] != stat['me']['direction']:
            return True
        count = fields_count(stat, storage)
        if count[0] > count[1]:
            return True
    return False
