## 基于用户的协作型过滤(user-based collaborative filtering)

## 基于物品的协作型过滤(item-based collaborative filtering)

> 在拥有大量数据集的情况下，item-based有更好的效果，并且item-based允许我们
> 将大量计算任务预先执行。

思想
> 为每一件物品预先计算好最为相近的其他物品。 当为某个用户推荐的时候，查看
> 用户曾经评论的物品，从中选出排位靠前的，构造一个加权列表，其中包含了与这些
> 选中物品最为相近的其他物品。

## user-based or item-based?

> 在针对大数据集生成推荐列表时，item-based明显要比user-based更快
> 但是item-based有维护物品相似度表的额外开销。
> 对于稀疏数据集，基于item-based通常优于基于用户的过滤方法，而对于密集
> 数据集而言，二者的效果几乎一样。