import random
LEFT = 'L'
RIGHT = 'R'
MIDDLE = 'M'
for i in range(10):
    dlist = [LEFT, RIGHT, MIDDLE]
    random.shuffle(dlist)
    print(dlist)