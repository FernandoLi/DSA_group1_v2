import match_core, match_interface
import os, sys


def process_task(data_queue, path, names, log_format, rounds, match_params):
    '''
    子进程执行两玩家多局对决

    params:
        data_queue - 数据队列
        path - 玩家模块所在路径
        names - 玩家名称
        log_format - 记录文件名格式
            比赛记录将保存为log_format % (*names, index)路径
        rounds - 单向比赛局数（双向进行）
        match_params - 比赛参数
    '''
    # 读取玩家
    sys.path.append(path)
    players = [__import__(n) for n in names]

    # 双向比赛
    win_counts = [0, 0]
    for i in 0, 1:
        # 初始化存储空间、局数统计
        match_core.STORAGE = [{}, {}]

        # 第二次交换比赛
        if i:
            players = players[::-1]
            names = names[::-1]
            win_counts = win_counts[::-1]

        # 总初始化函数
        for i in range(2):
            try:
                players[i].init(match_core.STORAGE[i])
            except:
                pass

        # 运行多局比赛
        for i in range(rounds):
            # 进行比赛，获取记录
            match_log = match_core.match(players, names, *match_params)

            # 生成比赛记录
            log_name = log_format % (*names, i)
            match_interface.save_match_log(match_log, log_name)

            # 比赛结果传递至队列
            result = match_log['result']
            data_queue.put((names, result))

            # 统计比赛结果，若胜利过半则跳出
            if result[0] is not None:
                win_counts[result[0]] += 1
                if win_counts[result[0]] > rounds:
                    break

        # 总总结函数
        for i in range(2):
            try:
                players[i].summaryall(match_core.STORAGE[i])
            except:
                pass


