def init(storage):
    storage['win_time'] = 0
    storage['lose_time'] = 0


def load(stat, storage):
    # group1 基础设施准备
    storage['path_time'] = []
    distance_divide_factor = 4
    max_len = 8
    small_len = 6
    # 基础设施准备
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    from random import choice, randrange

    # 计算距离
    def dist(me, enemy):
        return abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y'])

    # 领地内游走函数
    def wander(field, me, storage):
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction']][0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不出界
        nexty = me['y'] + directions[me['direction']][1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = choice('rl')
            storage['maxl'] = max(
                randrange(small_len, max_len),
                dist(me, storage['enemy']) // distance_divide_factor)
            return ''

        # 随机前进，转向频率递减
        # if randrange(storage['count']) == 0:
        #     storage['count'] += 3
        #     return choice('rl')
        # 倾向于进攻的前进
        from AI.DSA_group1_package.attack import attack
        return attack(stat, storage, last_path=None)

    # 领地外画圈
    def square(field, me, storage):
        # 防止出界
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction']][1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction']][0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return

        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 返回领地中心
    def goback(field, me, storage):
        # 第一步掉头
        if storage['turn']:
            res, storage['turn'] = storage['turn'], None
            return res

        # 状态转换
        elif field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['maxl'] = max(
                randrange(4, 7),
                dist(me, storage['enemy']) // distance_divide_factor)
            storage['turn'] = choice('rl')
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > small_len:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return choice('rl1234')

    # 写入模块
    storage['wander'] = wander
    storage['square'] = square
    storage['goback'] = goback

    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
    storage['count'] = 2


def play(stat, storage):
    storage['path'] = {'me': {'me': [None], 'enemy': [None, None]},
                       'enemy': {'enemy': [None], 'me': [None, None]}}
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    return curr_mode(field, me, storage)


def summary(match_result, stat, storage):
    if match_result[0] == stat['now']['me']['id']:
        storage['win_time'] += 1
        storage['lose_time'] += 1

    print(match_result)
    print('Find_path time: %4.4f' % sum(storage['path_time']))
    print()
    print()


def summaryn(storage):
    print("me win time: %d" % storage['win_time'])
    print("me lose time: %d" % storage['lose_time'])
