# 欧几里得距离（euclidean distance）

在python中可以这样计算二维空间两个点的欧几里得距离，多维空间下类似
    
    >>> from math import sqrt
    >>> sqrt(pow(x1 - x2) + pow(y1 - y2))
    
距离越短的点越相似，实际使用过程中，相似度函数返回值需要和实际相似度正相关。 
   
    >>> def similarity(point_1, point-2):
    >>>     distance = sqrt(pow(point_1.x - point_2.x) + pow(point_1.y - point_2.y))
    >>>     return 1 / (distance + 1)

# 皮尔逊相关系数 (pearson correlation coefficient)

以电影评分为例，有些用户评分的基准较高，有些较低，大多数是差不多的（符合高斯分布？）。这样用欧几里德距离根据电影打分来
计算两个用户的相似度的话误差比较大，所以是否有一种方法来对每个用户的打分做一下预处理（抹平不同的基准），然后再对打分计算
距离。

皮尔逊相关系数，就是做这样的事。我对皮尔逊相关系数的理解如下，计算两个向量***X***,***Y***的皮尔逊相似度，先将向量
的每一维减去向量的算数平均数（抹平基准）得到向量***X1***, ***Y1***; ***X***, ***Y***的皮尔逊相似度就是 ***X1*** ,
***Y1*** 的余弦距离。
    
    >>> from math import sqrt
    >>> x_mean = float(sum(x)) / len(x)
    >>> y_mean = float(sum(y)) / len(y)
    >>> x_1 = map(lambda x : x - x_mean, x)
    >>> y_1 = map(lambda x : x - y_mean, y)
    >>> dot_xy = sum([x_1[i] * y_1[i] for i in xrange(len(x_1))])
    >>> x_1_mo = sqrt(sum([e**2 for e in x_1]))
    >>> y_1_mo = sqrt(sum([e**2 for e in y_1]))
    >>> pearson_distance = dot_xy / (x_1_mo * y_1_mo)
     