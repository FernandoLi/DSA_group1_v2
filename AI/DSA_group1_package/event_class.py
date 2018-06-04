class Event:

    # Event类，在第一回合初始化三个，放在storage['event']内，storage['nowevent']存放进行中的事件
    # 事件每次进行（开始/继续），都会调用一次函数

    def __init__(self, name, acfun):
        self.name = name
        self.func = acfun
        self.out = None

    def event_start(self, stat, storage, lastway):
        self.out = self.func(stat, storage, lastway)
        storage['nowevent'] = self
        return self.out

    def event_continue(self, stat, storage):
        return self.out

    def event_stop(self, storage):
        self.out = None
        storage['nowevent'] = None

    def event_break_check(self, stat, storage, safe_point, chance_point):
        from AI.DSA_group1_package import gen_func
        from time import time
        flag = False
        t0 = time()
        self.out = self.func(stat, storage, self.name)
        t1 = time()
        storage['event_time'].append(t1 - t0)
        if not gen_func.fail_check(stat, storage, *gen_func.move(stat['now']['me']['x'], stat['now']['me']['y'],
                                                                 gen_func.direction_dict[self.out])):
            flag = True
        elif self.name == 'Expand':
            if safe_point < -25:
                flag = True
        elif self.name == 'Attack':
            if chance_point < -20:
                flag = True
        elif self.name == 'Defend':
            if safe_point > 60:
                flag = True
        return flag
