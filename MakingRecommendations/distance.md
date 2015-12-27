# 欧几里得距离（euclidean distance）
[百度百科](http://baike.baidu.com/link?url=L4ztlXcUSY3qbyFDjrzXtn4sa2SDe-z_eLpSegstJCCl3MkmkQX-zy_kGRlZUb7cvmJvKaY_tcGXKFYg8dhO_zLem2Jvf94aYGmCsL7Le-5PE2qvBOCaX1BI9li4ONfiIz6MWQYIJrQB2U8e8Wp6nxL6onv7zz2NWYcoQfghGlSjvK5rdaexhMW_nK5d-WtIvaqaI5F_DPGvBcFcnQIhLq)的解释

>欧几里得度量（euclidean metric）（也称欧式距离）是一个通常采用的距离定义，指在m维空间中两个点之间的真实距离，或者向量的自然长度（即该点到原点的距离）。在二维和三维空间中的欧氏距离就是两点之间的实际距离。

>![](http://static.oschina.net/uploads/space/2014/0622/222143_fdLt_1439326.jpg)
(来自百度图片)

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