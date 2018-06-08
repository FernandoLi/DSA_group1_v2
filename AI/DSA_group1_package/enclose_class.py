from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.gen_func import *
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'

LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

def me_and_enemy_easy(stat,storage):
    return abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(stat['now']['me']['y'] - stat['now']['me']['y'])

class Enclose(State):

    def init_output(self,stat,storage,last_state_name):
        if me_and_enemy_easy(stat,storage)<=12:
            storage['enclose_init'] = 'eight'
            return self.init_output_eight(stat, storage, last_state_name)
        else:
            storage['enclose_init'] = 'square'
            return self.init_output_square(stat,storage,last_state_name)

    def init_output_square(self,stat,storage,last_state_name):
        if me_and_enemy_easy(stat,storage)>=8:
            storage['square_type'] = 'Attack'
        else:
            storage['square_type'] = 'Defend'

        left = move(stat['now']['me']['x'], stat['now']['me']['y'], direction_dict[LEFT])
        right = move(stat['now']['me']['x'], stat['now']['me']['y'], direction_dict[RIGHT])
        leftdis = abs(left[0] - stat['now']['enemy']['x']) + abs(left[1] - stat['now']['me']['y'])
        rightdis = abs(right[0] - stat['now']['enemy']['x']) + abs(right[1] - stat['now']['me']['y'])
        if leftdis < rightdis:
            if storage['square_type'] == 'Attack':
                storage['turn'] = LEFT
            else:
                storage['turn'] = RIGHT
        else:
            if storage['square_type'] == 'Attack':
                storage['turn'] = RIGHT
            else:
                storage['turn'] = LEFT

        rank = me_and_enemy_easy(stat,storage)//4 + 1
        while True:
            point_test = (stat['now']['me']['x'],stat['now']['me']['y'])+(rank-2)*directions[stat['now']['me']['direction']]
            point_test = move(point_test[0],point_test[1],direction_dict[storage['turn']])
            point_test = point_test + (rank-2)*directions[(stat['now']['me']['direction']+direction_dict[storage['turn']])%4]
            print(point_test)
            if point_test[0] >0 and point_test[0] < stat['size'][0] and point_test[1] >0 and point_test[1] < stat['size'][1]:
                break
            else:
                rank -= 1
        storage['rank'] = rank
        storage['enclose_path'] = list(MIDDLE*(rank-2)+'T'+MIDDLE*(rank-2)+storage['turn']+MIDDLE*(rank-2)+storage['turn']+MIDDLE*(rank-2))
        print(stat['now']['turnleft'][0],storage['enclose_path'])
        return storage['enclose_path'].pop(0)

    def init_output_eight(self, stat, storage, last_state_name):
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

    def subquent_output(self, stat, storage):
        if storage['enclose_init'] == 'eight':
            return self.subquent_output_eight(stat,storage)
        else:
            return self.subquent_output_square(stat,storage)

    def subquent_output_square(self,stat,storage):
        print(2000-stat['now']['turnleft'][0],storage['enclose_path'])
        if storage['enclose_path'][0] == MIDDLE:
            return storage['enclose_path'].pop(0)
        elif storage['enclose_path'][0] == 'T':
            if me_and_enemy_easy(stat,storage) >= 3*storage['rank']-1:
                storage['rank'] += 1
                point_test = (stat['now']['me']['x'], stat['now']['me']['y']) + (storage['rank'] - 2) * directions[stat['now']['me']['direction']]
                point_test = move(point_test[0], point_test[1], direction_dict[storage['turn']])
                point_test = point_test + (storage['rank'] - 2) * directions[(stat['now']['me']['direction'] + direction_dict[storage['turn']]) % 4]
                if point_test[0] > 0 and point_test[0] < stat['size'][0] and point_test[1] > 0 and point_test[1] <stat['size'][1]:
                    storage['enclose_path'] = list('T'+MIDDLE*(storage['rank']-2)+storage['turn']+MIDDLE*(storage['rank']-2)+storage['turn']+MIDDLE*(storage['rank']-2))
                    return MIDDLE
                else:
                    storage['rank'] -= 1
                    storage['enclose_path'].pop(0)
                    return storage['turn']
            else :
                storage['enclose_path'].pop(0)
                return storage['turn']
        else:
            return storage['enclose_path'].pop(0)

    def enclone_eight(self, stat, storage):
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

    def encltwo_eight(self, stat, storage):
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

    def subquent_output_eight(self, stat, storage):
        if storage['store'][ENCLOSE]['cacu'] < 4:
            return self.enclone_eight(stat, storage)
        elif storage['store'][ENCLOSE]['cacu'] == 4:
            storage['store'][ENCLOSE]['cacu'] += 1
            storage['store'][ENCLOSE]['count'] = 0
            return RIGHT
        else:
            return self.encltwo_eight(stat, storage)

        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。
        # return

    def trans_where(self , stat,storage,outcome=None):
        if storage['enclose_init'] == 'eight':
            return self.trans_where_eight(stat,storage,outcome)
        else:
            return self.trans_where_square(stat,storage,outcome)
    def trans_where_square(self,stat,storage,outcome):
        if False:
            return ATTACK
        elif False:
            return RETREAT
        elif storage['enclose_path']:
            return ENCLOSE
        else:
            return APPROACH
    def trans_where_eight(self, stat, storage, outcome=None):
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



