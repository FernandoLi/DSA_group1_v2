def play(stat, storage):
    from AI.DSA_group1_package.find_path import path_to
    import time
    # 初始化，这次用于新的find_path剪枝的debug
    # storage['path'] = {'me': {'me': [None], 'enemy': [None, None]},
    #                    'enemy': {'enemy': [None], 'me': [None, None]}}

    # 初始化
    from AI.DSA_group1_package import gen_func

    # 清空上次计算的最短路径，这个不够优化，以后不要清空，要加以利用
    storage['me_me_fields'] = None
    storage['me_enemy_bands'] = None
    storage['enemy_enemy_fields'] = None
    storage['enemy_me_bands'] = None

    LEFT = 'L'
    RIGHT = 'R'
    MIDDLE = 'M'

    # 记录纸带list
    gen_func.record_bands(stat, storage, 'me')
    gen_func.record_bands(stat, storage, 'enemy')
    # 初始化

    storage['enemy'] = stat['now']['enemy']
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']

    t1 = time.time()
    a = path_to(stat, storage, 'me_me_fields')
    b = path_to(stat, storage, 'me_enemy_bands')
    c = path_to(stat, storage, 'enemy_enemy_fields')
    d = path_to(stat, storage, 'enemy_me_bands')
    # a = path_to(stat, storage, 'me', 'me', 'fields')
    # b = path_to(stat, storage, 'me', 'enemy', 'bands')
    # c = path_to(stat, storage, 'enemy', 'enemy', 'fields')
    # d = path_to(stat, storage, 'enemy', 'me', 'bands')
    t2 = time.time()

    # debug
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # debug

    try:
        storage['sumtime']
    except KeyError:
        storage['sumtime'] = 0

    storage['sumtime'] += (t2 - t1)
    # if a is not None and b is not None and c is not None and d is not None:
    return curr_mode(field, me, storage)
    # else:
    #     return 'x'


def load(stat, storage):
    # 定义四个状态名字常量
    ATTACK = 'attack'
    ENCLOSE = 'enclose'
    APPROACH = 'approach'
    RETREAT = 'retreat'

    # 开辟四个状态用的缓存空间
    storage['store'] = {}
    storage['store'][ATTACK] = None
    storage['store'][ENCLOSE] = None
    storage['store'][APPROACH] = None
    storage['store'][RETREAT] = None

    # 定义四个状态的类
    from AI.DSA_group1_package.attack_class import Attack
    from AI.DSA_group1_package.enclose_class import Enclose
    from AI.DSA_group1_package.approach_class import Approach
    from AI.DSA_group1_package.retreat_class import Retreat

    storage[ATTACK] = Attack(name=ATTACK, store=storage['store'][ATTACK])
    storage[ENCLOSE] = Enclose(name=ENCLOSE, store=storage['store'][ENCLOSE])
    storage[APPROACH] = Approach(name=APPROACH, store=storage['store'][APPROACH])
    storage[RETREAT] = Retreat(name=RETREAT, store=storage['store'][RETREAT])

    # storage['state']记录当前状态的名字
    storage['state'] = APPROACH
    storage['last_state'] = None

    storage['bands'] = {'me': [], 'enemy': []}
    # 这个空间记录自己（敌人）纸带的list，list中的每一个元素是一个坐标（x, y）
    # 其中list的最后一个元素是头而不是纸带，注意！list中第一个元素离纸带头的坐标距离最远，然后依次递减

    # debug
    storage['dead_time'] = []
    # debug


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
                randrange(4, 7),
                dist(me, storage['enemy']) // 5)
            return ''

        # 随机前进，转向频率递减
        if randrange(storage['count']) == 0:
            storage['count'] += 3
            return choice('rl')

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
                dist(me, storage['enemy']) // 5)
            storage['turn'] = choice('rl')
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > 4:
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


def summary(match_result, stat, storage):
    # print('Find_path time: %4.4f' % sum(storage['path_time']))
    # print('copy time: ', storage['copytime'])
    # print('calculate time: ', storage['caltime'])
    print('time of path_to:', storage['sumtime'])
    print('cycle end')
    print()
