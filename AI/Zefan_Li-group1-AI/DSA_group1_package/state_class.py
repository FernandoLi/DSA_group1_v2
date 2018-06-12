ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'
from AI.DSA_group1_package.gen_func import win_check

class State:

    # State，所有状态State具体类的父类

    def __init__(self, name, store):  # store = storage['statename_store']
        self.name = name
        self.store = store  # 这个"状态"能够使用的存储空间，
        # 在storage中，四个状态名字。

    def output_func(self, stat, storage, last_state_name):
        temp = win_check(stat, storage)
        if temp is not None:
            return temp
        else:
            if self.name != last_state_name:
                # 上一轮的状态和这一轮的状态不一致时

                outcome = self.init_output(stat, storage, last_state_name)

                next_state_name = self.trans_where(stat, storage)  # 需要根据当前的状态
                if next_state_name != self.name:
                    self.state_transfer(storage, next_state_name)

                pass  # 意思是，状态转换，首次调用一定要有要返回值，outcome保留到底

            else:
                next_state_name = self.trans_where(stat, storage)  # 需要根据当前的状态

                if next_state_name == self.name:
                    # 上一轮的状态和这一轮一致时：
                    outcome = self.subquent_output(stat, storage)  # 我预想O(1)的复杂度
                    pass  # 意思是，事件继续了，所以用这个outcome

                else:
                    # 如果状态转换了，那么交给笑一个函数的init_output来返回值

                    outcome = storage[next_state_name].init_output(stat, storage, self.name)

                    self.state_transfer(storage, next_state_name)

                    pass  # 这时候outcome就是下一状态init_output计算出来的值

            return outcome

    def init_output(self, stat, storage, last_state_name):  # storage几乎用不到，预备以后应用多局历史数据
        # step1: 处理几种进入状态的case：enclose, attack, approach, retreat
        # step2: 根据现在的情况计算出一个路径/或者一个输出值，这个自己看。但是必须有一个返回值
        return 0  # 路径的第一个值

    def subquent_output(self, stat, storage):
        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        return 0  # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。

    def trans_where(self, stat, storage, outcome=None):
        # outcome是为了，把下一步走什么列在state_transfer的考虑之中，我们目前可以简化不用，升级版可以用

        # step1: 有几种出去状态的情况，就考虑几种情况
        # Step2: 根据每一种情况，返回下一个状态的名字
        # 下面我把几种情况列举好，不过优先级顺序自己定
        return 0

    def if_transfer_in(self, stat, storage):
        # 返回一个逻辑值，True则进入这个状态，否则不满足进入状态条件
        pass

    def state_transfer(self, storage, next_state_name):
        # 实际的状态转移函数，进行状态转移
        # 相当于析构函数，当状态要转移出去的时候，清空store字典
        storage['state'] = next_state_name
        self.store = {}


