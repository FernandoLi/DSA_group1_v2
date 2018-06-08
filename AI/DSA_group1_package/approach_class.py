from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.find_path import path_to
from AI.DSA_group1_package.gen_func import *

#import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'

LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'

def me_and_enemy_easy(stat,storage):
    return abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(stat['now']['me']['y'] - stat['now']['me']['y'])

def to_enemy_fields_easy(inx,iny ,stat,storage):
    mindis = 99999
    for x in range(0,stat['size'][0]):
        for y in range(0,stat['size'][1]):
            if stat['now']['fields'][x][y] == stat['now']['enemy']['id']:
                temp = abs(x - inx) + abs(y - iny)
                mindis = min(temp,mindis)
    return mindis

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
class Approach(State):

    def approach_wrapper(self, stat, storage, way):
        out = move(stat['now']['me']['x'],stat['now']['me']['y'] , direction_dict[way])
        testlist =  [(stat['now']['me']['x']-1,stat['now']['me']['y']),(stat['now']['me']['x']+1,stat['now']['me']['y']),\
                     (stat['now']['me']['x'],stat['now']['me']['y']-1),(stat['now']['me']['x'],stat['now']['me']['y']+1)]
        flag = False
        for test in testlist:
            if stat['now']['fields'][test[0]][test[1]] != stat['now']['me']['id']:
                flag = True
                break
        if not flag:
            return way
        if fail_check(stat,storage,*out)!=0 and dying_check(stat,storage,*out) != 0:
            return way
        for method in (LEFT,RIGHT,MIDDLE):
            if way != method:
                return method

    def init_output(self, stat, storage, last_stat_name):
        if me_and_enemy_easy(stat,storage)>2 and to_enemy_fields_easy(stat['now']['me']['x'] , stat['now']['me']['y'],stat,storage)>3:
            storage['approach_type'] = 'Attack'
            return self.approach_wrapper(stat,storage,self.init_output_attack(stat, storage, last_stat_name))
        else:
            storage['approach_type'] = 'Invade'
            return self.approach_wrapper(stat,storage,self.init_output_invade(stat, storage))

    def init_output_invade(self, stat, storage):
        choose = [LEFT,RIGHT,MIDDLE]
        count  = [[0,0,0], [0,0,0],[0,0,0]]
        min = [999,999]
        choose_list = []
        mindis = None
        for i in range(0,3):
            newx,newy = stat['now']['me']['x'],stat['now']['me']['y']
            while newx>0 and newy >0 and newx<stat['size'][0]and newy<stat['size'][1]:
                newx,newy = move(newx, newy, direction_dict[choose[i]] + stat['now']['me']['direction'])
                if stat['now']['fields'][newx][newy] != stat['now']['me']['id']:
                    count[i][1] = count[i][0]
                    count[i][2] = abs(newx - stat['now']['enemy']['x']) + abs(newy - stat['now']['me']['y'])
                    if count[i][2] < min[0]:
                        min[0] = count[i][2]
                        mindis = choose[i]
                    choose_list.append((choose[i],count[i][1]))
                    break
                count[i][0] += 1
        choose = [x for x in choose_list if x[0] != mindis]
        min = [999,MIDDLE]
        for element in choose:
            if element[1]<min[0]:
                min[0] = element[1]
                min[1] = element[0]
        return min[1]





    def init_output_attack(self, stat, storage, last_state_name):
        me = stat['now']['me']
        (enex, eney) = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])
        forward = abs(me['x'] + directions[me['direction']][0] - enex) + abs(me['y'] + directions[me['direction']][1] - eney)
        turnleft = abs(me['x'] + directions[me['direction'] - 1][0] - enex) + abs(me['y'] + directions[me['direction'] - 1][1] - eney)
        turnright = abs(me['x'] + directions[me['direction'] - 3][0] - enex) + abs(me['y'] + directions[me['direction'] - 3][1] - eney)
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

    def subquent_output(self , stat ,storage):
        if storage['approach_type'] == 'Attack':
            return self.approach_wrapper(stat,storage,self.subquent_output_attack(stat, storage))
        else:
            return self.approach_wrapper(stat,storage,self.subquent_output_invade(stat,storage))

    def subquent_output_invade(self , stat , storage):
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
        me = stat['now']['me']
        if False:
            return ATTACK
        if stat['now']['fields'][me['x']][me['y']]!=me['id']:
            return ENCLOSE
        elif False:
            return ATTACK
        else:
            return self.name

