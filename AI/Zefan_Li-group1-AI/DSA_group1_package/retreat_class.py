from AI.DSA_group1_package.state_class import State
from AI.DSA_group1_package.find_path import path_to
from AI.DSA_group1_package.gen_func import LEFT
from AI.DSA_group1_package.gen_func import RIGHT
from AI.DSA_group1_package.gen_func import MIDDLE
import random
ATTACK = 'attack'
ENCLOSE = 'enclose'
APPROACH = 'approach'
RETREAT = 'retreat'


class Retreat(State):

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

        me_me_fields = path_to(stat, storage, 'me_me_fields')
        dis_me_me_fields = me_me_fields[0]                # 我回到己方区域的的最短距离
        temp = me_me_fields[3]

        # case2: 无路可走
        if temp is None:  # 如果无路可走，直走
            return 'x'

        # case3: 紧挨着边界
        if dis_me_me_fields == 1:  # 距离为1
            return self.coordinateToDirection(stat, temp[0], temp[1])

        # case4: 回
        ans = storage['me_me_fields'][2][0]
        return self.coordinateToDirection(stat, ans[0], ans[1])

    def subquent_output(self, stat, storage):
        return self.init_output(stat, storage, 'retreat')


    # 完备了！！！
    def trans_where(self, stat, storage, outcome=None):
        # if storage[APPROACH].if_transfer_in(stat, storage):  # 回到领地，go to approach
        #     return APPROACH
        # else:  # 还是自己
        #     if_retreat = storage[RETREAT].if_transfer_in(stat, storage)
        #     if if_retreat == -1:  # 说明跑不了了，干脆进攻吧
        #         return ATTACK
        #     else:
        #         return RETREAT

        if storage[APPROACH].if_transfer_in(stat, storage):  # 回到领地，go to approach
            return APPROACH
        else:  # 还是自己   
            return RETREAT   

    def if_transfer_in(self, stat, storage):          # 判断是否调用撤退函数
        dis_me_me_fields = storage['me_me_fields'][0]
        dis_enemy_me_bands = storage['enemy_me_bands'][0]
        retreat_disc = dis_enemy_me_bands - dis_me_me_fields
        safe_disc = 0
        # 如果小于0，没有用不用跑了；1， 2， 都有可能失败，所以可以设为必须跑的界限；3一定能跑掉，所以不用跑3最多降为0
        # 下面实验，哪一个值最厉害

        # if 0 <= retreat_disc <= safe_disc:
        #     return 1  # 说明要撤退
        # elif retreat_disc < 0:
        #     return -1  # 说明撤退也跑不掉了，干脆进攻吧
        # else:
        #     return 0  # 说明不用撤退

        if retreat_disc <= safe_disc:
            return True  # 说明要撤退
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
