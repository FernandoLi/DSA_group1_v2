from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.gen_func import LEFT
from AI.DSA_group1_package.gen_func import RIGHT
from AI.DSA_group1_package.gen_func import MIDDLE
from AI.DSA_group1_package.gen_func import dead_check
from AI.DSA_group1_package.gen_func import win_check
from AI.DSA_group1_package.find_path import path_to
from AI.DSA_group1_package.find_path import find_path
import random

ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'
INF = 99999999


class Attack(State):
    # 这里如果需要新的初始化函数，可以这样写，不用的话可以省略。
    # def __init__(self, name, store):  # store = storage['statename_store']
    #     super(State, self).__init__(name, store)
    def field_compare(self, me, enemy, stat, storage):
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

    def exchange(self, direction, a, b):
        p = MIDDLE
        if direction == 0:  # 当前方向向东
            if a == 1 and b == 0:
                p = MIDDLE
            elif a == 0 and b == -1:
                p = LEFT
            elif a == 0 and b == 1:
                p = RIGHT
        elif direction == 1:  # 当前方向南
            if a == 1 and b == 0:
                p = LEFT
            elif a == -1 and b == 0:
                p = RIGHT
            elif a == 0 and b == 1:
                p = MIDDLE
        elif direction == 2:  # 当前方向西
            if a == -1 and b == 0:
                p = MIDDLE
            elif a == 0 and b == -1:
                p = RIGHT
            elif a == 0 and b == 1:
                p = LEFT
        elif direction == 3:  # 当前方向北
            if a == 1 and b == 0:
                p = RIGHT
            elif a == -1 and b == 0:
                p = LEFT
            elif a == 0 and b == -1:
                p = MIDDLE
        return p

    def detour_attack(self, stat, storage, last_state_name):
        # step1: 处理几种进入状态的case：enclose, attack, approach, retreat
        # step2: 根据现在的情况计算出一个路径/或者一个输出值，这个自己看。但是必须有一个返回值
        if last_state_name == RETREAT:
            pass
        elif last_state_name == APPROACH:
            pass
        elif last_state_name == ENCLOSE:
            pass
        elif last_state_name == ATTACK:  # 还是attack
            east = 0
            west = 0
            north = 0
            south = 0
            optim_path = MIDDLE  # 记录最终的规划路径
            psa = path_to(stat, storage, 'me_enemy_bands')  # 我到对方纸带的最短距离
            psf = path_to(stat, storage, 'enemy_enemy_fields')  # 对方回家的最短距离
            r = self.field_compare(stat['now']['me']['id'], stat['now']['enemy']['id'], stat, storage)  # 判断双方领地大小
            abb = abs(stat['now']['me']['x'] - stat['now']['enemy']['x'])
            abl = abs(stat['now']['me']['y'] - stat['now']['enemy']['y'])
            if stat['now']['me']['x'] < stat['now']['enemy']['x']:
                x = stat['now']['me']['x']
                east = 1  # 表示对方在自己的东边
            elif stat['now']['me']['x'] > stat['now']['enemy']['x']:
                x = stat['now']['enemy']['x']
                west = 1  # 表示对方在自己的西边
            else:
                x = stat['now']['me']['x']
                east = 2
                west = 2
            if stat['now']['me']['y'] < stat['now']['enemy']['y']:
                y = stat['now']['me']['y']
                south = 1  # 表示对方在自己的南边
            elif stat['now']['me']['y'] > stat['now']['enemy']['y']:
                y = stat['now']['enemy']['y']
                north = 1  # 表示对方在自己的北边
            else:
                y = stat['now']['me']['y']
                north = 2
                south = 2
            xx = stat['now']['me']['x']
            yy = stat['now']['me']['y']
            pas = []  # 记录那些方向能走，那些不能
            pas.append(dead_check(stat, storage, xx, yy - 1))  # 北边能不能走
            pas.append(dead_check(stat, storage, xx, yy + 1))  # 南边能不能走
            pas.append(dead_check(stat, storage, xx - 1, yy))  # 西边能不能走
            pas.append(dead_check(stat, storage, xx + 1, yy))  # 东边能不能走
            if pas[0] == 1:
                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
            elif pas[1] == 1:
                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
            elif pas[2] == 1:
                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
            elif pas[3] == 1:
                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)

            if xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] == stat['now']['enemy']['id'] or (
                    stat['now']['enemy']['x'] == xx - 1 and stat['now']['enemy']['y'] == yy):
                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
            elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] == stat['now']['enemy']['id'] or (
                    stat['now']['enemy']['x'] == xx + 1 and stat['now']['enemy']['y'] == yy):
                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
            elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] == stat['now']['enemy']['id'] or (
                    stat['now']['enemy']['x'] == xx and stat['now']['enemy']['y'] == yy - 1):
                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
            elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] == stat['now']['enemy']['id'] or (
                    stat['now']['enemy']['x'] == xx and stat['now']['enemy']['y'] == yy + 1):
                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
            elif (abb == 0 or abl == 0):  # 两方带头处于同一直线，对方无法在被撞到之前回到领地
                flag = 0  # 判断两带头中是不是没有己方纸带
                if abb == 0:
                    for i in range(abl):
                        if stat['now']['bands'][x][y + i] == stat['now']['me']['id']:
                            flag = 1
                            break
                elif abl == 0:
                    for i in range(abb):
                        if stat['now']['bands'][x + i][y] == stat['now']['me']['id']:
                            flag = 1
                            break
                if flag == 0 and r and (abb // 2 == 1 or abl // 2 == 1) and psf[
                    0] > abb + abl:  # 当前几方面积大于对方并且距离为奇数,中间没有自己的纸带，一直往前走就肯定能赢，目前不考虑对方能回自己领地的情况
                    if east == 1:
                        if pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                    elif west == 1:
                        if pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                    elif north == 1:
                        if pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                    elif south == 1:
                        if pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                elif flag == 1 or abb // 2 == 0 or abl // 2 == 0:  # 距离是偶数或当前己方面积小于对方，有纸带，需要先往旁边让一步，试探一下再靠近
                    if east == 1:
                        if pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                    elif west == 1:
                        if pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                    elif north == 1:
                        if pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                    elif south == 1:
                        if pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
            elif psa[0] > 20:  # 离得很远
                if abb < abl:  # 横边长于竖边，优先沿竖边走
                    if north == 1:
                        if pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                    elif south == 1:
                        if pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                    elif east == 1:
                        if pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                    elif west == 1:
                        if pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                else:  # 竖边长于横边，优先沿横边走
                    if east == 1:
                        if pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                    elif west == 1:
                        if pas[2] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif pas[3] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                    elif north == 1:
                        if pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                    elif south == 1:
                        if pas[1] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif pas[0] == 1:
                            optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
            elif abb != 0 and abl != 0:  # 两带头错开
                locfield = [[2 for i in range(abl + 1)] for j in range(abb + 1)]  # 记录该片区域的状况，划分等级，为之后的路径规划提供参考
                optim_target = []
                # xxx，yyy表示带头在locfield中的坐标
                if xx < stat['now']['enemy']['x']:
                    xxx = 0
                    x = xx
                else:
                    xxx = xx - stat['now']['enemy']['x']
                    x = stat['now']['enemy']['x']
                if yy < stat['now']['enemy']['y']:
                    yyy = 0
                    y = yy
                else:
                    yyy = yy - stat['now']['enemy']['y']
                    y = stat['now']['enemy']['y']
                target = [stat['now']['enemy']['x'], stat['now']['enemy']['y']]  # 初始目标设为对方带头
                mind = [abl + abb, 0]  # 记录最短距离
                for i in range(abb + 1):
                    for j in range(abl + 1):
                        if stat['now']['fields'][x + i][y + j] == stat['now']['enemy']['id']:
                            locfield[i][j] = 1  # 优先度很低，尽量避免进攻路线穿过对方领地
                        elif stat['now']['fields'][x + i][y + j] == stat['now']['me']['id']:
                            locfield[i][j] = 3  # 让进攻路线穿过自己的领地是一种保险的做法
                        elif stat['now']['bands'][x + i][y + j] == stat['now']['me']['id']:
                            locfield[i][j] = 0  # 优先度最低，一定不能撞上自己的纸带
                        elif stat['now']['bands'][x + i][y + j] == stat['now']['enemy']['id']:
                            locfield[i][j] = 4  # 优先度很高，表明在双方带头间存在对方纸带，能对对方的行动造成一定的阻碍，并作为最优候选目标,可升级为最优目标
                            optim_target.append([i, j])
                for k in range(len(optim_target)):
                    # 根据双方位置确定进攻的大方向并规划进攻路线
                    if xxx < optim_target[k][0]:
                        xd = 1  # 表示目标在自己的东边
                    elif xxx > optim_target[k][0]:
                        xd = -1  # 表示目标在自己的西边
                    else:
                        xd = 0
                    if yyy < optim_target[k][1]:
                        yd = 1  # 表示目标在自己的南边
                    elif yyy > optim_target[k][1]:
                        yd = -1  # 表示目标在自己的北边
                    else:
                        yd = 0
                    if abs(xxx - optim_target[k][0]) + abs(yyy - optim_target[k][1]) <= mind[0]:
                        # 判断能否用通过敌方领地的方式直接抵达（没有己方纸带阻拦）
                        if yyy == optim_target[k][1]:  # 在同一横线上
                            band_ex = 0
                            field_ex = 0
                            for i in range(1, abs(xxx - optim_target[k][0])):
                                if locfield[xxx + xd * i][yyy] == 0:
                                    band_ex = 1
                                    break
                                elif locfield[xxx + xd * i][yyy] == 1:
                                    field_ex = 1
                            if band_ex != 1:
                                if field_ex == 0 or (field_ex == 1 and mind[1] == 1):
                                    target = [optim_target[k][0], optim_target[k][1]]  # 更新进攻目标
                                    mind = [abs(xxx - optim_target[k][0]), 0]  # 第二个表示是否必须经过对方领地
                                    if stat['now']['me']['direction'] == 0:  # 当前方向向东
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                            'id']:
                                            optim_path = LEFT
                                        elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                    elif stat['now']['me']['direction'] == 1:  # 当前方向南
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 2:  # 当前方向西
                                        if xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                            'id']:
                                            optim_path = RIGHT
                                        elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                    elif stat['now']['me']['direction'] == 3:  # 当前方向北
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                            'id']:
                                            optim_path = MIDDLE
                        elif xxx == optim_target[k][0]:  # 在同一竖线上
                            band_ex = 0
                            field_ex = 0
                            for i in range(1, abs(yyy - optim_target[k][1])):
                                if locfield[xxx][yyy + yd * i] == 0:
                                    band_ex = 1
                                    break
                                elif locfield[xxx][yyy + yd * i] == 1:
                                    field_ex = 1
                            if band_ex != 1:
                                if field_ex == 0 or (field_ex == 1 and mind[1] == 1):
                                    target = [optim_target[k][0], optim_target[k][1]]  # 更新进攻目标
                                    mind = [abs(yyy - optim_target[k][1]), 0]  # 第二个表示是否经过对方领地
                                    if stat['now']['me']['direction'] == 0:  # 当前方向向东
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 1:  # 当前方向南
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                            'id']:
                                            optim_path = RIGHT
                                    elif stat['now']['me']['direction'] == 2:  # 当前方向西
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                            'id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 3:  # 当前方向北
                                        if yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                            'id']:
                                            optim_path = LEFT
                        else:
                            flag = True
                            '''
                            for i in range(abs(yyy - optim_target[k][1]) + 1):
                                if locfield[xxx][yyy + yd * i] == 0:
                                    l = xxx + xd
                                    m = yyy + yd * i
                                    while l >= min(xxx, optim_target[k][0]) and l <= max(xxx, optim_target[k][0]) and m <= max(yyy, optim_target[k][1]) and m >= min(yyy, optim_target[k][1]):
                                        if locfield[l][m] == 0:
                                            l = l + xd
                                            if m + 1 <= max(yyy, optim_target[k][1]) and locfield[l][m + 1] == 0:
                                                m = m + 1
                                            elif m - 1 >= min(yyy, optim_target[k][1]) and locfield[l][m - 1] == 0:
                                                m = m - 1
                                        elif m == yyy:
                                            flag = True
                                            break
                                        else:
                                            flag = False
                                            break
                            '''
                            if flag:  # 表示可以通过，没有己方纸带阻拦
                                target = [optim_target[k][0], optim_target[k][1]]  # 更新进攻目标
                                mind = [abs(stat['now']['me']['x'] - optim_target[k][0]) + abs(
                                    stat['now']['me']['y'] - optim_target[k][1]), 0]  # 第二个表示是否经过对方领地
                                if abs(stat['now']['me']['x'] - optim_target[k][0]) < abs(
                                        stat['now']['me']['y'] - optim_target[k][1]):  # 横边小于竖边，优先沿横边走
                                    if stat['now']['me']['direction'] == 0:  # 当前方向向东
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif yd == -1:
                                            if yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                                'id']:
                                                optim_path = LEFT
                                            elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                    stat['now']['me']['id']:
                                                optim_path = RIGHT
                                        elif yd == 1:
                                            if yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                    stat['now']['me']['id']:
                                                optim_path = RIGHT
                                            elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                                'id']:
                                                optim_path = LEFT
                                    elif stat['now']['me']['direction'] == 1:  # 当前方向南
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 2:  # 当前方向西
                                        if xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif yd == -1:
                                            if yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                                    'id']:
                                                optim_path = RIGHT
                                            elif yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                    stat['now']['me']['id']:
                                                optim_path = LEFT
                                        elif yd == 1:
                                            if yy + 1 < stat['size'][1] and stat['now']['bands'][xx][yy + 1] != \
                                                    stat['now']['me']['id']:
                                                optim_path = RIGHT
                                            elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                                'id']:
                                                optim_path = LEFT
                                    elif stat['now']['me']['direction'] == 3:  # 当前方向北
                                        if xd == 1 and xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif xd == -1 and xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif yy - 1 >= 0 and stat['now']['bands'][xx][yy - 1] != stat['now']['me'][
                                                'id']:
                                            optim_path = MIDDLE
                                else:  # 竖边小于横边，优先沿竖边走
                                    if stat['now']['me']['direction'] == 0:  # 当前方向向东
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 1:  # 当前方向南
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif xd == 1:
                                            if xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                    stat['now']['me']['id']:
                                                optim_path = LEFT
                                            elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                                'id']:
                                                optim_path = RIGHT
                                        elif xd == -1:
                                            if xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                                    'id']:
                                                optim_path = RIGHT
                                            elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                    stat['now']['me']['id']:
                                                optim_path = LEFT
                                    elif stat['now']['me']['direction'] == 2:  # 当前方向西
                                        if yd == 1 and stat['now']['bands'][xx][yy + 1] != stat['now']['me']['id']:
                                            optim_path = LEFT
                                        elif yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = RIGHT
                                        elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                            'id']:
                                            optim_path = MIDDLE
                                    elif stat['now']['me']['direction'] == 3:  # 当前方向北
                                        if yd == -1 and stat['now']['bands'][xx][yy - 1] != stat['now']['me']['id']:
                                            optim_path = MIDDLE
                                        elif xd == 1:
                                            if xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                    stat['now']['me']['id']:
                                                optim_path = RIGHT
                                            elif xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                                'id']:
                                                optim_path = LEFT
                                        elif xd == -1:
                                            if xx - 1 >= 0 and stat['now']['bands'][xx - 1][yy] != stat['now']['me'][
                                                    'id']:
                                                optim_path = LEFT
                                            elif xx + 1 < stat['size'][0] and stat['now']['bands'][xx + 1][yy] != \
                                                    stat['now']['me']['id']:
                                                optim_path = RIGHT
                if len(optim_target) == 0:  # 没有可替代的点
                    if abb > abl:  # 横边长于竖边，优先沿竖边走
                        if north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif west == 1:
                                if pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                                elif pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif east == 1:
                                if pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                                elif pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif west == 1:
                                if pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                                elif pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif east == 1:
                                if pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                                elif pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                        elif east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif north == 1:
                                if pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                                elif pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif south == 1:
                                if pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                                elif pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif north == 1:
                                if pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                                elif pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif south == 1:
                                if pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                                elif pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                    else:  # 竖边长于横边，优先沿横边走
                        if east == 1:
                            if pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif north == 1:
                                if pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                                elif pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif south == 1:
                                if pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                                elif pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                        elif west == 1:
                            if pas[2] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif north == 1:
                                if pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                                elif pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif south == 1:
                                if pas[1] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                                elif pas[0] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif pas[3] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                        elif north == 1:
                            if pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
                            elif west == 1:
                                if pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                                elif pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif east == 1:
                                if pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                                elif pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                        elif south == 1:
                            if pas[1] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, 1)
                            elif west == 1:
                                if pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                                elif pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                            elif east == 1:
                                if pas[3] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], 1, 0)
                                elif pas[2] == 1:
                                    optim_path = self.exchange(stat['now']['me']['direction'], -1, 0)
                            elif pas[0] == 1:
                                optim_path = self.exchange(stat['now']['me']['direction'], 0, -1)
            return optim_path  # return 0  # 路径的第一个值  # debug  # return random.choice('LMR')  # debug

    def direct_attack(self, stat, storage, last_state_name):
        me = stat['now']['me']
        target = self.store['target_win_point']
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        if me['x'] == target[0] and me['y'] == target[1]:
            self.store['target_win_point'] = None
            xl, yl = me['x'] + directions[me['direction'] - 1][0], me['y'] + directions[me['direction'] - 1][1]
            tlt = dead_check(stat, storage, xl, yl)
            if tlt == 1:
                return LEFT
            xr, yr = me['x'] + directions[me['direction'] - 3][0], me['y'] + directions[me['direction'] - 3][1]
            trt = dead_check(stat, storage, xr, yr)
            if trt == 1:
                return RIGHT
            else:
                return MIDDLE
        if self.store['target_win_point'] is not None:
            xf, yf = me['x'] + directions[me['direction']][0], me['y'] + directions[me['direction']][1]
            forward = abs(xf - target[0]) + abs(yf - target[1])
            fwd = dead_check(stat, storage, xf, yf)
            if fwd == 0:
                forward += 1
            else:
                if stat['now']['fields'][xf][yf] == me['id']:
                    forward -= 0.5
            xl, yl = me['x'] + directions[me['direction'] - 1][0], me['y'] + directions[me['direction'] - 1][1]
            turnleft = abs(xl - target[0]) + abs(yl - target[1])
            tlt = dead_check(stat, storage, xl, yl)
            if tlt == 0:
                turnleft += 1
            else:
                if stat['now']['fields'][xl][yl] == me['id']:
                    turnleft -= 0.5
            xr, yr = me['x'] + directions[me['direction'] - 3][0], me['y'] + directions[me['direction'] - 3][1]
            turnright = abs(xr - target[0]) + abs(yr - target[1])
            trt = dead_check(stat, storage, xr, yr)
            if trt == 0:
                turnright += 1
            else:
                if stat['now']['fields'][xr][yr] == me['id']:
                    turnright -= 0.5
            if forward <= turnleft and forward <= turnright:
                if forward > (abs(me['x'] - target[0]) + abs(me['y'] - target[1])):
                    if turnleft <= turnright:
                        return LEFT
                    else:
                        return RIGHT
                else:
                    return MIDDLE
            elif turnleft < forward and turnleft < turnright:
                return LEFT
            else:
                return RIGHT

    def init_output(self, stat, storage, last_state_name):  # storage几乎用不到，预备以后应用多局历史数据
        meb = path_to(stat, storage, 'me_enemy_bands')  # 我到对方纸带的最短距离
        if meb[0] != INF:
            target_x = meb[3][0]
            target_y = meb[3][1]
            me = stat['now']['me']
            if stat['now']['fields'][target_x][target_y] == me['id']:
                self.store['target_win_point'] = (target_x, target_y)
                outcome = self.direct_attack(stat, storage, last_state_name)
            else:
                if self.store.__contains__('target_win_point'):
                    pass
                else:
                    self.store['target_win_point'] = None
                if self.store['target_win_point'] is not None:
                    outcome = self.direct_attack(stat, storage, last_state_name)
                else:
                    outcome = self.detour_attack(stat, storage, last_state_name)
        else:
            outcome = self.detour_attack(stat, storage, last_state_name)
        return outcome

    def subquent_output(self, stat, storage):
        outcome = self.init_output(stat, storage, self.name)

        return outcome
        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        #  return 0
        #  路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。  # return random.choice('LMR')

    # 完备了！！
    def trans_where(self, stat, storage, outcome=None):
        '''
        if self.if_transfer_in_win(stat, storage):  # 先判断当前是否为必胜条件
            return ATTACK
        else:
            if_retreat = storage[RETREAT].if_transfer_in(stat, storage)
            if if_retreat == 1:
                return RETREAT
            else:
                return ATTACK
        '''

        if self.if_transfer_in_win(stat, storage):  # 先判断当前是否为必胜条件
            return ATTACK
        elif storage[RETREAT].if_transfer_in(stat, storage):  # 判断是否需要撤退
            return RETREAT
        else:  # 继续进攻
            return ATTACK


        # def trans_where(self, stat, storage, outcome=None):
        #     if storage[APPROACH].if_transfer_in(stat, storage):  # 回到领地，go to approach
        #         return APPROACH
        #     else:  # 还是自己
        #         if_retreat = storage[RETREAT].if_transfer_in(stat, storage)
        #         if if_retreat == -1:  # 说明跑不了了，干脆进攻吧
        #             return ATTACK
        #         else:
        #             return RETREAT

        # outcome是为了，把下一步走什么列在state_transfer的考虑之中，我们目前可以简化不用，升级版可以用
        #  step1: 有几种出去状态的情况，就考虑几种情况
        #  Step2: 根据每一种情况，返回下一个状态的名字
        #  下面我把几种情况列举好，不过优先级顺序自己定  # debug

    def if_transfer_in(self, stat, storage):
        meb = path_to(stat, storage, 'me_enemy_bands')[0]  # 我到对方纸带的最短距离
        eef = path_to(stat, storage, 'enemy_enemy_fields')[0]  # 对方回家的最短距离
        if meb <= eef:
            return True
        else:
            return False

    def if_transfer_in_win(self, stat, storage):
        meb = path_to(stat, storage, 'me_enemy_bands')[0]  # 我到对方纸带的最短距离
        eef = path_to(stat, storage, 'enemy_enemy_fields')[0]  # 对方回家的最短距离
        emb = path_to(stat, storage, 'enemy_me_bands')[0]  # 对方到我纸带的最短距离
        if meb <= min(eef, emb):
            return True
        else:
            return False
