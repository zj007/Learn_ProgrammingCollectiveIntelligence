# 欧几里得距离
[百度百科](http://baike.baidu.com/link?url=L4ztlXcUSY3qbyFDjrzXtn4sa2SDe-z_eLpSegstJCCl3MkmkQX-zy_kGRlZUb7cvmJvKaY_tcGXKFYg8dhO_zLem2Jvf94aYGmCsL7Le-5PE2qvBOCaX1BI9li4ONfiIz6MWQYIJrQB2U8e8Wp6nxL6onv7zz2NWYcoQfghGlSjvK5rdaexhMW_nK5d-WtIvaqaI5F_DPGvBcFcnQIhLq)

>欧几里得度量（euclidean metric）（也称欧式距离）是一个通常采用的距离定义，指在m维空间中两个点之间的真实距离，或者向量的自然长度（即该点到原点的距离）。在二维和三维空间中的欧氏距离就是两点之间的实际距离。

![](http://static.oschina.net/uploads/space/2014/0622/222143_fdLt_1439326.jpg)

在python中可以这样计算二维空间两个点的欧几里得距离，多维空间下类似

    >>> from math import sqrt
    >>> sqrt(pow(x1 - x2) + pow(y1 - y2))
    
距离越短的点越相似   