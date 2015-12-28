from math import sqrt

def euclidean_distance(item, elem_1, elem_2):
    common_item = {e for e in item[elem_1] if e in item[elem_2]}
    if len(common_item) == 0:
        return 0
    distance = sqrt(sum([pow(item[elem_1][m] - item[elem_2][m], 2) for m in common_item]))
    return 1 / (1 + distance)
    
def pearson_distance(item, elem_1, elem_2):
    common_item = [e for e in item[elem_1] if e in item[elem_2]]
    if len(common_item) == 0:
        return 0
    
    # 算术平均数
    p1 = [item[elem_1][m] for m in common_item]
    p2 = [item[elem_2][m] for m in common_item]
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
    
def top_matches(item, elem, n = 7, similarity = pearson_distance):
    candidates = [(other, similarity(item, elem, other)) for other in item if other != elem]
    candidates.sort(key = lambda x : x[1], reverse = True)
    return candidates[:n]

def trans_item(item):
    result = {}
    for k1 in item:
        for k2 in item[k1]:
            if k2 not in result:
                result[k2] = {}
            result[k2][k1] = item[k1][k2]
    return result
 
def get_similar_items(item, n = 21):
    result = {}
    new_item = trans_item(item)
    for e in new_item:
        near_item = top_matches(new_item, e, n)
        result[e] = near_item
    return result
    
def item_based_recommend(item, items_table, user):
    user_item = item[user]
    scores = {}
    total_sim = {}
    
    for (good, score) in user_item:
        for (other_good, similarity) in items_table[good]:
            if other_good in user_item:
                continue
            if other_good not in scores:
                scores[other_good] = 0
            scores[other_good] += score * similarity
            if other_good not in total_sim:
                total_sim[other_good] = 0
            total_sim[other_good] += similarity
     
     # ranking
     rank_list = [(e, float(score) / total_sim[e]) for (e, score) in scores]
     rank_list.sort(key = lambda x : x[1], reverse = True)
     return rank_list