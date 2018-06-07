from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.gen_func import LEFT
from AI.DSA_group1_package.gen_func import RIGHT
from AI.DSA_group1_package.gen_func import MIDDLE
import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'


class Retreat(State):

    # 这里如果需要新的初始化函数，可以这样写，不用的话可以省略。
    # def __init__(self, name, store):  # store = storage['statename_store']
    #     super(State, self).__init__(name, store)

    def output_func(self, stat, storage, last_state_name):
        if last_state_name != 'retreat':
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
        me = stat['now']['me']['id']
        xx = stat['now']['players'][me - 1]['x']  # 己方头部的位置
        yy = stat['now']['players'][me - 1]['y']
        olddire = stat['now']['players'][me - 1]['direction']
        width = stat['size'][0]  # 场地的宽
        height = stat['size'][1]  # 场地的高

        # case1: 纸带头在自己的领地，这样纸带头就在自己领地中打转
        if stat['now']['fields'][xx][yy] == me:
            if xx > 0 and olddire != 0 and stat['now']['fields'][xx - 1][yy] == me:
                return self.coordinateToDirection(stat, xx - 1, yy)
            elif xx < width - 1 and olddire != 2 and stat['now']['fields'][xx + 1][yy] == me:
                return self.coordinateToDirection(stat, xx + 1, yy)
            elif yy > 0 and olddire != 1 and stat['now']['fields'][xx][yy - 1] == me:
                return self.coordinateToDirection(stat, xx, yy - 1)
            else:
                return self.coordinateToDirection(stat, xx, yy + 1)

        iToMyFields = storage['path']['me_me_fields']
        retreatDis = storage['path']['me_me_fields'][0][0]                # 我回到己方区域的的最短距离
        temp = storage['path']['me_me_fields'][0][2]

        # case2: 无路可走
        if temp is None:  # 如果无路可走，直走
            return MIDDLE

        # case3: 紧挨着边界
        if retreatDis == 1:  # 距离为1
            return self.coordinateToDirection(stat, temp[0], temp[1])

        # case4: 敌人无法到达我的纸带
        if storage['path']['enemy_me_bands'][0][2] is None:
            storage['store']['retreat'] = iToMyFields[0][1]
            ans = storage['store']['retreat'].pop()
            return self.coordinateToDirection(stat, ans[0], ans[1])

        # case5: 检查第一种路径
        startX = storage['path']['enemy_me_bands'][0][2][0]
        startY = storage['path']['enemy_me_bands'][0][2][1]
        endX = stat['now']['players'][2 - me]['x']                  # 对方头部的位置
        endY = stat['now']['players'][2 - me]['y']
        if startX > endX:
            startX, endX = endX, startX
        if startY > endY:
            startY, endY = endY, startY

        count = [0]                                                  # 检查第一条路径
        target = iToMyFields[0][2]
        if startX <= target[0] <= endX and startY <= target[0] <= endY:  # 目标区域在带头和目标点之间的区域，可以走，对方不一定敢来
            count[0] = 0
        else:
            for i in range(len(iToMyFields[0][1])):
                if startX <= iToMyFields[0][1][i][0] <= endX and startY <= iToMyFields[0][1][i][0] <= endY:
                    count[0] += 1
        if count[0] == 0:
            storage['store']['retreat'] = iToMyFields[0][1]
            ans = storage['store']['retreat'].pop()
            return self.coordinateToDirection(stat, ans[0], ans[1])

        # case5: 检查其余路径
        k = 1
        pathNum = len(iToMyFields)
        minCount = count[0]
        minIndex = 0
        while k < pathNum:
            count.pop(0)
            target = iToMyFields[k][2]
            if startX <= target[0] <= endX and startY <= target[0] <= endY:  # 目标区域在两个带头之间的区域，可以走，对方不一定敢来
                count[k] = 0
            else:
                for i in range(iToMyFields[k][2]):
                    if startX <= iToMyFields[k][2][i][0] <= endX and startY <= iToMyFields[k][2][i][0] <= endY:
                        count[k] += 1
            if count[k] == 0:
                storage['store']['retreat'] = iToMyFields[k][1]
                ans = storage['store']['retreat'].pop()
                return self.coordinateToDirection(stat, ans[0], ans[1])
            elif count[k] < minCount:
                minIndex = k
            k += 1

        storage['store']['retreat'] = iToMyFields[minIndex][1]
        ans = storage['store']['retreat'].pop()
        return self.coordinateToDirection(stat, ans[0], ans[1])

    def subquent_output(self, stat, storage):
        # 如果计算过了路径，此处应该是规划好的路线，不需要stat和storage。你们可以重载不用这两个值
        # return 0  # 路径接下来的值，这个复杂度我假设是O(1)的，不要从list开头取出来，从尾取出来。
        if storage['store']['retreat'] is None:
            storage['store']['retreat'] = []
        if len(storage['store']['retreat']) != 0:
            ans = storage['store']['retreat'].pop()
            return self.coordinateToDirection(stat, ans[0], ans[1])
        else:
            return self.init_output(stat, storage, 'retreat')

    def trans_where(self, stat, storage, outcome=None):
        # outcome是为了，把下一步走什么列在state_transfer的考虑之中，我们目前可以简化不用，升级版可以用

        # step1: 有几种出去状态的情况，就考虑几种情况
        # Step2: 根据每一种情况，返回下一个状态的名字
        # 下面我把几种情况列举好，不过优先级顺序自己定

        # 提交时把下面这句话注释掉

        me = storage['me']['id']
        x = storage['me']['x']
        y = storage['me']['y']

        if storage['path']['me_enemy_bands'][0][0] < storage['path']['enemy_enemy_fields'][0][0]:  # go back to attack
            return ATTACK
            pass
        elif storage['fields'][x][y] == me:  # 回到领地，go to approach
            return APPROACH
            pass
        else:  # 还是自己
            return RETREAT
            pass
        # debug

        # return 0

    def state_transfer(self, storage, next_state_name):
        storage['state'] = next_state_name

    def transfer_to_retreat(self, storage):          # 判断是否调用撤退函数
        disToHome = storage['path']['me_me_fields'][0][0]
        disBeAttacked = storage['path']['enemy_me_bands'][0][0]
        if disToHome <= disBeAttacked:
            return True
        else:
            return False

    def coordinateToDirection(self, stat, nextX, nextY):  # 将坐标变为转向
        me = stat['now']['me']['id']
        xx = stat['now']['players'][me - 1]['x']  # 己方头部的位置
        yy = stat['now']['players'][me - 1]['y']
        if nextX > xx:
            dire = 0
        elif nextX < xx:
            dire = 2
        elif nextY > yy:
            dire = 1
        else:
            dire = 3
        olddire = stat['now']['players'][me - 1]['direction']
        if dire == olddire:
            return MIDDLE
        elif (dire == olddire + 1) or (dire == 0 and olddire == 3):
            return RIGHT
        else:
            return LEFT
