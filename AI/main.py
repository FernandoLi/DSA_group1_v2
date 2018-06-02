def play(stat, storage):
    # 我又添加了很多注释
    # 我添加了很多注释
    from AI.DSA_group1_package.find_path import path_to
    from AI.DSA_group1_package import gen_func
    # 距离计算的记录，一次比赛的play完成后会删除
    storage['path'] = {'me': {'me': [None], 'enemy': [None, None]},
                       'enemy': {'enemy': [None], 'me': [None, None]}, }
    storage['fields_count'] = None

    safe_point, chance_point = 0, 0
    name1 = stat['me']['id']
    name2 = stat['me']['id']
    pos_me = (stat['me']['x'], stat['me']['y'])
    pos_enemy = (stat['enemy']['x'], stat['enemy']['y'])

    # 计算安全感指数与胜机指数
    if stat['fields'][pos_me[0]][pos_me[1]] == name1:  # 我在自己领地，安全感+++
        safe_point += 90
    # 我回领地难于对方进攻，安全感*-
    elif path_to(stat, storage, 'me', 'me', 'fields')['dis'] > path_to(stat, storage, 'enemy', 'me', 'bands')['dis']:
        safe_point -= 10 + 5 * (path_to(stat, storage, 'me', 'me', 'fields')['dis'] -
                                path_to(stat, storage, 'enemy', 'me', 'bands')['dis'])
    else:  # 我回领地易于对方进攻，安全感*+
        safe_point -= 3 * (path_to(stat, storage, 'me', 'me', 'fields')['dis'] -
                           path_to(stat, storage, 'enemy', 'me', 'bands')['dis'])

    if stat['fields'][pos_me[0]][pos_me[1]] == name2:  # 我进入敌方领地，安全感--
        safe_point -= 20

    temp = gen_func.fields_count(stat, storage)
    safe_point += 2 * (temp[0] - temp[1])  # 领地越大越安全，安全感*（+/-）
    if stat['fields'][pos_enemy[0]][pos_enemy[1]] == name2:  # 敌方回领地，胜机---
        chance_point -= 60
    elif path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] < \
            path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis']:  # 我进攻易于敌退守，胜机++，*+
        chance_point += 10 - 5 * (path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] -
                                  path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis'])
    else:  # 我进攻难于敌退守，胜机*-
        chance_point -= 10 * (path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] -
                              path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis'])
    if stat['fields'][pos_enemy[0]][pos_enemy[1]] == name1:  # 敌进入我方领地，胜机++
        chance_point += 20
    else:
        chance_point += 1 * path_to(stat, storage, 'enemy', 'me', 'fields')['dis']

    # 如果可以立即获胜，那么进行
    for key, value in gen_func.direction_dict.items():
        new = gen_func.move(stat['me']['x'], stat['me']['y'], value + stat['me']['direction'])
        if new[0] < 0 or new[1] < 0 or new[0] >= storage['size'][0] or new[1] >= storage['size'][1]:
            continue
        if gen_func.win_check(stat, storage, *new):
            storage['memory'].append('Win Immediately')
            # storage['path'] = None
            return key

    # 之前的事件是否延续
    pastevent = storage['nowevent']
    if pastevent == 'first':
        pastname = 'first'
        pass
    else:
        pastname = pastevent.name[:]
        if pastevent:
            if not pastevent.event_break_check(stat, storage, safe_point, chance_point):
                temp = pastevent.event_continue(stat, storage)
                if storage['memory'] == []:
                    storage['memory'].append((pastname, 1))
                elif pastname == storage['memory'][len(storage['memory'])-1][0]:
                    storage['memory'][1] += 1
                else:
                    storage['memory'].append((pastname , 1))
                # storage['path'] = None
                return temp
            else:
                pastevent.event_stop(storage)

    # 未延续之前事件，开启新事件
    if safe_point > 0 and chance_point > 30:
        output = storage['event']['Attack'].event_start(stat, storage, pastname)
    elif safe_point > 30:
        output = storage['event']['Expand'].event_start(stat, storage, pastname)
    else:
        output = storage['event']['Defend'].event_start(stat, storage, pastname)

    if storage['memory'] == []:
        storage['memory'].append((storage['nowevent'].name, 1))
    elif storage['nowevent'].name == storage['memory'][len(storage['memory']) - 1][0]:
        storage['memory'][1] += 1
    else:
        storage['memory'].append((storage['nowevent'].name, 1))
    # storage['path'] = None
    return output


# load函数，初始化storage
def load(storage):
    import random

    def acfun1(stat, storage, name):
        from AI.DSA_group1_package.attack import attack
        return attack(stat=stat, storage=storage, last_path=None)
        # return random.choice('LMR')

    def acfun2(stat, storage, name):
        from AI.DSA_group1_package.retreat import retreat
        return retreat(stat=stat, storage=storage)
        # return random.choice('LMR')

    def acfun3(stat, storage, name):
        from AI.DSA_group1_package.enclosure import enclosure
        return enclosure(stat=stat, storage=storage, order='Yes')
        # return random.choice('LMR')

    from AI.DSA_group1_package.event_class import Event

    storage['memory'] = []

    temp = {'Attack': Event('Attack', acfun1), 'Defend': Event('Defend', acfun2),
            'Expand': Event('Expand', acfun3)}
    storage['event'] = temp
    storage['nowevent'] = 'first'

def summary(match_result , storage):
    print(match_result)
    print(storage['memory'])
    storage['memory'] = None
