from AI.DSA_group1_package.state_class import State
import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'

LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
class Approach(State):

    def init_output(self, stat, storage, last_state_name):
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

    def subquent_output(self, stat, storage):
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

