# stat是状态，me是自己的id，desid是des对应的id，des指区域或者纸带，区域为1，纸带为0
# 无路可走返回[‘dis’]为999的字典，已经到达返回['dis']为0的字典(无其他key)
# 如果纸带头紧挨着目标区域，返回['dis']为1，['map']为None


class Node:
    def __init__(self, init_data, nxt=None, prev=None):
        self.data = init_data
        self.nxt = nxt
        self.prev = prev

    def get_data(self):
        return self.data

    def get_next(self):
        return self.nxt

    def get_prev(self):
        return self.prev

    def set_data(self, new_data):
        self.data = new_data
        return

    def set_next(self, new_next):
        self.nxt = new_next
        return

    def set_prev(self, new_prev):
        self.prev = new_prev
        return


class UnorderedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, item):
        temp = Node(item, self.head)    # 生成一个新节点
        if self.head is None:           # 无序列表为空
            self.head = temp
            self.tail = temp
        else:                           # 无序列表不为空
            self.head.set_prev(temp)
            self.head = temp
        return

    def size(self):
        current = self.head
        count = 0
        while current is not None:      # 当前节点不是尾节点
            count = count + 1
            current = current.get_next()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:    # 当前节点不是尾节点且没找到item
            if current.get_data() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def remove(self, item):
        if self.head == self.tail and self.head is not None: # 无序列表只有一个节点
            self.head = None
            self.tail = None
            return
        current = self.head
        while current is not None:                 # 前一个节点不是尾节点
            if current.get_data() == item:         # 找到item
                if current == self.head:           # item节点为头结点
                    self.head = current.get_next()
                    self.head.set_prev(None)
                elif current == self.tail:         # item节点为尾节点
                    self.tail = current.get_prev()
                    self.tail.set_next(None)
                else:                              # item节点在中间
                    current.get_prev().set_next(current.get_next())
                    current.get_next().set_prev(current.get_prev())
                return
            else:
                current = current.get_next()
        return current.get_data()                  # 找不到item，报错

    def append(self, item):
        temp = Node(item, prev=self.tail)
        if self.head is None:                       # 无序列表为空
            self.head = temp
            self.tail = temp
        else:
            self.tail.set_next(temp)                # 改变原来尾节点的指向
            self.tail = temp                        # 设置新的尾节点
        return

    def index(self, item):
        num = 0                               # item的索引
        current = self.head
        while True:                           # 无限循环
            if current.get_data() == item:    # 找到item
                return num
            else:
                num = num + 1
                current = current.get_next()  # 如果越界这句话会报错

    def __str__(self):
        current = self.head
        if current is None:                   # UnorderedList为空
            return '[]'
        stri = '['                            # 存储UnorderedList的字符串表示
        while current is not None:
            stri = stri + str(current.get_data()) + ', '
            current = current.get_next()
        stri = stri[:-2] + ']'                # 添加右括号
        return stri

    def __getitem__(self, ind):
        count = 0                             # 记录当前索引值
        current = self.head
        while True:
            if count == ind:                  # 找到索引
                return current.get_data()
            else:
                current = current.get_next()  # 如果越界这句话会报错
                count = count + 1

    def pop(self, pos=-1):
        current = self.tail
        if self.head == self.tail and self.head is not None:  # 无序列表只有一个节点
            self.head = None
            self.tail = None
            return current
        count = -1                            # 记录当前索引值
        while True:
            if count == pos:                  # 找到item
                if current == self.head:      # item节点为头结点
                    self.head = current.get_next()
                    self.head.set_prev(None)
                elif current == self.tail:    # item节点为尾节点
                    self.tail = current.get_prev()
                    self.tail.set_next(None)
                else:                         # item节点在中间
                    current.get_prev().set_next(current.get_next())
                    current.get_next().set_prev(current.get_prev())
                return current.get_data()
            else:
                current = current.get_prev()  # 如果越界这句话会报错
                count = count - 1

    def insert(self, ind, item):
        temp = Node(item)
        if self.head is None:                 # 无序列表为空
            if ind == 0:
                self.head = temp
                self.tail = self.head
            return                            # 不论ind为何值都返回
        count = 0                             # 记录当前索引值
        current = self.head
        while True:
            if count == ind:
                if current == self.head:      # 索引值为0
                    temp.set_next(self.head)
                    self.head.set_prev(temp)
                    self.head = temp
                else:                         # 索引值为1 ~ size()-1
                    temp.set_prev(current.get_prev())
                    temp.set_next(current)
                    current.get_prev().set_next(temp)
                    current.set_prev(temp)
                return
            elif count == (ind - 1) and current == self.tail:    # 索引值为size()
                temp.set_prev(self.tail)
                self.tail.set_next(temp)
                self.tail = temp
                return
            else:
                current = current.get_next()  # 如果越界这句话会报错
                count = count + 1


