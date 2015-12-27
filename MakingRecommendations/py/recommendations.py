from math import sqrt

def euclidean_distance(item, person_1, person_2):
    common_item = {e for e in item[person_1] if e in item[person_2]}
    if len(common_item) == 0:
        return 0
    distance = sqrt(sum([pow(item[person_1][m] - item[person_2][m], 2) for m in common_item]))
    return 1 / (1 + distance)
    
def pearson_distance(item, person_1, person_2):
    common_item = {}
    