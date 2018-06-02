# 公告
##  下下次组会前准备工作（待定）
- 大家组会前准备以下三方面：

1. 思考我们的程序下一步怎么走

    i.	Level1：是否还是event驱动的

    ii.	Level2：是否分开两级程序做判断

    iii.	Level3：如果继续目前的思路，那么第一级程序和第二级怎么优化

2. 大家准备讲讲自己module程序的实现思路，忽略细节，重点在每一个函数的功能。可能有什么缺陷。

3. 我会搞到投影的，有需要把自己的电脑带上，有想法提前整理。以及，网上帮我做一下调研，以前有没有人写过“纸袋圈地”的代码，他们怎么实现的。
  
- 平台给的参数有变动。我们的version1完成以后，以后要做出调整。组会上我们商量怎么封装。

## 工程使用方法
1.	下面的测试，请将main_package文件和DSA_group1_package文件夹放到平台程序的AI文件夹下。
2.	切记，用pycharm打开工程，一定要打开paper.io.sessdsa-master这个platform文件夹作为当前工程，否则import报错。
3.	请不要修改函数和文件的命名。
4.  每次请修改自己对应的DSA_group1_package中的.py文件。

# 项目进展
## 20180602
### 杜文博
1. 完成attack debug。
### 杨正浩和李泽凡
1. 完成整体version1的调试和封装。
## 20180601
### 李泽凡
1.	完成项目代码封装
2.	部分完成接口调整和coding规范文档
## 20180531
### 李泽凡
1.	完成了对第二级程序的封装。
2.	完成了path_to/find_path的封装。
3.  find_path 添加了storage参数，否则报错；上述修改通过了测试。
4.  协助完成enclosure模块的调试

### 钟若愚
1.  完成了enclosure模块的调试

## 20180530 (short summary)
### 杨正浩
1.	加入了load函数
2.	修复了事件选择时的bug
3.	以子函数返回单个字符串为基础重构代码
4.	修改了space_check函数，抛弃了递归方式，使得速度更快，并且不会递归栈溢出
5.	path_to函数可以考虑目标不存在情况了

### 张浩波
1.	添加了新的撤退函数，已经调试完毕
2.	添加了新的功能，如果纸带头紧挨着目标区域，返回['dis']为1，['map']和['map2']为None，['start']和['start2']是紧挨的点的坐标
3.	find_path函数添加了一项功能，当纸带头紧邻目标区域时直接返回相邻的点，不返回map

### 杜文博
1.	基本实现简单模式下进攻方案的确定
2.	在双方带头错开的情况下的路线规划只简单的区分是否有己方纸带阻挡
3.	未调试

### 钟若愚
1.	完成圈地函数书写
2.	正在调试
3.  solo调试有结果，但是走到边缘会死，需要将边缘的参数修改（原来是MAXx和MAXY）。

### 李泽凡
1.	添加了summary函数；
2.	添加了测试play每次运行时间函数；
3.	上述通过了测试。