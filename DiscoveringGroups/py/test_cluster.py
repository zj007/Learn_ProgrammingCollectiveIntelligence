import sys
from cluster import kcluster
from data import d

def equal(lhd, rhd):
    '''
    lhd & rhd's type is below:
    [set(int, int), set(), ...]
    '''
    lhd_set = set()
    rhd_set = set()
    for e in lhd:
        if not len(e):
            continue
        lhd_set.add('_'.join(sorted([str(i) for i in e])))
    for e in rhd:
        if not len(e):
            continue
        rhd_set.add('_'.join(sorted([str(i) for i in e])))
    if lhd_set == rhd_set:
        return True
    return False

def main(k, test_freq = 100):
    rows = []
    for key in d:
        rows.append(d[key])
    last_cluster = kcluster(rows, k = k)
    print 'first cluster : %s' % last_cluster
    only_one_cluster = True
    for i in xrange(test_freq):
        cur_cluster = kcluster(rows, k = k)
        if not equal(last_cluster, cur_cluster):
            print 'cluster %d: %s' %(i, cur_cluster)
            only_one_cluster = False
            last_cluster = cur_cluster
    if only_one_cluster:
        print 'stable'
    else:
        print 'not stable'

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