if __name__ == "__main__":
    '''
    用法：
        python3 this.py 分组名 [晋级人数(默认8)]
    '''

    # 导入必要库
    from multiprocessing import Process, Queue
    from sqlite3 import connect
    from time import perf_counter as pf
    from random import shuffle, randrange
    from platform import system

    # 初始化环境
    if 'init':
        # 常量参数
        MATCH_PARAMS = (51, 101, 2000, 30)  # k, h, turn, time
        ROUNDS = 10  # 比赛局数（单向）
        MAX_TASKS = 12  # 最大子进程数
        TIMEOUT = 65 * ROUNDS  # 超时限制
        try:
            MAX_PROMOTION = int(sys.argv[2])  # 晋级人数
        except:
            MAX_PROMOTION = 8

        # 组别
        TEAM = sys.argv[1]
        # TEAM = 'AI'
        LOG_FORMAT = TEAM + "/log/%s-%s(%d).zlog"
        AI_PATH = os.path.abspath(TEAM)

        # 屏蔽AI自带print
        class null_stream:
            def read(*args):
                pass

            def write(*args):
                pass

            def flush(*args):
                pass

        sys.stdout = null_stream

    # 数据结构
    if 'IO':
        # 进程队列初始化
        dataq = Queue()

        # 数据库初始化
        db = connect('%s.db' % TEAM)
        try:  # 清空已有数据
            db.execute("drop table match_result")
        except:
            pass
        db.execute(
            "CREATE TABLE `match_result` ( `plr1` TEXT, `plr2` TEXT, `flag` TEXT, `win1` INTEGER, `win2` INTEGER, `tie` INTEGER, PRIMARY KEY(`plr1`,`plr2`) )"
        )  # 建表
        db.commit()

        # 当前任务池
        running_tasks = []  # 运行进程

        # 比赛结果统计字典
        rounds_stat = {}
        results_stat = {}

    # 生成赛制
    if 'get schedule':
        # 获取玩家，信息保存为同目录txt文件
        players = []
        sys.path.append(AI_PATH)
        with open('%s/errors.txt' % TEAM, 'w') as errlist:
            for file in os.listdir(TEAM):
                if file.endswith('.py'):
                    # 提取含play函数模块
                    try:
                        name = file[:-3]
                        ai = __import__(name)
                        ai.play
                        players.append(name)

                    # 读取时出错
                    except Exception as e:
                        print('读取%r时出错：%s' % (file, e), file=errlist)
        with open('%s/players.txt' % TEAM, 'w') as plrlist:
            for plr in players:
                print(plr, file=plrlist)
        max_name_len = max(map(len, players))

        # 生成赛制顺序
        tasks_buffer = []
        for i in range(len(players) - 1):
            for j in range(i + 1, len(players)):
                if randrange(2):
                    tasks_buffer.append((players[i], players[j]))
                else:
                    tasks_buffer.append((players[j], players[i]))
        shuffle(tasks_buffer)
        players.sort()

    # 函数定义
    if 'helpers':

        def flush_queue():
            '''
            清空队列内容并进行统计
            '''
            while not dataq.empty():
                update_stat(*dataq.get())

        def update_stat(names, result):
            '''
            更新单次比赛结果

            params:
                names - 双方名称（字典关键字）
                result - 比赛结果元组
            '''
            if names not in rounds_stat:
                rounds_stat[names] = {0: 0, 1: 0, None: 0}
            rounds_stat[names][result[0]] += 1

        def update_pair(names, flag):
            '''
            总结双方多局对战结果

            params:
                names - 双方玩家名
                flag - 对局结果（FINISHED或TIMEOUT）
            '''
            # 清空统计队列
            flush_queue()

            # 双向加入数据库
            stat1 = rounds_stat.get(names, {0: 0, 1: 0, None: 0})
            db.execute(
                'INSERT INTO match_result (plr1,plr2,flag,win1,win2,tie) VALUES ("%s","%s","%s",%s,%s,%s)'
                % (*names, flag, stat1[0], stat1[1], stat1[None]))
            stat2 = rounds_stat.get(names[::-1], {0: 0, 1: 0, None: 0})
            db.execute(
                'INSERT INTO match_result (plr1,plr2,flag,win1,win2,tie) VALUES ("%s","%s","%s",%s,%s,%s)'
                % (*names[::-1], flag, stat2[0], stat2[1], stat2[None]))
            db.commit()

            # 统计比赛结果
            stat = [stat1[i] + stat2[1 - i] for i in (0, 1)]
            if flag == 'FINISH':
                if stat[0] > stat[1]:
                    results_stat[names] = '+'
                    results_stat[names[::-1]] = '-'
                elif stat[0] < stat[1]:
                    results_stat[names] = '-'
                    results_stat[names[::-1]] = '+'
                else:
                    results_stat[names] = '0'
                    results_stat[names[::-1]] = '0'
            else:
                results_stat[names] = 'x'
                results_stat[names[::-1]] = 'x'

        def visualize(file=sys.__stdout__):
            '''
            可视化比赛过程

            params:
                file - 输出流
            '''
            # 清屏
            if file == sys.__stdout__:
                if system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')

            # 绘制表格，统计得分
            scores = []
            print('Status:', file=file)
            for plr in players:
                score = 0
                line = plr.rjust(max_name_len) + ': |'
                for cp in players:
                    if plr == cp:
                        line += '*****'
                    else:
                        pair = (plr, cp)
                        if pair in results_stat:
                            pair_result = results_stat[pair]
                            line += pair_result.center(5)
                            if pair_result == '+':
                                score += 3
                            elif pair_result == '0':
                                score += 1
                        elif pair in rounds_stat:
                            line += '%02d-%02d' % (rounds_stat[pair][0],
                                                   rounds_stat[pair][1])
                        else:
                            line += '     '
                    line += '|'
                line += '  %d' % score
                print(line, file=file)
                scores.append((plr, score))

            # 得分排序
            print('\n\nRanking:', file=file)
            scores.sort(key=lambda x: -x[1])
            for i in range(len(scores)):
                if i == MAX_PROMOTION:
                    print('-' * 40, file=file)
                plr = scores[i]
                line = plr[0].rjust(max_name_len) + ' |'
                line += '##' * plr[1] + ' %d' % plr[1]
                print(line, file=file)

    # 主事件循环
    visualize_timer = pf()
    visualize()
    while 1:
        now = pf()

        # 0. 清空队列缓冲区
        flush_queue()

        # 1. 移除已结束任务
        for i in range(len(running_tasks)):
            names, task, time = running_tasks[i]
            flag = None
            if not task.is_alive():
                flag = 'FINISH'
            elif now - time > TIMEOUT:
                task.terminate()
                flag = 'TIMEOUT'
            if flag:
                update_pair(names, flag)
                running_tasks[i] = None
        running_tasks = [i for i in running_tasks if i]

        # 2. 加入新任务
        if tasks_buffer and len(running_tasks) < MAX_TASKS:
            names = tasks_buffer.pop()
            process = Process(
                target=process_task,
                args=(dataq, AI_PATH, names, LOG_FORMAT, ROUNDS, MATCH_PARAMS))
            process.start()
            running_tasks.append((names, process, now))

        # 3. 可视化
        if now - visualize_timer > 0.5:
            visualize()
            visualize_timer = now

        # 4. 若运行完毕则跳出
        if not running_tasks:
            break
    visualize()

    # 写入结果
    with open('%s/RESULT.txt' % TEAM, 'w') as result:
        visualize(result)

    # 打包比赛记录
    for plr in players:
        op = "cd %s/log; tar -czf %s.tgz *%s*" % (TEAM, plr, plr)
        print('$ ' + op, file=sys.__stdout__)
        os.system(op)