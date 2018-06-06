from AI.DSA_group1_package.state_class import State
import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'


class Attack(State):

    # 这里如果需要新的初始化函数，可以这样写，不用的话可以省略。
    # def __init__(self, name, store):  # store = storage['statename_store']
    #     super(State, self).__init__(name, store)

    def output_func(self, stat, storage, last_state_name):
        if self.name != last_state_name:
            # 上一轮的状态和这一轮的状态不一致时

            outcome = self.init_output(stat, storage, last_state_name)

            next_state_name = self.trans_where(stat, storage)  # 需要根据当前的状态
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

                self.state_transfer(storage, next_state_name)

                outcome = storage[next_state_name].output_func(stat, storage, self.name)

                pass  # 这时候outcome就是下一状态init_output计算出来的值

        return outcome

    def init_output(self, stat, storage, last_state_name):  # storage几乎用不到，预备以后应用多局历史数据
        # step1: 处理几种进入状态的case：enclose, attack, approach, retreat
        # step2: 根据现在的情况计算出一个路径/或者一个输出值，这个自己看。但是必须有一个返回值
        if last_state_name == RETREAT:
            pass
        elif last_state_name == APPROACH:
            pass
        elif last_state_name == ENCLOSE:
            pass
        else:  # 还是attack
            pass
        # return 0  # 路径的第一个值

        # debug
        return random.choice('LMR')
        # debug

    def subquent_output(self, stat, storage):
        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        # return 0  # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。
        return random.choice('LMR')

    def trans_where(self, stat, storage, outcome=None):
        # outcome是为了，把下一步走什么列在state_transfer的考虑之中，我们目前可以简化不用，升级版可以用

        # step1: 有几种出去状态的情况，就考虑几种情况
        # Step2: 根据每一种情况，返回下一个状态的名字
        # 下面我把几种情况列举好，不过优先级顺序自己定

        # debug
        rand_num = random.randint(1, 20)
        if rand_num == 1:  # go to retreat
            return RETREAT
            pass
        else:  # 还是自己
            return self.name
            pass
        # debug

        # return 0

    def state_transfer(self, storage, next_state_name):
        storage['state'] = next_state_name