def find_path(stat, storage, me, desid, des):
    import time
    t0 = time.time()
    width = stat['size'][0]  # 场地的宽
    height = stat['size'][1]  # 场地的高
    x = stat['now']['players'][me - 1]['x']  # 己方头部的位置
    y = stat['now']['players'][me - 1]['y']

    if des:
        if stat['now']['fields'][x][y] == desid:# 头部在己方区域，且寻找到己方区域的最短路径
            t1 = time.time()
            storage['path_time'].append(t1 - t0)
            return {'dis': 0}
        aim = 'fields'
        destination = desid
    else:
        aim = 'bands'
        destination = 3 - me

    mymap = []  # 记录路径状态，以目标区域为递推起点
    for i in range(width):
        mymap.append([])
        for j in range(height):
            if stat['now'][aim][i][j] == destination:  # 目标区域
                mymap[i].append(0)
            elif stat['now']['bands'][i][j] == me:  # 己方纸带
                mymap[i].append(-1)
            else:
                mymap[i].append(None)
    mymap[x][y] = -1
    if aim == 'bands':  # 搜索到纸带的距离，把头部也当作纸带
        mymap[stat['now']['players'][2 - me]['x']][stat['now']['players'][2 - me]['y']] = 0

    if x > 0 and mymap[x - 1][y] == 0 and stat['now']['players'][me - 1]['direction'] != 0:# 纸带头紧挨着目标区域
        t1 = time.time()
        storage['path_time'].append(t1 - t0)
        return {'dis': 1, 'map': None, 'start': [[x - 1, y]]}
    if x < width - 1 and mymap[x + 1][y] == 0 and stat['now']['players'][me - 1]['direction'] != 2:
        t1 = time.time()
        storage['path_time'].append(t1 - t0)
        return {'dis': 1, 'map': None, 'start': [[x + 1, y]]}
    if y > 0 and mymap[x][y - 1] == 0 and stat['now']['players'][me - 1]['direction'] != 1:
        t1 = time.time()
        storage['path_time'].append(t1 - t0)
        return {'dis': 1, 'map': None, 'start': [[x, y - 1]]}
    if y < height - 1 and mymap[x][y + 1] == 0 and stat['now']['players'][me - 1]['direction'] != 3:
        t1 = time.time()
        storage['path_time'].append(t1 - t0)
        return {'dis': 1, 'map': None, 'start': [[x, y + 1]]}

    # 以头部为起点开始搜索
    start = [[], []]       # 记录搜索的起点
    start[0].append([x, y])

    # stop = []              # 记录搜索的终点
    stop = UnorderedList()
    temp = []              # 记录路径起点
    for i in range(width):
        for j in range(height):
            if mymap[i][j] is not None:
                continue
            if (i > 0 and mymap[i - 1][j] == 0)\
                    or (i < width - 1 and mymap[i + 1][j] == 0)\
                    or (j > 0 and mymap[i][j - 1] == 0)\
                    or (j < height - 1 and mymap[i][j + 1] == 0):
                stop.append([i, j])

    length = 0              # 当前搜索的路径长度
    while True:             # 搜索路径
        length += 1
        start[length % 2] = []
        for index in range(len(start[1 - length % 2])):  # 遍历当前节点
            i = start[1 - length % 2][index][0]
            j = start[1 - length % 2][index][1]
            if i > 0 and mymap[i - 1][j] is None:
                mymap[i - 1][j] = length
                start[length % 2].append([i - 1, j])
            if i < width - 1 and mymap[i + 1][j] is None:
                mymap[i + 1][j] = length
                start[length % 2].append([i + 1, j])
            if j > 0 and mymap[i][j - 1] is None:
                mymap[i][j - 1] = length
                start[length % 2].append([i, j - 1])
            if j < height - 1 and mymap[i][j + 1] is None:
                mymap[i][j + 1] = length
                start[length % 2].append([i, j + 1])
        ind = 0
        while ind < stop.size():
            if mymap[stop[ind][0]][stop[ind][1]] is not None:
                temp.append(stop.pop(ind - stop.size()))
            else:
                ind += 1
        if stop.size() == 0:
            break
        if len(temp) > 5:
            break
        if len(start[length % 2]) == 0:
            break

    t1 = time.time()
    storage['path_time'].append(t1 - t0)
    if len(temp) != 0:
        # temp是目标区域可以出发的坐标
        return {'dis': mymap[temp[0][0]][temp[0][1]] + 1, 'map': mymap, 'start': temp}
    else:
        return {'dis': 99999, 'map': mymap, 'start': None}


def path_to(stat, storage, person, owner, area_type):
    FIELDS = 1
    BANDS = 0

    flag = True
    for x in stat['now'][area_type]:
        for y in x:
            if y == stat['now'][owner]['id']:
                flag = False
                break
    if flag:
        return {'dis': 99999}
    if person == 'me':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['me']['me'][0]:
                    return storage['path']['me']['me'][0]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['me']['id'], FIELDS)
                storage['path']['me']['me'][0] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['me']['enemy'][0]:
                    return storage['path']['me']['enemy'][0]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['enemy']['id'], FIELDS)
                storage['path']['me']['enemy'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['me']['enemy'][1]:
                    return storage['path']['me']['enemy'][1]
                a = find_path(stat, storage, stat['now']['me']['id'], stat['now']['enemy']['id'], BANDS)
                storage['path']['me']['enemy'][1] = a
                return a
    elif person == 'enemy':
        if owner == 'me':
            if area_type == 'fields':
                if storage['path']['enemy']['me'][0]:
                    return storage['path']['enemy']['me'][0]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['me']['id'], FIELDS)
                storage['path']['enemy']['me'][0] = a
                return a
            elif area_type == 'bands':
                if storage['path']['enemy']['me'][1]:
                    return storage['path']['enemy']['me'][1]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['me']['id'], BANDS)
                storage['path']['enemy']['me'][1] = a
                return a
        elif owner == 'enemy':
            if area_type == 'fields':
                if storage['path']['enemy']['enemy'][0]:
                    return storage['path']['enemy']['enemy'][0]
                a = find_path(stat, storage, stat['now']['enemy']['id'], stat['now']['enemy']['id'], FIELDS)
                storage['path']['enemy']['enemy'][0] = a
                return a
