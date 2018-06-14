def load(stat, storage):
    # 定义四个状态名字常量
    ATTACK = 'attack'
    ENCLOSE = 'enclose'
    APPROACH = 'approach'
    RETREAT = 'retreat'

    # 开辟四个状态用的缓存空间
    storage['store'] = {}
    storage['store'][ATTACK] = {}
    storage['store'][ENCLOSE] = {}
    storage['store'][APPROACH] = {}
    storage['store'][RETREAT] = {}

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

    # 存储双方的纸带：
    storage['bands'] = {}
    storage['bands']['me'] = []
    storage['bands']['enemy'] = []

    '''一般情况下，用于debug的代码'''
    # debug 记录每一回合调用了什么状态
    storage['state_record'] = [(0, None)]
    f = open('./AI/log/state_main_state_transfer.txt', 'w')
    storage['f'] = f
    # debug


def play(stat, storage):
    from AI.DSA_group1_package.find_path import path_to
    from AI.DSA_group1_package.gen_func import record_bands
    # import time

    # 记录双方的纸带
    record_bands(stat, storage, 'me')
    record_bands(stat, storage, 'enemy')

    # 计算四个路径并且计时
    # t1 = time.time()
    storage['me_me_fields'] = None
    storage['me_enemy_bands'] = None
    storage['enemy_enemy_fields'] = None
    storage['enemy_me_bands'] = None

    storage['me_me_fields'] = path_to(stat, storage, 'me_me_fields')
    storage['me_enemy_bands'] = path_to(stat, storage, 'me_enemy_bands')
    storage['enemy_enemy_fields'] = path_to(stat, storage, 'enemy_enemy_fields')
    storage['enemy_me_bands'] = path_to(stat, storage, 'enemy_me_bands', storage['me_me_fields'][2])

    '''find_path后手bug，debug代码'''
    #
    # # debug
    # storage['me_me_fields'] = path_to(stat, storage, 'me_me_fields')
    # storage['me_enemy_bands'] = path_to(stat, storage, 'me_enemy_bands')
    # storage['enemy_enemy_fields'] = path_to(stat, storage, 'enemy_enemy_fields')
    # storage['enemy_me_bands'] = path_to(stat, storage, 'enemy_me_bands')
    #
    # me_id = stat['now']['me']['id']  # 这里原来是bug啊，list的0元素是先手玩家，1元素是后手玩家
    # me_turn = 2 * (2000 - stat['now']['turnleft'][me_id - 1] + 1)  # 综合两方面的turn
    # print('(%d, %s)' % (me_turn, storage['state']))
    #
    # mmf = storage['me_me_fields']
    # meb = storage['me_enemy_bands']
    # eef = storage['enemy_enemy_fields']
    # emb = storage['enemy_me_bands']
    # print("me_me_fields, me_enemy_bands, enemy_enemy_fields, enemy_me_bands, = %d, %d, %d, %d" %
    #       (mmf[0], meb[0], eef[0], emb[0]))
    # print(mmf[2])
    # print(meb[2])
    # print(eef[2])
    # print(emb[2])
    # print()
    # # debug

    '''记录path_to时间代码'''
    # t2 = time.time()

    # try:
    #     storage['sumtime']
    # except KeyError:
    #     storage['sumtime'] = 0
    # storage['sumtime'] += (t2 - t1)

    '''真正的执行语句'''
    curr_state_name = storage['state']
    curr_state = storage[curr_state_name]
    me_id = stat['now']['me']['id']  # 这里原来是bug啊，list的0元素是先手玩家，1元素是后手玩家
    if stat['now']['turnleft'][me_id - 1] == 2000:
        outcome = curr_state.output_func(stat, storage, None)
    else:
        outcome = curr_state.output_func(stat, storage, curr_state_name)

    '''一般情况下，用于debug的代码'''
    # debug
    # 记录我是第几局用了什么状态，计算出的输出，本局计算出的输出包括在内。
    # 准备输出这一局计算的几个路径
    mmf = storage['me_me_fields']
    meb = storage['me_enemy_bands']
    eef = storage['enemy_enemy_fields']
    emb = storage['enemy_me_bands']

    me_turn = 2 * (2000 - stat['now']['turnleft'][me_id - 1] + 1) - 1  # 综合两方面的turn
    # me_turn = (2000 - stat['now']['turnleft'][me_id] + 1)  # 自己单方面的 turn
    state_record = storage['state_record']

    if state_record[-1][1] != storage['state']:
        state_record.append((me_turn, storage['state']))
        print('(%d, %s)' % (me_turn, storage['state']))
        print("me_me_fields, me_enemy_bands, enemy_enemy_fields, enemy_me_bands, = %d, %d, %d, %d" %
              (mmf[0], meb[0], eef[0], emb[0]))
        print(mmf[2])
        print(meb[2])
        print(eef[2])
        print(emb[2])
        print()
        storage['f'].write('(%d, %s)\n' % (me_turn, storage['state']))
        storage['f'].write("me_me_fields, me_enemy_bands, enemy_enemy_fields, enemy_me_bands, = %d, %d, %d, %d\n" %
                           (mmf[0], meb[0], eef[0], emb[0]))
    # debug
    return outcome


def summary(match_result, stat, storage):
    '''一般情况下，用于debug的代码'''

    print('VS Begin!')
    # 打印path_to时间
    print('time of path_to:', storage['sumtime'])
    print()
    storage['f'].close()

    '''最后汇总输出状态转移情况'''
    # # 打印第几局是什么state计算的输出
    # state_record = storage['state_record']
    # for i in state_record:
    #     print(i)
    pass


def init(storage):
    pass


def summaryall(storage):
    pass
