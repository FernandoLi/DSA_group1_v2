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

class Enclose(State):

    def init_output(self, stat, storage, last_state_name):
        me, ene = stat['now']['me'], stat['now']['enemy']
        storage['store'][ENCLOSE]['maxi'] = (abs(me['x'] - ene['x']) + abs(me['y'] - ene['y'])) // 8
        storage['store'][ENCLOSE]['turn'] = LEFT
        storage['store'][ENCLOSE]['cacu'] = 0
        storage['store'][ENCLOSE]['count'] = 0
        # step1: 处理几种进入状态的case：enclose, attack, approach, retreat
        # step2: 根据现在的情况计算出一个路径/或者一个输出值，这个自己看。但是必须有一个返回值
        # return 0  # 路径的第一个值
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            leftx = me['x'] + directions[me['direction'] - 1][0]
            if nexty < 0 or nexty >= stat['size'][1]:
                storage['store'][ENCLOSE]['count'] = 0
                storage['store'][ENCLOSE]['cacu'] += 1
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            lefty = me['y'] + directions[me['direction'] - 1][1]
            if nextx < 0 or nextx >= stat['size'][0]:
                storage['store'][ENCLOSE]['count'] = 0
                storage['store'][ENCLOSE]['cacu'] += 1
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        storage['store'][ENCLOSE]['count'] += 1
        if storage['store'][ENCLOSE]['count'] >= storage['store'][ENCLOSE]['maxi']:
            storage['store'][ENCLOSE]['count'] = 0
            storage['store'][ENCLOSE]['cacu']+=1
            if me['direction'] % 2:
                leftx = me['x'] + directions[me['direction'] - 1][0]
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
            else:
                lefty = me['y'] + directions[me['direction'] - 1][1]
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:
            return MIDDLE

    def enclone(self, stat, storage):
        me, ene = stat['now']['me'], stat['now']['enemy']
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            leftx = me['x'] + directions[me['direction'] - 1][0]
            if nexty < 0 or nexty >= stat['size'][1]:
                storage['store'][ENCLOSE]['count'] = 0
                storage['store'][ENCLOSE]['cacu'] += 1
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            lefty = me['y'] + directions[me['direction'] - 1][1]
            if nextx < 0 or nextx >= stat['size'][0]:
                storage['store'][ENCLOSE]['count'] = 0
                storage['store'][ENCLOSE]['cacu'] += 1
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        storage['store'][ENCLOSE]['count'] += 1
        if storage['store'][ENCLOSE]['count'] >= storage['store'][ENCLOSE]['maxi']:
            storage['store'][ENCLOSE]['count'] = 0
            storage['store'][ENCLOSE]['cacu'] += 1
            if me['direction'] % 2:
                leftx = me['x'] + directions[me['direction'] - 1][0]
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
            else:
                lefty = me['y'] + directions[me['direction'] - 1][1]
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['store'][ENCLOSE]['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:
            return MIDDLE

    def encltwo(self, stat, storage):
        me, ene = stat['now']['me'], stat['now']['enemy']
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= stat['size'][1]:
                storage['store'][ENCLOSE]['count'] = 0
                return storage['store'][ENCLOSE]['turn']
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= stat['size'][0]:
                storage['store'][ENCLOSE]['count'] = 0
                return storage['store'][ENCLOSE]['turn']
        storage['store'][ENCLOSE]['count'] += 1
        if storage['store'][ENCLOSE]['count'] >= storage['store'][ENCLOSE]['maxi'] - 1:
            storage['store'][ENCLOSE]['count'] = 0
            return storage['store'][ENCLOSE]['turn']
        else:
            return 'M'

    def subquent_output(self, stat, storage):
        if storage['store'][ENCLOSE]['cacu'] < 4:
            return self.enclone(stat, storage)
        elif storage['store'][ENCLOSE]['cacu'] == 4:
            storage['store'][ENCLOSE]['cacu'] += 1
            storage['store'][ENCLOSE]['count'] = 0
            return RIGHT
        else:
            return self.encltwo(stat, storage)


        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。
        # return


    def trans_where(self, stat, storage, outcome=None):
        me, ene = stat['now']['me'], stat['now']['enemy']
        if storage['store'][ENCLOSE]['cacu'] < 4:
            return self.name
        elif storage['store'][ENCLOSE]['cacu']==4:
            if stat['now']['fields'][me['x']][me['y']] != me['id']:
                return RETREAT
            if storage['store'][ENCLOSE]['turn'] == 'Right':
                # 变成approach
                return APPROACH
            else:
                return self.name
        else:
            if stat['now']['fields'][me['x']][me['y']] == me['id']:
                return APPROACH
            else:
                return self.name



