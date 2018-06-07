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

    def state_transfer(self, storage, next_state_name):
        storage['state'] = next_state_name
