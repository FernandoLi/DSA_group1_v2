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
    # 清空上次计算的最短路径，这个不够优化，以后不要清空，要加以利用
    storage['path']['me_me_fields'] = None
    storage['path']['me_enermy_bands'] = None
    storage['path']['enermy_enermy_fields'] = None
    storage['path']['enermy_me_bands'] = None

    curr_state = storage[storage['mode']]

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
    return curr_state.output_func(stat, storage, None)


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