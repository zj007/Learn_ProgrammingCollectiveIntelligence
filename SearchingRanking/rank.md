# 排序

## 1 基于内容的排序

### 1.1 单词频度

直观上看，文档包含的查询词的数量越多，那文档主题越可能和查询词相关

### 1.2 文档位置

文档的主题有可能会出现在文档的开始处

### 1.3 单词距离

如果查询条件中有多个单词，那他们再文档中出现的位置应该靠的很近

## 2 利用外部链接回指

>当对存在可疑内容的网页或垃圾内容制造者生成的网页建立索引时，这一方法
>特别有效，因为与包含真实内容的网页相比，这些网页被他人引用的可能性非常小

### 2.1 简单计数

统计指向当前网页的外链数量，数量越大，则当前网页的质量越好。

### 2.2 pagerank

> 该算法为每一个网页都赋予了一个指示网页重要程度的评价值。网页的重要性
> 是依据指向该网页的所有其他网页的重要性，以及这些网页中所包含的链接数求得

原理

> 理论上pagerank计算的是某个人在任意次连接点击后到达某一网页的可能性。
> 如果某个网页拥有来自其他热门网页的外部回指链接越多，人们无意间到达
> 该网页的可能性也就越大。当然，如果用户始终不停地点击，那么他们终将
> 到达每一个网页，但是大多数人在浏览一段时间后都会停止点击。为了反映
> 这一情况，pagerank还使用了一个值为0.85的**阻尼因子**，用以指示用户
> 持续点击每个网页中链接的概率为85%。另外，每个网页的评价值都有个最小
> 值0.15


例子

> 网页B、C和D均指向A，它们的pagerank值已经算出来了，B还指向另外3个网页
> C指向其他4个网页，D只指向A。计算PR(A)如下
> 
    PR(A) = 0.15 + 0.85 * (PR(B) / links(B) + PR(C) / links(C) + PR(D) / links(D))
          = 0.15 + 0.85 * (0.5 / 4 + 0.7 / 5  + 0.2 / 1)
          = 0.15 + 0.85 * 0.465
          = 0.54525
          
> 关于初始值，一般每个网页赋予初始值 1.0， 初始值的设定不影响最终的网页pr值；
> 经过充分迭代后，会接近网页真实的PR值

### 2.3 利用连接文本

> 大多时候，相比于被链接的网页自身所提供的信息而言，我们从指向该网页
> 的链接中所得到的信息会更有价值。

## 3 从点击行为中学习

### 3.1 多层感知机网络（MLP）（神经网络）

包含 输入层， 隐藏层（多层）， 输出层
