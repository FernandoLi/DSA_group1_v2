LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'
direction_dict = {LEFT: -1, MIDDLE: 0, RIGHT: 1}


def record_bands(stat, storage, ID):
    # 这个函数必须在每一局的开头执行，这时候的来更新本局的纸带列表。
    # 输入：ID 当前计算方的id, 'me'自己'enermy'敌人
    # 输出：无
    head_x = stat['now'][ID]['x']
    head_y = stat['now'][ID]['y']
    if stat['now']['fields'][head_x][head_y] != stat['now'][ID]['id']:
        # 如果我当前头所在的位置不是自己的领地，那么下一回合suppose会变成纸带，所以加入纸带列表
        storage['bands'][ID].append((head_x, head_y))
    else:
        # 如果是自己的领地，说明纸带会消失，圈地完成。
        storage['bands'][ID] = []


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

def find_new_abs_direction(stat, storage, inx, iny ,person):
    abs_direction_dict = {(0,1):1,(0,-1):3,(1,0):0,(-1,0):2}
    for key in abs_direction_dict:
        if (inx-stat['now'][person]['x'],iny-stat['now'][person]['y']) == key:
            return abs_direction_dict[key]

def fail_check(stat, storage, inx, iny):
    # 返回0，死亡；返回1，目前不会死亡或获胜
    if inx < 0 or iny < 0 or inx >= stat['size'][0] or iny >= stat['size'][1]:
        return 0
    if stat['now']['bands'][inx][iny] == stat['now']['me']['id']:
        print(inx,iny , stat['now']['bands'][inx][iny] , stat['now']['me']['id'])
        return 0

    if stat['now']['fields'][inx][iny] == stat['now']['enemy']['id'] and stat['now']['enemy']['x'] == inx and stat['now']['enemy']['y'] == iny:
        return 0

    if inx == stat['now']['enemy']['x'] and iny == stat['now']['enemy']['y']:
        if stat['now']['enemy']['direction'] == find_new_abs_direction(stat,storage,inx,iny,'me'):
            count = fields_count(stat, storage)
            if count[0] < count[1]:
                return 0

    return 1


def dying_check(stat,storage,inx,iny):
    #易于死亡返回0，不易于死亡返回1
    orix = stat['now']['me']['x']
    oriy = stat['now']['me']['y']
    nowdir = stat['now']['me']['direction']
    test1 = move(orix, oriy, nowdir)
    test2 = move(test1[0], test1[1], nowdir + direction_dict['L'])
    test3 = move(test1[0], test1[1], nowdir + direction_dict['R'])
    flag = False
    for point in [test1, test2, test3]:
        if point[0] < 0 or point[1] < 0 or point[0] >= stat['size'][0] or point[1] >= stat['size'][1]:
            flag = True
            break
        if stat['now']['bands'][point[0]][point[1]] == stat['now']['me']['id']:
            flag = True
            break
    if flag:
        temp = space_check(stat, storage, inx, iny)
        if not temp:
            return 0
    flag = False
    me_enemy_x = abs(inx-stat['now']['enemy']['x'])
    me_enemy_y = abs(iny-stat['now']['enemy']['y'])
    if (me_enemy_x==1 and me_enemy_y==0) or (me_enemy_x==0 and me_enemy_y==1):
        flag = True
    if stat['now']['fields'][inx][iny] == stat['now']['enemy']['id'] and flag:
        return 0
    if stat['now']['fields'][inx][iny] is None and flag:
        mynew = find_new_abs_direction(stat, storage, inx, iny, 'me')
        enemynew = find_new_abs_direction(stat,storage,inx,iny,'enemy')
        print(inx,iny,stat['now']['enemy']['x'],stat['now']['enemy']['y'])
        if  abs(mynew-enemynew) == 2:
            fields = fields_count(stat, storage)
            if fields[0] > fields[1]:
                return True
        else:
            return 0
    return 1



# 计算双方的领地大小，二元tuple，第一个为自己
def fields_count(stat, storage):
    #if storage['fields_count']:
        #return storage['fields_count']
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


def space_check(stat, storage, x, y):
    #足够大返回True；否则False
    now_list = [(x, y)]
    find_all_list = [[None]*stat['size'][1]for i in range(0,stat['size'][0])]
    find_num = 0
    while True:
        if find_num >= stat['now']['turnleft'][1]:
            return True
        if now_list == []:
            return False
        new_list = []
        for element in now_list:
            x = element[0]
            y = element[1]
            if x < 0 or y < 0 or x >= stat['size'][0] or y >= stat['size'][1]:
                continue
            elif stat['now']['fields'][x][y] == stat['now']['me']['id']:
                return True
            elif stat['now']['bands'][x][y] == stat['now']['me']['id'] or (find_all_list[x][y]) or (
                    stat['now']['me']['x'] == x and stat['now']['me']['y'] == y):
                continue
            else:
                find_all_list[x][y] = True
                find_num += 1
                new_list.append((x + 1, y,))
                new_list.append((x - 1, y,))
                new_list.append((x, y + 1,))
                new_list.append((x, y - 1,))
        now_list = new_list


# 立即胜利情形，很罕见
def win_check(stat , storage , inx ,iny):
    #  立即获胜返回True，否则False
    if stat['now']['bands'][inx][iny] == stat['now']['enemy']['id']:
        return True
    if stat['now']['enemy']['x'] == inx and stat['now']['enemy']['y'] == iny:
        if stat['now']['fields'][inx][iny] == stat['now']['me']['id']:
            return True
        elif stat['now']['fields'][inx][iny] == stat['now']['enemy']['id']:
            return False
        else:
            temp = find_new_abs_direction(stat,storage,inx,iny,'me')
            if temp+2 == stat['now']['enemy']['direction'] or temp-2 == stat['now']['enemy']['direction']:
                fields = fields_count(stat,storage)
                if fields[0]>fields[1]:
                    return True
            else:
                return True
    return False


