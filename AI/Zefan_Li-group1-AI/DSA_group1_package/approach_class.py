from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.find_path import path_to
from AI.DSA_group1_package.gen_func import *

import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'

LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'

MINDISTANCE = 6

def me_and_enemy_easy(stat, storage):
    return abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(
        stat['now']['me']['y'] - stat['now']['me']['y'])


def to_enemy_fields_easy(inx, iny, stat, storage):
    mindis = 99999
    for x in range(0, stat['size'][0]):
        for y in range(0, stat['size'][1]):
            if stat['now']['fields'][x][y] == stat['now']['enemy']['id']:
                temp = abs(x - inx) + abs(y - iny)
                mindis = min(temp, mindis)
    return mindis

def abs_distance(x1,y1,x2,y2):
    return abs(x2-x1)+abs(y2-y1)

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Approach(State):

    def approach_wrapper(self, stat, storage, way):
        out = move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[way])
        testlist = [(stat['now']['me']['x'] - 1, stat['now']['me']['y']),
                    (stat['now']['me']['x'] + 1, stat['now']['me']['y']),
                    (stat['now']['me']['x'], stat['now']['me']['y'] - 1),
                    (stat['now']['me']['x'], stat['now']['me']['y'] + 1)]
        flag = False
        for test in testlist:
            if test[0] > 0 and test[0] < stat['size'][0] and test[1] > 0 and test[1] < stat['size'][1]:
                if stat['now']['fields'][test[0]][test[1]] != stat['now']['me']['id']:
                    flag = True
                    break
        if not flag:
            return way
        if fail_check(stat, storage, *out) != 0 and dying_check(stat, storage, *out) != 0 and me_and_enemy_easy(stat, storage) >= MINDISTANCE:
            return way
        list1 = [RIGHT,LEFT,MIDDLE]
        list2 = [a for a in list1 if fail_check(stat,storage,\
                *move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[a])) != 0]
        list3 = [a for a in list2 if dying_check(stat,storage,\
                *move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[a])) != 0]
        list4 = []
        for a in list3:
            if abs_distance(stat['now']['enemy']['x'],stat['now']['enemy']['y'],\
                         *move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[a])) >= 5:
                list4.append(a)
        if len(list4) == 1 :
            return list4[0]
        if len(list4) > 1:
            return min(*list4 ,key = lambda x : abs_distance(stat['now']['enemy']['x'],stat['now']['enemy']['y'],\
                         *move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[x])))
        #list4==[]
        if len(list3) == 1 :
            return list3[0]
        if len(list3) > 1:
            for a in list3:
                temp = move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[a])
                if stat['now']['fields'][temp[0]][temp[1]] == stat['now']['me']['id']:
                    return a
            return max(*list3 ,key = lambda x : abs_distance(stat['now']['enemy']['x'],stat['now']['enemy']['y'],\
                         *move(stat['now']['me']['x'], stat['now']['me']['y'],stat['now']['me']['direction'] + direction_dict[x])))
        #list3==[]
        if list2 == []:
            return random.choice(list1)
        else:
            return random.choice(list2)





    def init_output(self, stat, storage, last_stat_name):
        if me_and_enemy_easy(stat, storage) > 4 :
            self.store['approach_type'] = 'Attack'
            return self.approach_wrapper(stat, storage, self.init_output_attack(stat, storage, last_stat_name))
        else:
            self.store['approach_type'] = 'Invade'
            return self.approach_wrapper(stat, storage, self.init_output_invade(stat, storage))

    def init_output_invade(self, stat, storage):
        choose = [LEFT, RIGHT, MIDDLE]
        count = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        min = 999
        choose_list = []
        for i in range(0, 3):
            newx, newy = stat['now']['me']['x'], stat['now']['me']['y']
            while True:
                newx, newy = move(newx, newy, direction_dict[choose[i]] + stat['now']['me']['direction'])
                if newx < 0 or newy < 0 or newx >= stat['size'][0] or newy >= stat['size'][1]:
                    break
                if stat['now']['fields'][newx][newy] != stat['now']['me']['id']:
                    count[i][1] = count[i][0]
                    count[i][2] = abs(newx - stat['now']['enemy']['x']) + abs(newy - stat['now']['me']['y'])
                    if count[i][2] < min:
                        min = count[i][2]
                    choose_list.append((choose[i], count[i][1] , count[i][2]))
                    break
                count[i][0] += 1
        choose = [x for x in choose_list if x[2] != min]
        min = [999, MIDDLE]
        for element in choose:
            if element[1] < min[0]:
                min[0] = element[1]
                min[1] = element[0]
        return min[1]

    def init_output_attack(self, stat, storage, last_state_name):
        me = stat['now']['me']
        (enex, eney) = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])
        forward = abs(me['x'] + directions[me['direction']][0] - enex) + abs(
            me['y'] + directions[me['direction']][1] - eney)
        turnleft = abs(me['x'] + directions[me['direction'] - 1][0] - enex) + abs(
            me['y'] + directions[me['direction'] - 1][1] - eney)
        turnright = abs(me['x'] + directions[me['direction'] - 3][0] - enex) + abs(
            me['y'] + directions[me['direction'] - 3][1] - eney)
        if forward <= turnleft and forward <= turnright:
            return MIDDLE
        elif turnleft < forward and turnleft < turnright:
            return LEFT
        elif turnright < forward and turnright < turnleft:
            return RIGHT
        else:
            if me['direction'] % 2:
                le = me['x'] + directions[me['direction'] - 1][0]
                if le < 0 or le >= stat['size'][0]:
                    return RIGHT
                else:
                    return LEFT
            else:
                le = me['y'] + directions[me['direction'] - 1][1]
                if le < 0 or le >= stat['size'][1]:
                    return RIGHT
                else:
                    return LEFT

    def subquent_output(self, stat, storage):
        if self.store['approach_type'] == 'Attack':
            return self.approach_wrapper(stat, storage, self.subquent_output_attack(stat, storage))
        else:
            return self.approach_wrapper(stat, storage, self.subquent_output_invade(stat, storage))

    def subquent_output_invade(self, stat, storage):
        return MIDDLE

    def subquent_output_attack(self, stat, storage):
        me = stat['now']['me']
        (enex, eney) = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])
        forward = abs(me['x'] + directions[me['direction']][0] - enex) + abs(
            me['y'] + directions[me['direction']][1] - eney)
        turnleft = abs(me['x'] + directions[me['direction'] - 1][0] - enex) + abs(
            me['y'] + directions[me['direction'] - 1][1] - eney)
        turnright = abs(me['x'] + directions[me['direction'] - 3][0] - enex) + abs(
            me['y'] + directions[me['direction'] - 3][1] - eney)
        if forward <= turnleft and forward <= turnright:
            return MIDDLE
        elif turnleft < forward and turnleft < turnright:
            return LEFT
        elif turnright < forward and turnright < turnleft:
            return RIGHT
        else:
            if me['direction'] % 2:
                le = me['x'] + directions[me['direction'] - 1][0]
                if le < 0 or le >= stat['size'][0]:
                    return RIGHT
                else:
                    return LEFT
            else:
                le = me['y'] + directions[me['direction'] - 1][1]
                if le < 0 or le >= stat['size'][1]:
                    return RIGHT
                else:
                    return LEFT

    def trans_where(self, stat, storage, outcome=None):
        if storage[ATTACK].if_transfer_in(stat, storage):
            return ATTACK
        elif storage[ENCLOSE].if_transfer_in(stat, storage):
            return ENCLOSE
        else:
            return self.name

    def if_transfer_in(self, stat, storage):
        me = stat['now']['me']
        if stat['now']['fields'][me['x']][me['y']] == me['id']:
            return True
        else:
            return False
