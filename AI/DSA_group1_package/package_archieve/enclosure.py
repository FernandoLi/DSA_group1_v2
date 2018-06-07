def fun_enclosure(stat, storage):
    from random import choice
    from AI.DSA_group1_package.find_path_new import path_to
    from AI.DSA_group1_package.gen_func import LEFT
    from AI.DSA_group1_package.gen_func import RIGHT
    from AI.DSA_group1_package.gen_func import MIDDLE

    now = stat['now']['me']
    ene = stat['now']['enemy']
    max_dist = path_to(stat, storage, 'enemy', 'me', 'bands')['dis']  # 敌方纸头到我方纸带的最短距离
    try:
        maps = path_to(stat, storage, 'me', 'me', 'fields')['map']
    except KeyError:
        maps = 'excuseme'
    xe = ene['x']
    ye = ene['y']
    xn = now['x']
    yn = now['y']
    if max_dist == 99999 or max_dist == 0:
        max_dist = abs(xe - xn) + abs(ye - yn)
    si = stat['size']
    MAXx = si[0]
    MAXY = si[1]

    # 测算领地最外沿的坐标值
    # 就是遍历一遍找最值
    def field_range(name, owner):
        mini = 'False'
        xmin = MAXx - 1
        ymin = MAXY - 1
        xmax = 0
        ymax = 0
        for x in range(0, MAXx - 1):
            for y in range(0, MAXY - 1):
                if stat['now'][name][x][y] == owner and (
                        stat['now'][name][x - 1][y] is None or stat['now'][name][x - 1][y] == ene['id'] or x == 0) and (
                        stat['now'][name][x][y - 1] is None or stat['now'][name][x][y - 1] == ene['id'] or y == 0):
                    if mini == 'False':
                        xmin = x
                        mini = True
                        if y < ymin:
                            ymin = y
                    else:
                        if y < ymin:
                            ymin = y
                elif stat['now'][name][x][y] == owner and (
                        stat['now'][name][x + 1][y] is None or stat['now'][name][x + 1][y] == ene['id'] or x == MAXx - 2) and (
                        stat['now'][name][x][y + 1] is None or stat['now'][name][x][y + 1] == ene['id'] or y == MAXY - 2):
                    if x > xmax:
                        xmax = x
                    if y > ymax:
                        ymax = y
        return xmin, ymin, xmax, ymax

    # '''以下这些是划定最外沿的八个顶点'''
    # 设x最小，从头开始找y
    (xm, ym, xM, yM) = field_range('fields', now['id'])
    a1 = 0
    a2 = 0
    a3 = 0
    a4 = 0
    ylu = 0
    yld = MAXY - 1
    yru = 0
    yrd = MAXY - 1
    while a1 < 1:
        if stat['now']['fields'][xm][ylu] is None or stat['now']['fields'][xm][ylu] == ene['id']:
            ylu += 1
        else:
            a1 = 1
    while a2 < 1:
        if stat['now']['fields'][xm][yld] is None or stat['now']['fields'][xm][yld] == ene['id']:
            yld -= 1
        else:
            a2 = 1
    while a3 < 1:
        if stat['now']['fields'][xM][yru] is None or stat['now']['fields'][xM][yru] == ene['id']:
            yru += 1
        else:
            a3 = 1
    while a4 < 1:
        if stat['now']['fields'][xM][yrd] is None or stat['now']['fields'][xM][yrd] == ene['id']:
            yrd -= 1
        else:
            a4 = 1
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    xlu = 0
    xru = MAXx - 1
    xld = 0
    xrd = MAXx - 1
    while b1 < 1:
        if stat['now']['fields'][xlu][ym] is None or stat['now']['fields'][xlu][ym] == ene['id']:
            xlu += 1
        else:
            b1 = 1
    while b2 < 1:
        if stat['now']['fields'][xru][ym] is None or stat['now']['fields'][xru][ym] == ene['id']:
            xru -= 1
        else:
            b2 = 1
    while b3 < 1:
        if stat['now']['fields'][xld][yM] is None or stat['now']['fields'][xld][yM] == ene['id']:
            xld += 1
        else:
            b3 = 1
    while b4 < 1:
        if stat['now']['fields'][xrd][yM] is None or stat['now']['fields'][xrd][yM] == ene['id']:
            xrd -= 1
        else:
            b4 = 1

        '''五种走法'''

    def updown(leng, ya, yb, maxdist):  # 先北上再水平再南下
        deltay = yb - ya
        totallength = leng + abs(deltay)
        ave = (maxdist - totallength - 1) // 2
        if deltay >= 0:
            if ya - ave <= 1:
                ave = ya - 1
            nr = deltay + ave
            paralla = leng
            su = ave
        else:
            if yb - ave <= 1:
                ave = yb - 1
            nr = ave
            paralla = leng
            su = ave - deltay
        return nr, paralla, su

    def downup(leng, ya, yb, maxdist):  # 先南下再水平再北上
        deltay = yb - ya
        totallength = leng + abs(deltay)
        ave = (maxdist - totallength - 1) // 2
        if deltay >= 0:
            if yb + ave >= MAXY - 2:
                ave = MAXY - yb - 2
            nr = deltay + ave
            paralla = leng
            su = ave
        else:
            if ya + ave >= MAXY - 2:
                ave = MAXY - ya - 2
            nr = ave
            paralla = leng
            su = ave - deltay
        return su, paralla, nr

    def leftright(leng, xa, xb, maxdist):  # 先西游再竖直再东行
        deltax = xb - xa
        totallength = leng + abs(deltax)
        ave = (maxdist - totallength - 1) // 2
        if deltax >= 0:
            if xa - ave <= 1:
                ave = xa - 1
            we = deltax + ave
            vertical = leng
            ea = ave
        else:
            if xb - ave <= 1:
                ave = xb - 1
            we = ave
            vertical = leng
            ea = ave - deltax
        return we, vertical, ea

    def rightleft(leng, xa, xb, maxdist):  # 先东行再竖直再西游
        deltax = xb - xa
        totallength = leng + abs(deltax)
        ave = (maxdist - totallength - 1) // 2
        if deltax >= 0:
            if xb + ave >= MAXx - 2:
                ave = MAXx - xb - 2
            we = deltax + ave
            vertical = leng
            ea = ave
        else:
            if xa + ave >= MAXx - 2:
                ave = MAXx - xa - 2
            we = ave
            vertical = leng
            ea = ave - deltax
        return ea, vertical, we

    def shortest(xp, yp, mapss):  # 最短回程, 回到自己领地，在自己领地，则想办法出去
        answe = []
        fi = stat['now']['me']['direction']
        if mapss == 'excuseme':
            if fi == 0:
                if 1 < yp < MAXY - 2:
                    answe.append(choice([LEFT, RIGHT]))
                elif yp >= MAXY - 2:
                    answe.append(LEFT)
                else:
                    answe.append(RIGHT)
            elif fi == 1:
                if 1 < xp < MAXx - 2:
                    answe.append(choice([LEFT, RIGHT]))
                elif xp >= MAXx - 2:
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
            elif fi == 2:
                if 1 < yp < MAXY - 2:
                    answe.append(choice([LEFT, RIGHT]))
                elif yp >= MAXY - 2:
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
            else:
                if 1 < xp < MAXx - 2:
                    answe.append(choice([LEFT, RIGHT]))
                elif xp >= MAXx - 2:
                    answe.append(LEFT)
                else:
                    answe.append(RIGHT)
        elif mapss is None:
            if fi == 0:
                if yp == ym:
                    answe.append(RIGHT)
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
                    answe.append(LEFT)
            elif fi == 1:
                if xp == xM:
                    answe.append(RIGHT)
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
                    answe.append(LEFT)
            elif fi == 2:
                if yp == yM:
                    answe.append(RIGHT)
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
                    answe.append(LEFT)
            elif fi == 3:
                if xp == xm:
                    answe.append(RIGHT)
                    answe.append(RIGHT)
                else:
                    answe.append(LEFT)
                    answe.append(LEFT)
        else:
            ans = list()
            ans.append(fi)
            check = 1
            while check > 0:
                try:
                    e = mapss[xp + 1][yp]
                except IndexError:
                    e = 200
                try:
                    s = mapss[xp][yp + 1]
                except IndexError:
                    s = 200
                try:
                    w = mapss[xp - 1][yp]
                except IndexError:
                    w = 200
                try:
                    n = mapss[xp][yp - 1]
                except IndexError:
                    n = 200
                eswn = [e, s, w, n]
                for i in range(4):
                    if eswn[i] == -1 or eswn[i] is None:
                        eswn[i] = 200
                p = 0
                q = 201
                for i in range(4):
                    if eswn[i] < q:
                        q = eswn[i]
                        p = i
                if p == 0:
                    xp = xp + 1
                    yp = yp
                elif p == 1:
                    xp = xp
                    yp = yp + 1
                elif p == 2:
                    xp = xp - 1
                    yp = yp
                else:
                    xp = xp
                    yp = yp - 1
                ans.append(p)
                if eswn[p] == 0:
                    check = 0

            for k in range(len(ans) - 1):
                num1 = ans[k]
                num2 = ans[k + 1]
                if num2 - num1 == 1 or num2 - num1 == -3:
                    answe.append(RIGHT)
                elif num2 == num1:
                    answe.append(MIDDLE)
                else:
                    answe.append(LEFT)
        return answe

    # 敌人和我的对角线，走避开敌人的那个角
    # 1， 0避开他的趋势。根据长度，太小就回去，足够大，圈U型
    # 2， 3是朝向他的趋势。那么把最短距离/2，U型的长度总共是这么多。
    answer = []
    if xe <= xn and ye <= yn:
        if now['direction'] == 1:
            if xn < xM:
                length = xM - xn
                delta = abs(yrd - yn)
                if max_dist - length - delta > 0:
                    (south, para, north) = downup(length, yrd, yn, max_dist)
                    answer = answer + [MIDDLE] * south
                    if para > 0:
                        answer.append(LEFT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if north > 0:
                        answer.append(LEFT)
                        north -= 1
                    answer = answer + [MIDDLE] * north
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 0:
            if yn < yM:
                length = yM - yn
                delta = abs(xrd - xn)
                if max_dist - length - delta > 0:
                    (east, vert, west) = rightleft(length, xrd, xn, max_dist)
                    answer = answer + [MIDDLE] * east
                    if vert > 0:
                        answer.append(RIGHT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if west > 0:
                        answer.append(RIGHT)
                        west -= 1
                    answer = answer + [MIDDLE] * west
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 2:
            if yn < yM:
                length = yM - yn
                delta = abs(xld - xn)
                if max_dist // 2 - length - delta > 0:
                    (west, vert, east) = leftright(length, xld, xn, max_dist // 2)
                    answer = answer + [MIDDLE] * west
                    if vert > 0:
                        answer.append(LEFT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if east > 0:
                        answer.append(LEFT)
                        east -= 1
                    answer = answer + [MIDDLE] * east
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 3:
            if xn < xM:
                length = xM - xn
                delta = abs(yru - yn)
                if max_dist // 2 - length - delta > 0:
                    (north, para, south) = updown(length, yru, yn, max_dist // 2)
                    answer = answer + [MIDDLE] * north
                    if para > 0:
                        answer.append(RIGHT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if south > 0:
                        answer.append(RIGHT)
                        south -= 1
                    answer = answer + [MIDDLE] * south
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)

    elif xe >= xn and ye >= yn:
        if now['direction'] == 3:
            if xn > xm:
                length = xn - xm
                delta = abs(ylu - yn)
                if max_dist - length - delta > 0:
                    (north, para, south) = updown(length, ylu, yn, max_dist)
                    answer = answer + [MIDDLE] * north
                    if para > 0:
                        answer.append(LEFT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if south > 0:
                        answer.append(LEFT)
                        south -= 1
                    answer = answer + [MIDDLE] * south
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 2:
            if yn > ym:
                length = yn - ym
                delta = abs(xlu - xn)
                if max_dist - length - delta > 0:
                    (west, vert, east) = leftright(length, xlu, xn, max_dist)
                    answer = answer + [MIDDLE] * west
                    if vert > 0:
                        answer.append(RIGHT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if east > 0:
                        answer.append(RIGHT)
                        east -= 1
                    answer = answer + [MIDDLE] * east
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 1:
            if xn > xm:
                length = xn - xm
                delta = abs(yld - yn)
                if max_dist // 2 - length - delta > 0:
                    (south, para, north) = downup(length, yld, yn, max_dist // 2)
                    answer = answer + [MIDDLE] * south
                    if para > 0:
                        answer.append(RIGHT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if north > 0:
                        answer.append(RIGHT)
                        north -= 1
                    answer = answer + [MIDDLE] * north
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 0:
            if yn > ym:
                length = yn - ym
                delta = abs(xru - xn)
                if max_dist // 2 - length - delta > 0:
                    (east, vert, west) = rightleft(length, xru, xn, max_dist // 2)
                    answer = answer + [MIDDLE] * east
                    if vert > 0:
                        answer.append(LEFT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if west > 0:
                        answer.append(LEFT)
                        west -= 1
                    answer = answer + [MIDDLE] * west
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)

    elif xe < xn and ye > yn:
        if now['direction'] == 3:
            if xn < xM:
                length = xM - xn
                delta = abs(yru - yn)
                if max_dist - length - delta > 0:
                    (north, para, south) = updown(length, yru, yn, max_dist)
                    answer = answer + [MIDDLE] * north
                    if para > 0:
                        answer.append(RIGHT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if south > 0:
                        answer.append(RIGHT)
                        south -= 1
                    answer = answer + [MIDDLE] * south
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 0:
            if yn > ym:
                length = yn - ym
                delta = abs(xru - xn)
                if max_dist // 2 - length - delta > 0:
                    (east, vert, west) = rightleft(length, xru, xn, max_dist // 2)
                    answer = answer + [MIDDLE] * east
                    if vert > 0:
                        answer.append(LEFT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if west > 0:
                        answer.append(LEFT)
                        west -= 1
                    answer = answer + [MIDDLE] * west
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 1:
            if xn < xM:
                length = xM - xn
                delta = abs(yrd - yn)
                if max_dist // 2 - length - delta > 0:
                    (south, para, north) = downup(length, yrd, yn, max_dist // 2)
                    answer = answer + [MIDDLE] * south
                    if para > 0:
                        answer.append(LEFT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if north > 0:
                        answer.append(LEFT)
                        north -= 1
                    answer = answer + [MIDDLE] * north
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 2:
            if yn > ym:
                length = yn - ym
                delta = abs(xlu - xn)
                if max_dist // 2 - length - delta > 0:
                    (west, vert, east) = leftright(length, xlu, xn, max_dist // 2)
                    answer = answer + [MIDDLE] * west
                    if vert > 0:
                        answer.append(RIGHT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if east > 0:
                        answer.append(RIGHT)
                        east -= 1
                    answer = answer + [MIDDLE] * east
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)

    elif xe > xn and ye < yn:
        if now['direction'] == 1:
            if xn > xm:
                length = xn - xm
                delta = abs(yld - yn)
                if max_dist - length - delta > 0:
                    (south, para, north) = downup(length, yld, yn, max_dist)
                    answer = answer + [MIDDLE] * south
                    if para > 0:
                        answer.append(RIGHT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if north > 0:
                        answer.append(RIGHT)
                        north -= 1
                    answer = answer + [MIDDLE] * north
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 2:
            if yn < yM:
                length = yM - yn
                delta = abs(xld - xn)
                if max_dist - length - delta > 0:
                    (west, vert, east) = leftright(length, xld, xn, max_dist)
                    answer = answer + [MIDDLE] * west
                    if vert > 0:
                        answer.append(LEFT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if east > 0:
                        answer.append(LEFT)
                        east -= 1
                    answer = answer + [MIDDLE] * east
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 3:
            if xn > xm:
                length = xn - xm
                delta = abs(ylu - yn)
                if max_dist // 2 - length - delta > 0:
                    (north, para, south) = updown(length, ylu, yn, max_dist // 2)
                    answer = answer + [MIDDLE] * north
                    if para > 0:
                        answer.append(LEFT)
                        para -= 1
                    answer = answer + [MIDDLE] * para
                    if south > 0:
                        answer.append(LEFT)
                        south -= 1
                    answer = answer + [MIDDLE] * south
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)
        elif now['direction'] == 0:
            if yn < yM:
                length = yM - yn
                delta = abs(xrd - xn)
                if max_dist // 2 - length - delta > 0:
                    (east, vert, west) = rightleft(length, xrd, xn, max_dist // 2)
                    answer = answer + [MIDDLE] * east
                    if vert > 0:
                        answer.append(RIGHT)
                        vert -= 1
                    answer = answer + [MIDDLE] * vert
                    if west > 0:
                        answer.append(RIGHT)
                        west -= 1
                    answer = answer + [MIDDLE] * west
                else:
                    answer = shortest(xn, yn, maps)
            else:
                answer = shortest(xn, yn, maps)

    return answer


def enclosure(stat, storage, order):
    try:
        storage['enclosure']
    except KeyError:
        storage['enclosure'] = []
    if order == 'Yes' or len(storage['enclosure']) == 0:
        lst = fun_enclosure(stat, storage)
        storage['enclosure'] = lst
    ans = storage['enclosure'].pop(0)
    return ans
