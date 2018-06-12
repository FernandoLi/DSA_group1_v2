LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'
INF = 99999999
direction_dict = {LEFT: -1, MIDDLE: 0, RIGHT: 1}
from AI.DSA_group1_package.find_path import path_to


def record_bands(stat, storage, ID):
    # 这个函数必须在每一局的开头执行，这时候的来更新本局的纸带列表。
    # 输入：ID 当前计算方的id, 'me'自己'enemy'敌人
    # 输出：无
    head_x = stat['now'][ID]['x']
    head_y = stat['now'][ID]['y']
    if stat['now']['fields'][head_x][head_y] != stat['now'][ID]['id']:
        # 如果我当前头所在的位置不是自己的领地，那么下一回合suppose会变成纸带，所以加入纸带列表
        storage['bands'][ID].append((head_x, head_y))
    else:
        # 如果是自己的领地，说明纸带会消失，圈地完成。
        storage['bands'][ID] = []


# 检查是否立即死亡，或者将要死亡
def dead_check(stat, storage, inx, iny):
    if dying_check(stat, storage, inx, iny) == 1 and fail_check(stat, storage, inx, iny) == 1:
        return 1
    else:
        return 0


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


def find_new_abs_direction(stat, storage, inx, iny, person):
    abs_direction_dict = {(0, 1): 1, (0, -1): 3, (1, 0): 0, (-1, 0): 2}
    for key in abs_direction_dict:
        if (inx - stat['now'][person]['x'], iny - stat['now'][person]['y']) == key:
            return abs_direction_dict[key]


def fail_check(stat, storage, inx, iny):
    # 返回0，死亡；返回1，目前不会死亡或获胜
    if inx < 0 or iny < 0 or inx >= stat['size'][0] or iny >= stat['size'][1]:
        return 0
    if stat['now']['bands'][inx][iny] == stat['now']['me']['id']:
        return 0

    if stat['now']['fields'][inx][iny] == stat['now']['enemy']['id'] and stat['now']['enemy']['x'] == inx and \
            stat['now']['enemy']['y'] == iny:
        return 0

    if stat['now']['fields'][inx][iny] is None and inx == stat['now']['enemy']['x'] and iny == stat['now']['enemy']['y']:
        temp = find_new_abs_direction(stat, storage, inx, iny, 'me')
        if temp + 2 == stat['now']['enemy']['direction'] or temp - 2 == stat['now']['enemy']['direction']:
            count = fields_count(stat, storage)
            if count[0] < count[1]:
                return 0

    return 1


def dying_check(stat, storage, inx, iny):
    # 易于死亡返回0，不易于死亡返回1
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
    me_enemy_x = abs(inx - stat['now']['enemy']['x'])
    me_enemy_y = abs(iny - stat['now']['enemy']['y'])
    if (me_enemy_x == 1 and me_enemy_y == 0) or (me_enemy_x == 0 and me_enemy_y == 1):
        flag = True
    if stat['now']['fields'][inx][iny] == stat['now']['enemy']['id'] and flag:
        for i in [RIGHT,LEFT,MIDDLE]:
            if (stat['now']['me']['x'], stat['now']['me']['y'], ) == \
                    move(stat['now']['enemy']['x'],stat['now']['enemy']['y'] , stat['now']['enemy']['direction'] + direction_dict[i]):
                return 0
    if stat['now']['fields'][inx][iny] is None and flag:
        mynew = find_new_abs_direction(stat, storage, inx, iny, 'me')
        enemynew = find_new_abs_direction(stat, storage, inx, iny, 'enemy')
        if abs(mynew - enemynew) == 2:
            fields = fields_count(stat, storage)
            if fields[0] > fields[1]:
                return 1
        else:
            return 0
    return 1


# 计算双方的领地大小，二元tuple，第一个为自己
def fields_count(stat, storage):
    # if storage['fields_count']:
    # return storage['fields_count']
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
    # 足够大返回True；否则False
    now_list = [(x, y)]
    find_all_list = [[None] * stat['size'][1] for i in range(0, stat['size'][0])]
    find_num = 0
    while True:
        me_id = stat['now']['me']['id']  # 这里原来是bug啊，list的0元素是先手玩家，1元素是后手玩家
        if find_num >= stat['now']['turnleft'][me_id - 1]:
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





def field_compare(me, enemy, stat, storage):
    count = [0, 0]
    for i in range(stat['size'][0]):
        for j in range(stat['size'][1]):
            if stat['now']['fields'][i][j] == me:
                count[me - 1] = count[me - 1] + 1
            elif stat['now']['fields'][i][j] == enemy:
                count[enemy - 1] = count[enemy - 1] + 1
    if count[me - 1] >= count[enemy - 1]:
        return True
    else:
        return False


# 检查MLR三个方向，如果有一个方向能直接击杀对手，那么直接返回那个方向
# 如果不能直接击杀对手，返回 None
def win_check(stat, storage):
    meb = path_to(stat, storage, 'me_enemy_bands')  # 我到对方纸带的最短距离
    if meb[0] == INF:
        return None
    else:
        target_x = meb[3][0]
        target_y = meb[3][1]
        me = stat['now']['me']
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if abs(target_x - me['x']) + abs(target_y - me['y']) > 1:
            return None
        else:
            deltax = target_x - me['x']
            deltay = target_y - me['y']
            nxt_direction = directions.index((deltax, deltay))
            delta = nxt_direction - me['direction']
            if delta == 0:
                outcome = MIDDLE
            elif delta == 1 or delta == -3:
                outcome = RIGHT
            elif delta == -1 or delta == 3:
                outcome = LEFT  # 计算下一步应该怎么走
            else:
                return None
            if stat['now']['fields'][target_x][target_y] == me['id']:
                return outcome
            elif stat['now']['fields'][target_x][target_y] is None:
                if stat['now']['enemy']['x'] == target_x and stat['now']['enemy']['y'] == target_y:
                    if abs(nxt_direction - stat['now']['enemy']['direction']) == 2:
                        if field_compare(me['id'], stat['now']['enemy']['id'], stat, storage):
                            return outcome
                        else:
                            return None
                    else:
                        return outcome
                else:
                    return outcome
            else:
                return None
