# 撤退函数
def retreat(stat, storage, order):
    # 将坐标转换为转向的函数
    from AI.DSA_group1_package.gen_func import LEFT
    from AI.DSA_group1_package.gen_func import RIGHT
    from AI.DSA_group1_package.gen_func import MIDDLE

    def coordinateToDirection(stat, me, nextX, nextY):  # 将坐标变为转向
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
        elif dire == olddire + 1 or (dire == 0 and olddire == 3):
            return RIGHT
        else:
            return LEFT

    me = stat['now']['me']['id']
    xx = stat['now']['players'][me - 1]['x']  # 己方头部的位置
    yy = stat['now']['players'][me - 1]['y']
    olddire = stat['now']['players'][me - 1]['direction']
    width = stat['size'][0]         # 场地的宽
    height = stat['size'][1]        # 场地的高

    # case1: 纸带头在自己的领地
    if stat['now']['fields'][xx][yy] == me:
        if xx > 0 and olddire != 0:
            return coordinateToDirection(stat, me, xx-1, yy)
        elif xx < width-1 and olddire != 2:
            return coordinateToDirection(stat, me, xx + 1, yy)
        elif yy > 0 and olddire != 1:
            return coordinateToDirection(stat, me, xx, yy-1)
        else:
            return coordinateToDirection(stat, me, xx, yy+1)

    try:
        storage['retreat']
    except KeyError:
        storage['retreat'] = []
    # case2: 连续调用且存储的值不为空
    if order != 'Defend' and len(storage['retreat']) != 0:
        return storage['retreat'].pop()

    from AI.DSA_group1_package.find_path import path_to
    iToMyFields = path_to(stat, storage, 'me', 'me', 'fields')
    eToMyBands = path_to(stat, storage, 'enemy', 'me', 'bands')
    retreatDis = iToMyFields['dis']  # 我回到己方区域的的最短距离
    failDis = eToMyBands['dis']      # 对方到我的纸带的最短距离
    retreatMap = iToMyFields['map']
    failMap = eToMyBands['map']
    paths = [[]]  # 恢复路径
    temp = iToMyFields['start']

    # case4: 无路可走
    if temp is None:  # 如果无路可走，直走
        return MIDDLE

    # case5: 紧挨着边界
    if retreatDis == 1:    # 距离为1
        return coordinateToDirection(stat, me, temp[0][0], temp[0][1])

    paths[0].append(temp[0])  # 恢复一条最短路径
    index = retreatMap[paths[0][0][0]][paths[0][0][1]]
    index -= 1
    i = paths[0][0][0]  # 记录起点坐标
    j = paths[0][0][1]
    failTemp = failDis
    while index > 0:
        if failMap[i][j] is not None and failMap[i][j] + 1 < failDis:
            # 这条最短路径是否会缩短对方到我方纸带距离
            failTemp = failMap[i][j] + 1
        if i > 0 and retreatMap[i - 1][j] == index:
            paths[0].append([i - 1, j])
            i = i - 1
        elif i < width - 1 and retreatMap[i + 1][j] == index:
            paths[0].append([i + 1, j])
            i = i + 1
        elif j > 0 and retreatMap[i][j - 1] == index:
            paths[0].append([i, j - 1])
            j = j - 1
        elif j < height - 1 and retreatMap[i][j + 1] == index:
            paths[0].append([i, j + 1])
            j = j + 1
        index -= 1

    # case6: 最短路径是安全的
    if failTemp >= retreatDis:  # 走最短路径是绝对安全的
        storage['retreat'] = paths[0]
        ans = storage['retreat'].pop()
        return coordinateToDirection(stat, me, ans[0], ans[1])

    # case7：最短路径不安全，找其他路径
    k = 1  # 走最短路径不安全，寻找其他路径
    failDisL = [failTemp]
    while k < len(temp):          # 这里temp最大为5
        paths.append([])
        paths[k].append(temp[k])  # 恢复其他最短路径
        index = retreatMap[paths[k][0][0]][paths[k][0][1]]
        index -= 1
        i = paths[k][0][0]  # 记录起点坐标
        j = paths[k][0][1]
        failTemp = failMap[i][j] + 1
        while index >= 0:
            if failMap[i][j] is not None and failMap[i][j] + 1 < failTemp:
                # 这条最短路径是否会缩短对方到我方纸带距离
                failTemp = failMap[i][j] + 1
            if i > 0 and retreatMap[i - 1][j] == index:
                paths[k].append([i - 1, j])
                i = i - 1
            elif i < width - 1 and retreatMap[i + 1][j] == index:
                paths[k].append([i + 1, j])
                i = i + 1
            elif j > 0 and retreatMap[i][j - 1] == index:
                paths[k].append([i, j - 1])
                j = j - 1
            elif j < height - 1 and retreatMap[i][j + 1] == index:
                paths[k].append([i, j + 1])
                j = j + 1
            index -= 1
        failDisL.append(failTemp)
        k += 1

    maxDis = failDisL[0]
    maxIndex = 0
    k = 1
    while k < len(temp):
        if failDisL[k] > maxDis:
            maxIndex = k
        k += 1
    storage['retreat'] = paths[maxIndex]
    ans = storage['retreat'].pop()
    return coordinateToDirection(stat, me, ans[0], ans[1])
