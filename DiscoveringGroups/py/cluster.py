#encoding:utf8
from math import sqrt
import random

def pearson(v1, v2):
    # 算术平均数
    v_len = len(v1)
    assert v_len == len(v2)
    v1_mean = float(sum(v1)) / v_len
    v2_mean = float(sum(v2)) / v_len
    
    # 向量减去算术平均数
    v_1 = map(lambda x : x - v1_mean, v1)
    v_2 = map(lambda x : x - v2_mean, v2)
    
    #计算 p_1 和 p_2 的余弦距离
    v_1_2_dot = sum([v_1[i] * v_2[i] for i in xrange(v_len)])
    v_1_mo = sqrt(sum(e**2 for e in v_1))
    v_2_mo = sqrt(sum(e**2 for e in v_2))
    
    #当v_1_mo = 0 可以这么理解，以电影评分举例
    # 0 表示用户对每一部电影的评分都是一样的（或者没有评分）
    #那表示这个用户没有偏好，也就没有参考价值，所以
    #和其他用户的相似是0 
    if v_1_mo == 0 or v_2_mo == 0:
        return 0
    return v_1_2_dot / (v_1_mo * v_2_mo)
    
def cluster_distance(v1, v2):
    return 1.0 - pearson(v1, v2)
    
def kcluster(rows, distance = cluster_distance, k = 2, iternum = 10):
    row_len = len(rows[0])
    row_num = len(rows)
    range = [(min([row[i] for row in rows]), max([row[i] for row in rows])) 
            for i in xrange(row_len)]
    clusters = [[range[i][0] + random.random() * (range[i][1] - range[i][0]) for i in xrange(row_len)] for j in xrange(k)]
    
    last_matches = None
    cur_matches = None
    for t in xrange(iternum):
        print 'Iteration %d' % t
        cur_matches = [set() for c in xrange(k)]
        #遍历每个点，将点放到最近的中心点下面
        for rowid in xrange(row_num):
            row = rows[rowid]
            min_d = 10000
            min_c = 0
            for c in xrange(k):
                d = distance(row, clusters[c])
                if d < min_d:
                    min_d = d
                    min_c = c
            cur_matches[min_c].add(rowid)
        if cur_matches == last_matches:
            break
        last_matches = cur_matches
         #重新计算聚类中心点
        for c in xrange(k):
            c_row_num = len(cur_matches[c])
            if c_row_num == 0:
                continue
            clusters[c] = [sum([rows[rowid][i] for rowid in cur_matches[c] ]) / float(c_row_num) for i in xrange(row_len)]
    return cur_matches

def main(k):
    from data import d
    rows = []
    map = []
    for key in d:
        rows.append(d[key])
        map.append(key)
    cluster = kcluster(rows, k = int(k))
    for c in cluster:
        print '-'*7
        for e in c:
            print map[e]
        print '-'*7
        
if __name__ == '__main__':
    import sys
    main(sys.argv[1])
