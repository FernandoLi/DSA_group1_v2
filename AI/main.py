def play(stat, storage):
    from time import time
    from AI.DSA_group1_package.find_path import path_to
    from AI.DSA_group1_package import gen_func

    timetemp = [stat['now']['turnleft'][0]]
    print(timetemp)
    t = time()
    t0 = int(round(t * 1000))
    # 距离计算的记录，一次比赛的play完成后会删除
    storage['path'] = {'me': {'me': [None], 'enemy': [None, None]},
                       'enemy': {'enemy': [None], 'me': [None, None]}, }
    storage['fields_count'] = None

    safe_point, chance_point = 0, 0
    name1 = stat['now']['me']['id']
    name2 = stat['now']['me']['id']
    pos_me = (stat['now']['me']['x'], stat['now']['me']['y'])
    pos_enemy = (stat['now']['enemy']['x'], stat['now']['enemy']['y'])

    # 计算安全感指数与胜机指数
    if stat['now']['fields'][pos_me[0]][pos_me[1]] == name1:  # 我在自己领地，安全感+++
        safe_point += 90
    # 我回领地难于对方进攻，安全感*-
    elif path_to(stat, storage, 'me', 'me', 'fields')['dis'] > path_to(stat, storage, 'enemy', 'me', 'bands')['dis']:
        safe_point -= 10 + 5 * (path_to(stat, storage, 'me', 'me', 'fields')['dis'] -
                                path_to(stat, storage, 'enemy', 'me', 'bands')['dis'])
    else:  # 我回领地易于对方进攻，安全感*+
        safe_point -= 3 * (path_to(stat, storage, 'me', 'me', 'fields')['dis'] -
                           path_to(stat, storage, 'enemy', 'me', 'bands')['dis'])

    if stat['now']['fields'][pos_me[0]][pos_me[1]] == name2:  # 我进入敌方领地，安全感--
        safe_point -= 20

    temp = gen_func.fields_count(stat, storage)
    safe_point += 0.5 * (temp[0] - temp[1])  # 领地越大越安全，安全感*（+/-）

    t = time()
    t2 = int(round(t * 1000))
    timetemp.append(['safe_calculate:', t2 - t0])

    if stat['now']['fields'][pos_enemy[0]][pos_enemy[1]] == name2:  # 敌方回领地，胜机---
        chance_point -= 60
    elif path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] < \
            path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis']:  # 我进攻易于敌退守，胜机++，*+
        chance_point += 10 - 5 * (path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] -
                                  path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis'])
    else:  # 我进攻难于敌退守，胜机*-
        chance_point -= 5 * (path_to(stat, storage, 'me', 'enemy', 'bands')['dis'] -
                              path_to(stat, storage, 'enemy', 'enemy', 'fields')['dis'])
    if stat['now']['fields'][pos_enemy[0]][pos_enemy[1]] == name1:  # 敌进入我方领地，胜机++
        chance_point += 20
    else:
        chance_point += 1 * path_to(stat, storage, 'enemy', 'me', 'fields')['dis']

    t = time()
    t3 = int(round(t * 1000))
    timetemp.append(['chance_calculate:', t3 - t2])

    # 如果可以立即获胜，那么进行
    for key, value in gen_func.direction_dict.items():
        new = gen_func.move(stat['now']['me']['x'], stat['now']['me']['y'], value + stat['now']['me']['direction'])
        if new[0] < 0 or new[1] < 0 or new[0] >= stat['size'][0] or new[1] >= stat['size'][1]:
            continue
        if gen_func.win_check(stat, storage, *new):
            storage['memory'].append('Win Immediately')
            t = time()
            t1 = int(round(t * 1000))
            timetemp.append(['immediately:', t1 - t3])
            # storage['path'] = None
            storage['time'].append([storage['nowevent'].name, timetemp])
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
                    storage['memory'].append([pastname, 1])
                elif pastname == storage['memory'][-1][0]:
                    storage['memory'][-1][1] += 1
                else:
                    print(storage['memory'][-1])
                    storage['memory'].append([pastname , 1])
                # storage['path'] = None
                t = time()
                t1 = int(round(t * 1000))
                timetemp.append(['fun_continue:',t1-t3])
                storage['time'].append([storage['nowevent'].name, timetemp])
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

    t = time()
    t4 = int(round(t * 1000))
    timetemp.append(['newevent:', t4 - t3])

    if storage['memory'] == []:
        storage['memory'].append([storage['nowevent'].name, 1])
    elif storage['nowevent'].name == storage['memory'][- 1][0]:
        storage['memory'][-1][1] += 1
    else:
        print(storage['memory'][-1])
        storage['memory'].append([storage['nowevent'].name, 1])
    # storage['path'] = None
    storage['time'].append([storage['nowevent'].name,timetemp])
    return output


# init函数，初始化storage
def load(stat , storage):

    def acfun1(stat, storage, name):
        from AI.DSA_group1_package.attack import attack
        return attack(stat=stat, storage=storage, last_path=None)
        # return random.choice('LMR')

    def acfun2(stat, storage, name):
        from AI.DSA_group1_package.retreat import retreat
        return retreat(stat=stat, storage=storage , order = name)
        # return random.choice('LMR')

    def acfun3(stat, storage, name):
        from AI.DSA_group1_package.enclosure import enclosure
        return enclosure(stat=stat, storage=storage, order='Yes')
        # return random.choice('LMR')

    from AI.DSA_group1_package.event_class import Event

    temp = {'Attack': Event('Attack', acfun1), 'Defend': Event('Defend', acfun2),
            'Expand': Event('Expand', acfun3)}
    storage['event'] = temp

    storage['memory'] = []
    storage['nowevent'] = 'first'
    storage['time'] = []

#对局总结函数(单次)
def summary(match_result , stat , storage):
    print(match_result)
    print(storage['memory'])
    print(storage['time'])
    storage['memory'] = None
    storage['path'] = None
