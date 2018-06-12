from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.gen_func import *
from AI.DSA_group1_package.find_path import *

ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'

LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))


def me_and_enemy_easy(stat, storage):
    return abs(stat['now']['me']['x'] - stat['now']['enemy']['x']) + abs(
        stat['now']['me']['y'] - stat['now']['me']['y'])


class Enclose(State):

    def init_output(self, stat, storage, last_state_name):
        self.store['enclose_init'] = 'square'
        return self.init_output_square(stat, storage, last_state_name)

    def init_output_square(self, stat, storage, last_state_name):
        if me_and_enemy_easy(stat, storage) >= 8:
            self.store['square_type'] = 'Attack'
        else:
            self.store['square_type'] = 'Defend'

        left = move(stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction'] + direction_dict[LEFT])
        right = move(stat['now']['me']['x'], stat['now']['me']['y'], stat['now']['me']['direction'] + direction_dict[RIGHT])
        leftdis = abs(left[0] - stat['now']['enemy']['x']) + abs(left[1] - stat['now']['me']['y'])
        rightdis = abs(right[0] - stat['now']['enemy']['x']) + abs(right[1] - stat['now']['me']['y'])
        if leftdis < rightdis:
            if self.store['square_type'] == 'Attack':
                self.store['turn'] = LEFT
            else:
                self.store['turn'] = RIGHT
        else:
            if self.store['square_type'] == 'Attack':
                self.store['turn'] = RIGHT
            else:
                self.store['turn'] = LEFT

        rank = (me_and_enemy_easy(stat, storage) // 4) + 1
        while True:
            point_test = stat['now']['me']['x'], stat['now']['me']['y']
            for i in range(0, rank - 2):
                point_test = move(point_test[0], point_test[1], stat['now']['me']['direction'])
            point_test = move(point_test[0], point_test[1],
                stat['now']['me']['direction'] + direction_dict[self.store['turn']])
            for i in range(0, rank - 2):
                point_test = move(point_test[0], point_test[1],
                    stat['now']['me']['direction'] + direction_dict[self.store['turn']])
            if point_test[0] > 0 and point_test[0] < stat['size'][0] and point_test[1] > 0 and point_test[1] < \
                    stat['size'][1]:
                break
            else:
                rank -= 1
        if rank <= 2:
            rightpos = move(stat['now']['me']['x'], stat['now']['me']['y'], direction_dict[RIGHT])
            if rightpos[0] > 0 and rightpos[0] < stat['size'][0] and rightpos[1] > 0 and rightpos[1] < stat['size'][1]:
                self.store['enclose_path'] = [RIGHT, RIGHT]
                return RIGHT
            else:
                self.store['enclose_path'] = [LEFT, LEFT]
                return LEFT
        self.store['rank'] = rank
        self.store['enclose_path'] = list(
            MIDDLE * (rank - 2) + 'T' + MIDDLE * (rank - 2) + self.store['turn'] + MIDDLE * (rank - 2) + self.store[
                'turn'] + MIDDLE * (rank - 2))
        return self.store['enclose_path'].pop(0)

    def subquent_output(self, stat, storage):
        return self.subquent_output_square(stat, storage)

    def subquent_output_square(self, stat, storage):
        if self.store['enclose_path'][0] == MIDDLE:
            return self.store['enclose_path'].pop(0)
        elif self.store['enclose_path'][0] == 'T':
            if me_and_enemy_easy(stat, storage) >= 3 * self.store['rank'] - 1:
                self.store['rank'] += 1
                point_test = stat['now']['me']['x'], stat['now']['me']['y']
                for i in range(0, self.store['rank'] - 2):
                    point_test = move(point_test[0], point_test[1], stat['now']['me']['direction'])
                point_test = move(point_test[0], point_test[1],
                    stat['now']['me']['direction'] + direction_dict[self.store['turn']])
                for i in range(0, self.store['rank'] - 2):
                    point_test = move(point_test[0], point_test[1],
                        stat['now']['me']['direction'] + direction_dict[self.store['turn']])
                if point_test[0] > 0 and point_test[0] < stat['size'][0] and point_test[1] > 0 and point_test[1] < \
                        stat['size'][1]:
                    self.store['enclose_path'] = list(
                        'T' + MIDDLE * (self.store['rank'] - 2) + self.store['turn'] + MIDDLE * (
                                self.store['rank'] - 2) + self.store['turn'] + MIDDLE * (self.store['rank'] - 2))
                    return MIDDLE
                else:
                    self.store['rank'] -= 1
                    self.store['enclose_path'].pop(0)
                    return self.store['turn']
            else:
                self.store['enclose_path'].pop(0)
                return self.store['turn']
        else:
            return self.store['enclose_path'].pop(0)

    def trans_where(self, stat, storage, outcome=None):
        return self.trans_where_square(stat, storage, outcome)

    def trans_where_square(self, stat, storage, outcome):
        # 条件1，目前的体检看似没问题
        if storage[ATTACK].if_transfer_in_win(stat, storage):
            return ATTACK
        elif storage[RETREAT].if_transfer_in(stat, storage):
            return RETREAT
        elif storage[APPROACH].if_transfer_in(stat, storage):
            return APPROACH
        else:
            return ENCLOSE
        # 条件2，应用这个条件，会莫名其妙，当自己与敌人距离很远的时候依然只会右转。
        '''
        if storage[ATTACK].if_transfer_in_win(stat, storage):
            return ATTACK
        elif storage[RETREAT].if_transfer_in(stat, storage):
            return RETREAT
        elif storage[APPROACH].if_transfer_in(stat, storage):
            return APPROACH
        elif self.store['enclose_path']:
            return ENCLOSE
        else:
            return RETREAT
        '''
        # 条件3 用这个条件，进入领地之后也不会继续圈地
        '''
        if storage[ATTACK].if_transfer_in_win(stat, storage):
            return ATTACK
        elif storage[RETREAT].if_transfer_in(stat, storage):
            return RETREAT
        elif self.store['enclose_path']:
            return ENCLOSE
        else:
            return APPROACH
        '''

    def if_transfer_in(self, stat, storage):
        me = stat['now']['me']
        if stat['now']['fields'][me['x']][me['y']] != me['id']:
            return True
        else:
            return False
