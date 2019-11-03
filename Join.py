import numpy as np
from random import randrange
import time


def make_inverted(filename,  b):    # 对b属性进行连接
    # 频率就是num的collection的长度
    # collection是num的主键
    # origin把连接的公共num放在前，其它在后
    inverted_map = {}
    origin = {}
    flag = 0
    with open(filename, "rb") as f:
        for fLine in f:
            s = fLine.decode().strip().replace("\n", "").split("|")
            if len(s) != 1:
                origin_v = []
                collection = []
                num = s[b]
                for i in range(len(s)):
                    if i != b:
                        collection.append(s[i])
                origin_v.append(num)
                origin_v.append(collection)
                origin[flag] = origin_v
                flag += 1
                if num not in inverted_map.keys():
                    l = []
                    l.append(collection)
                    inverted_map[num] = l
                else:
                    inverted_map[num].append(collection)
    return origin, inverted_map


def compute_join(R1, b1, R2, b2):
    # 对R1的吧b1属性和R2的b2属性进行连接
    # result中第一个是b值，第二部分个是R1其它属性，第三部分是R2其它属性
    result = []
    origin_R1, R1_inverted = make_inverted(R1, b1)
    origin_R2, R2_inverted = make_inverted(R2, b2)
    origin_R1_allT = len(origin_R1.keys())
    origin_R2_allT = len(origin_R2.keys())
    max_len = 0
    max_value = 0
    for k in R2_inverted.keys():
        if len(R2_inverted[k]) > max_len:
            # print(R2_inverted[k])
            max_len = len(R2_inverted[k])
            max_value = k
    # print(max_value)
    while 1 == 1:
        r1 = origin_R1[int(np.random.rand() * origin_R1_allT)]
        r1_b = r1[0]
        if r1_b in R2_inverted.keys():
            r2_b_num = len(R2_inverted[r1_b])
            # print(r2_b_num / int(max_value))
            # print(r2_b_num)
            # print(int(max_len))
            if np.random.rand() < r2_b_num / int(max_len):
                r = r1
                r2_not_b = R2_inverted[r1_b][int(r2_b_num * np.random.rand())]
                # 避免改变r1使用+
                r = r + [r2_not_b]
                return r
                # print(r)
                # 避免重复输出
                # if r not in result:
                #   result.append(r)

    # return result


def multi_way_join(R1, b12, b13,  R2, b2, R3, b3):
    # b12 < b13
    # R1外键，R2、R3主键
    # 对R1、R2、R3顺次做连接
    result = compute_join(R1, b12, R2, b2)
    f1 = open('result_of_multi.txt', 'w')
    for t in result:
        f1.write(str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "") + "\n")
    f1.close()
    result1 = compute_join("result_of_multi.txt", b13, R3, b3)
    f1 = open('result_of_multi.txt', 'w')
    for t in result1:
        f1.write(str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "") + "\n")
    f1.close()


def findOne(filename):
    i = 0
    content = {}
    with open(filename, "rb") as f:
        for fLine in f:
            s = fLine.decode().strip()
            # print(s)
            i = i + 1
            content[i] = s

    random_index = randrange(1, i + 1)
    r = content[random_index]
    f1 = open(filename, 'w')
    f1.write(r)
    f1.close()
    return r


def half_join(s, b1, R2, b2):
    # 对R1的吧b1属性和R2的b2属性进行连接
    # result中第一个是b值，第二部分个是R1其它属性，第三部分是R2其它属性
    # R1中元组数必须为1
    result = []
    # origin_R1, R1_inverted = make_inverted(R1, b1)
    origin_R2, R2_inverted = make_inverted(R2, b2)
    # r1 = origin_R1[0]
    S = s.split("|")
    r1 = []
    r1.append(S[b1])
    for i in range(len(S)):
        if i != b1:
            r1.append(S[i])
    r1_b = r1[0]
    if r1_b in R2_inverted.keys():
        for i in range(len(R2_inverted[r1_b])):
            r = r1
            r2_not_b = R2_inverted[r1_b][i]
            r = r + [r2_not_b]
            if r not in result:
                result.append(r)
    return result


def framework():
    r0 = "1|4"
    result1 = half_join(r0, 1, "R1.txt", 3)
    # print(result1)
    f1 = open('result_of_S.txt', 'w')
    for t in result1:
        f1.write(str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "") + "\n")
    f1.close()
    r1 = findOne('result_of_S.txt')
    result2 = half_join(r1, 3, "R2.txt", 0)
    # print(result2)

    f1 = open('result_of_S.txt', 'w')
    for t in result2:
        f1.write(str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "") + "\n")
    f1.close()
    '''
    findOne('result_of_S.txt')
    
    result3 = half_join('result_of_S.txt', 4, "R3.txt", 0)
    # print(result3)
    f1 = open('result_of_S.txt', 'w')
    for t in result3:
        f1.write(str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "") + "\n")
    f1.close()
    '''
    final = findOne('result_of_S.txt')

    return final


def calculate_max_freq(inverted_map):
    max_len = 0
    max_value = 0
    for k in inverted_map.keys():
        if len(inverted_map[k]) > max_len:
            # print(R2_inverted[k])
            max_len = len(inverted_map[k])
            max_value = k
    return max_value, max_len


if __name__ == '__main__':
    start = time.time()
    map_tuple = {}
    for i in range(1000):
        t = compute_join("R1.txt", 1, "R2.txt", 0)
        x = str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "")
        if x in map_tuple.keys():
            map_tuple[x] = map_tuple[x] + 1
        else:
            map_tuple[x] = 1
    end = time.time()
    print("\ntime: " + str(end - start) + "\n")
    for k in map_tuple.keys():
        print(k + " : " + str(map_tuple[k]))

    f1 = open('result_of_two.txt', 'w')
    for t in map_tuple.keys():
        f1.write(t + "  " + str(map_tuple[t]) + "\n")
    f1.close()
    multi_way_join("R1.txt", 1, 2,  "R2.txt", 0, "R3.txt", 0)
    """
    # R1的外键，R2的主键
    
    framework()
    map_tuple = {}
    for i in range(300):
        x = framework()
        if x in map_tuple.keys():
            map_tuple[x] = map_tuple[x] + 1
        else:
            map_tuple[x] = 1

    # print(map_tuple)
    f1 = open('S-result.txt', 'w')
    for t in map_tuple.keys():
        f1.write(t + "  " + str(map_tuple[t]) + "\n")
    f1.close()
"""






