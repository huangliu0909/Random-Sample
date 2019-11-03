import numpy as np
import time
import matplotlib.pyplot as plt


def make_inverted(R):    # 对b属性进行连接
    inverted_map = {}
    for s in R:
        if s[0] not in inverted_map.keys():
            inverted_map[s[0]] = []
        inverted_map[s[0]].append(s[1])
    return  inverted_map


def calculate_max_freq(inverted_map):
    max_len = 0
    max_value = 0
    for k in inverted_map.keys():
        if len(inverted_map[k]) > max_len:
            # print(R2_inverted[k])
            max_len = len(inverted_map[k])
            max_value = k
    return max_len


def sample(R_num, t_num, value):
    R = {}
    W = {}
    x = {}

    inverted_map = {}
    for i in range(R_num):
        LL = []
        for j in range(t_num):
            L = []
            L.append(np.random.randint(value))
            L.append(np.random.randint(value))
            LL.append(L)
        R[i + 1] = LL
        inverted_map[i + 1] = make_inverted(LL)
        x[i + 1] = calculate_max_freq(inverted_map[i + 1])
        # print(x[i + 1])
    for i in range(R_num):
        xx = 1
        for j in range(R_num - i - 1):
            xx = xx * x[j + 2]
        W[i + 1] = xx
    # print(W)
    flag = 0
    while 1 == 1:
        t = [1, 4]
        W[0] = W[1]
        flag += 1
        for i in range(R_num - 1):
            w_ = W[i]
            # print(i + 2)
            # print(t[len(t) - 1])
            if t[len(t) - 1] not in inverted_map[i + 1].keys():
                break
            l = len(inverted_map[i + 1][t[len(t) - 1]])
            W[i] = W[i + 1] * l
            # print("W[i+1]  " + str(W[i + 1]))
            # print("w_   " + str(w_))
            # print("rejection rate: " + str(1 - W[i + 1] / w_))
            if np.random.rand() < 1 - W[i + 1] / w_:
                break
            t.append(inverted_map[i + 1][t[len(t) - 1]][np.random.randint(l)])

        if len(t) == R_num + 1:
            return t, flag


if __name__ == '__main__':
    map_tuple = {}
    '''
    rr = 3
    tt = 100
    value = 10
    R_num_s = range(1, 9)
    t_num_s = range(1000, 50000, 1000)
    values = range(5, 30)
    reject_R = []
    reject_T = []
    vt_x = []
    reject_vt_y = []
    for v in values:
        print(v)
        vt_x .append(v / tt)
        t, flag = sample(rr, tt, v)
        reject_vt_y.append(1 - 1 / flag)
    plt.plot(vt_x, reject_vt_y)
    plt.xlabel("value range/tuple num")
    plt.ylabel("rejection rate")
    plt.title("relation num = " + str(rr))
    plt.show()
    for r_num in R_num_s:
        print(r_num)
        t, flag = sample(r_num, tt, value)
        reject_R.append(1-1/flag)
    plt.plot(R_num_s, reject_R)
    plt.xlabel("relation num")
    plt.ylabel("rejection rate")
    plt.title("tuple num = " + str(tt) + "  attr value:  0 - " + str(value))
    plt.show()
    for t_num in t_num_s:
        print(t_num)
        t, flag = sample(rr, t_num, value)
        reject_T.append(1-1/flag)
    plt.plot(t_num_s, reject_T)
    plt.xlabel("tuple num")
    plt.ylabel("rejection rate")
    plt.title("relation num = " + str(rr) + "  attr value: 0 - " + str(value))
    plt.show()


'''
    start = time.time()
    t_num = 30
    R_num = 2
    vv = 5
    for i in range(1000):
        t, flag = sample(R_num, t_num, vv)
        x = str(t).replace("[", "").replace("]", "").replace(",", "|").replace("\'", "").replace(" ", "")
        if x in map_tuple.keys():
            map_tuple[x] = map_tuple[x] + 1
        else:
            map_tuple[x] = 1
    end = time.time()
    print("\ntuple num: " + str(t_num) + "  Relation num : " + str(R_num) + "  value range: 0 - " + str(vv))
    print("time: " + str(end - start))
    for k in map_tuple.keys():
        print(k + " : " + str(map_tuple[k]))
    # print(map_tuple)




