def init(storage):
    # 指标是几就表示第几局
    storage['state_transfer'] = [None]
    storage['min_path'] = [None]
    storage['path_to_time'] = [None]
    storage['match_num'] = 0
    pass
    storage['safe_disc'] = 0


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
    storage['if_new_match'] = True

    # 存储双方的纸带：
    storage['bands'] = {}
    storage['bands']['me'] = []
    storage['bands']['enemy'] = []

    '''用于k20 记录状态的代码'''
    storage['match_num'] += 1
    storage['state_transfer'].append([(0, 'state_before_match')])
    storage['min_path'].append([(None, None, None, None)])
    storage['path_to_time'].append(0)


def play(stat, storage):
    from AI.DSA_group1_package.find_path import path_to
    from AI.DSA_group1_package.gen_func import record_bands
    import time

    # 记录双方的纸带
    record_bands(stat, storage, 'me')
    record_bands(stat, storage, 'enemy')

    # 计算四个路径并且计时
    t1 = time.time()
    storage['me_me_fields'] = None
    storage['me_enemy_bands'] = None
    storage['enemy_enemy_fields'] = None
    storage['enemy_me_bands'] = None

    storage['me_me_fields'] = path_to(stat, storage, 'me_me_fields')
    storage['me_enemy_bands'] = path_to(stat, storage, 'me_enemy_bands')
    storage['enemy_enemy_fields'] = path_to(stat, storage, 'enemy_enemy_fields')
    storage['enemy_me_bands'] = path_to(stat, storage, 'enemy_me_bands', storage['me_me_fields'][2])
    t2 = time.time()

    '''所需要的数据记录'''
    match_num = storage['match_num']
    '''记录path_to时间代码'''
    storage['path_to_time'][match_num] += (t2 - t1)

    '''真正的执行语句'''
    curr_state_name = storage['state']
    curr_state = storage[curr_state_name]
    if storage['if_new_match'] is True:
        storage['if_new_match'] = False
        outcome = curr_state.output_func(stat, storage, 'new_match')
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
    me_id = stat['now']['me']['id']
    if me_id == 1:  # 如果我是先手
        me_turn = 2 * (2000 - stat['now']['turnleft'][me_id - 1] + 1) - 1  # 综合两方面的turn
    else:  # 如果我是后手
        me_turn = 2 * (2000 - stat['now']['turnleft'][me_id - 1] + 1)  # 综合两方面的turn

    state_record = storage['state_transfer'][match_num]
    path_record = storage['min_path'][match_num]

    if state_record[-1][1] != storage['state']:
        state_record.append((me_turn, storage['state']))
        path_record.append((mmf[0], meb[0], eef[0], emb[0]))

    # debug
    return outcome


def summary(match_result, stat, storage):
    '''一般情况下，用于debug的代码'''
    match_num = storage['match_num']
    me_id = stat['now']['me']['id']
    file_name = './AI/log/state_main_%d(%d)-%d.txt' % (storage['safe_disc'], match_num, me_id)  # 括号里表示第几局；id表示是先手还是后手
    f = open(file_name, 'w')
    state_record = storage['state_transfer'][match_num]
    path_record = storage['min_path'][match_num]
    this_len = len(state_record)
    for i in range(1, this_len):  # print None 搞不出来，还不报错
        f.write('Turn = %d, State = %s\n' % (state_record[i][0], state_record[i][1]))
        f.write("me_me_fields, me_enemy_bands, enemy_enemy_fields, enemy_me_bands = %d, %d, %d, %d\n" %
                           (path_record[i][0], path_record[i][1], path_record[i][2], path_record[i][3]))
        f.write('\n')
    f.write('ime of path_to: %fs\n' % storage['path_to_time'][match_num])
    f.close()


def summaryall(storage):
    pass
