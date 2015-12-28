from math import sqrt

def euclidean_distance(item, person_1, person_2):
    common_item = {e for e in item[person_1] if e in item[person_2]}
    if len(common_item) == 0:
        return 0
    distance = sqrt(sum([pow(item[person_1][m] - item[person_2][m], 2) for m in common_item]))
    return 1 / (1 + distance)
    
def pearson_distance(item, person_1, person_2):
    common_item = [e for e in item[person_1] if e in item[person_2]]
    if len(common_item) == 0:
        return 0
    
    # 算术平均数
    p1 = [item[person_1][m] for m in common_item]
    p2 = [item[person_2][m] for m in common_item]
    length = len(common_item)
    p1_mean = float(sum(p1)) / length
    p2_mean = float(sum(p2)) / length
    
    # 向量减去算术平均数
    p_1 = map(lambda x : x - p1_mean, p1)
    p_2 = map(lambda x : x - p2_mean, p2)
    
    #计算 p_1 和 p_2 的余弦距离
    p_1_2_dot = sum([p_1[i] * p_2[i] for i in xrange(len(p_1))])
    p_1_mo = sqrt(sum(e**2 for e in p_1))
    p_2_mo = sqrt(sum(e**2 for e in p_2))
    
    if p_1_mo == 0 || p_2_mo == 0:
        return 0
    return p_1_2_dot / (p_1_mo * p_2_mo)
    
def topMatches(item, person, n, similarity = pearson_distance):
    candidates = [(other, similarity(item, person, other)) for other in item if other != person]
    candidates.sort(key = lambda x : x[1], reverse = True)
    return candidates[:n]