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


    # 这里如果需要新的初始化函数，可以这样写，不用的话可以省略。
    # def __init__(self, name, store):  # store = storage['statename_store']
    #     super(State, self).__init__(name, store)

    def output_func(self, stat, storage, last_state_name):
        if self.name != last_state_name:
            # 上一轮的状态和这一轮的状态不一致时

            outcome = self.init_output(stat, storage, last_state_name)

            next_state_name = self.trans_where(stat, storage)  # 需要根据当前的状态
            self.state_transfer(storage, next_state_name)

            pass  # 意思是，状态转换，首次调用一定要有要返回值，outcome保留到底

        else:
            next_state_name = self.trans_where(stat, storage)  # 需要根据当前的状态

            if next_state_name == self.name:
                # 上一轮的状态和这一轮一致时：
                outcome = self.subquent_output(stat, storage)  # 我预想O(1)的复杂度

                pass  # 意思是，事件继续了，所以用这个outcome

            else:
                # 如果状态转换了，那么交给笑一个函数的init_output来返回值

                self.state_transfer(storage, next_state_name)

                outcome = storage[next_state_name].output_func(stat, storage, self.name)

                pass  # 这时候outcome就是下一状态init_output计算出来的值

        return outcome

    def init_output(self, stat, storage, last_state_name):

        me, ene = stat['now']['me'], stat['now']['enemy']
        storage['maxi'] = (abs(me['x'] - ene['x']) + abs(me['y'] - ene['y'])) // 8
        storage['turn'] = LEFT
        storage['cacu'] = 0
        storage['count'] = 0
        # step1: 处理几种进入状态的case：enclose, attack, approach, retreat
        # step2: 根据现在的情况计算出一个路径/或者一个输出值，这个自己看。但是必须有一个返回值
        # return 0  # 路径的第一个值
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            leftx = me['x'] + directions[me['direction'] - 1][0]
            if nexty < 0 or nexty >= stat['size'][1]:
                storage['count'] = 0
                storage['cacu'] += 1
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            lefty = me['y'] + directions[me['direction'] - 1][1]
            if nextx < 0 or nextx >= stat['size'][0]:
                storage['count'] = 0
                storage['cacu'] += 1
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        storage['count'] += 1
        if storage['count'] >= storage['maxi']:
            storage['count'] = 0
            storage['cacu']+=1
            if me['direction'] % 2:
                leftx = me['x'] + directions[me['direction'] - 1][0]
                if leftx < 0 or leftx >= stat['size'][0]:
                    storage['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
            else:
                lefty = me['y'] + directions[me['direction'] - 1][1]
                if lefty < 0 or lefty >= stat['size'][1]:
                    storage['turn'] = RIGHT
                    return RIGHT
                else:
                    return LEFT
        else:
            return MIDDLE

    def subquent_output(self, stat, storage):
        me, ene = stat['now']['me'], stat['now']['enemy']
        def enclone(stat, storage):
            if me['direction'] % 2:  # y轴不出界
                nexty = me['y'] + directions[me['direction']][1]
                leftx = me['x'] + directions[me['direction'] - 1][0]
                if nexty < 0 or nexty >= stat['size'][1]:
                    storage['count'] = 0
                    storage['cacu'] += 1
                    if leftx < 0 or leftx >= stat['size'][0]:
                        storage['turn'] = RIGHT
                        return RIGHT
                    else:
                        return LEFT
            else:  # x轴不出界
                nextx = me['x'] + directions[me['direction']][0]
                lefty = me['y'] + directions[me['direction'] - 1][1]
                if nextx < 0 or nextx >= stat['size'][0]:
                    storage['count'] = 0
                    storage['cacu'] += 1
                    if lefty < 0 or lefty >= stat['size'][1]:
                        storage['turn'] = RIGHT
                        return RIGHT
                    else:
                        return LEFT
            storage['count'] += 1
            if storage['count'] >= storage['maxi']:
                storage['count'] = 0
                storage['cacu'] += 1
                if me['direction'] % 2:
                    leftx = me['x'] + directions[me['direction'] - 1][0]
                    if leftx < 0 or leftx >= stat['size'][0]:
                        storage['turn'] = RIGHT
                        return RIGHT
                    else:
                        return LEFT
                else:
                    lefty = me['y'] + directions[me['direction'] - 1][1]
                    if lefty < 0 or lefty >= stat['size'][1]:
                        storage['turn'] = RIGHT
                        return RIGHT
                    else:
                        return LEFT
            else:
                return MIDDLE

        def encltwo(stat, storage):
            if me['direction'] % 2:  # y轴不出界
                nexty = me['y'] + directions[me['direction']][1]
                if nexty < 0 or nexty >= stat['size'][1]:
                    storage['count'] = 0
                    return storage['turn']
            else:  # x轴不出界
                nextx = me['x'] + directions[me['direction']][0]
                if nextx < 0 or nextx >= stat['size'][0]:
                    storage['count'] = 0
                    return storage['turn']
            storage['count'] += 1
            if storage['count'] >= storage['maxi']-1:
                storage['count'] = 0
                return storage['turn']
            else:
                return 'M'
        if storage['cacu'] < 4:
            return enclone(stat, storage)
        elif storage['cacu'] == 4:
            storage['cacu'] += 1
            storage['count'] = 0
            return RIGHT
        else:
            return encltwo(stat, storage)


        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。
        # return


    def trans_where(self, stat, storage, outcome=None):
        me, ene = stat['now']['me'], stat['now']['enemy']
        if storage['cacu'] < 4:
            return self.name
        elif storage['cacu']==4:
            if stat['now']['fields'][me['x']][me['y']] != me['id']:
                return RETREAT
            if storage['turn'] == 'Right':
                # 变成approach
                return APPROACH
            else:
                return self.name
        else:
            if stat['now']['fields'][me['x']][me['y']] == me['id']:
                return APPROACH
            else:
                return self.name


    def state_transfer(self, storage, next_state_name):
        storage['state'] = next_state_name
