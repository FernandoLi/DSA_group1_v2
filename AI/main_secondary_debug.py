def play(stat, storage):
    ''''I revised just now'''
    ''''I revised just now'''
    from AI.DSA_group1_package.retreat import retreat
    from AI.DSA_group1_package.enclosure import enclosure
    from AI.DSA_group1_package.attack import attack

    storage['path'] = {'me': {'me': [None], 'enemy': [None, None]},
                       'enemy': {'enemy': [None], 'me': [None, None]}, }

    # turn = enclosure(stat=stat, storage=storage, order=None)
    turn = attack(stat, storage, last_path=None)
    # turn = retreat(stat=stat, storage=storage)

    return turn
