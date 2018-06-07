__doc__ = '''模板AI函数
 
（必要）play函数

（可选）load，summary函数

（多局比赛中可选）init，summaryall函数

详见AI_Template.pdf
'''


def load(stat, storage):
    # 定义四个状态名字常量
    ATTACK = 'attack'
    ENCLOSE = 'enclose'
    APPROACH = 'approach'
    RETREAT = 'retreat'

    # 开辟四个状态用的缓存空间
    storage['store'] = {}
    storage['store'][ATTACK] = None
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

    # debug
    storage['dead_time'] = []
    # debug

    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数超时或报错将判负

    params:
        stat - 游戏数据
        storage - 游戏存储
    '''
    pass


def play(stat, storage):
    ATTACK = 'attack'
    ENCLOSE = 'enclose'
    APPROACH = 'approach'
    RETREAT = 'retreat'
    # 清空上次计算的最短路径，这个不够优化，以后不要清空，要加以利用
    storage['me_me_fields'] = None
    storage['me_enemy_bands'] = None
    storage['enemy_enemy_fields'] = None
    storage['enemy_me_bands'] = None
    from AI.DSA_group1_package import gen_func
    LEFT = 'L'
    RIGHT = 'R'
    MIDDLE = 'M'
    # debug
    import random
    # debug

    curr_state = storage[storage['state']]
    '''
    AI函数，返回指令决定玩家转向方式
    该函数超时或报错将判负

    params:
        stat - 游戏数据
        storage - 游戏存储

    returns:
        1. 首字母为'l'或'L'的字符串 - 代表左转
        2. 首字母为'r'或'R'的字符串 - 代表右转
        3. 其余 - 代表直行
    '''

    outcome = curr_state.output_func(stat, storage, storage['state'])
    # debug
    if curr_state.name != ENCLOSE and curr_state.name != APPROACH:
        # 请改成你的state名称，比如'attack'。这里是，只有当现在不是你的state才会deadcheck，然后random选一个值走，
        direction_list = [LEFT, RIGHT, MIDDLE]
        random.shuffle(direction_list)
        for i in direction_list:
            x = stat['now']['me']['x']
            y = stat['now']['me']['y']
            test_point = gen_func.move(x, y, stat['now']['me']['direction'] + gen_func.direction_dict[i])
            temp = gen_func.fail_check(stat, storage, test_point[0], test_point[1])
            if temp == 1:
                outcome = i
                break
    return outcome
    # debug


def summary(match_result, stat, storage):




    '''
    一局对局总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        match_result - 对局结果
        stat - 游戏数据
        storage - 游戏存储
    '''
    pass


def init(storage):
    '''
    多轮对决中全局初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        storage - 游戏存储
    '''
    pass


def summaryall(storage):
    '''
    多轮对决中整体总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        storage - 游戏存储
    '''
    pass