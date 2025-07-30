from .topk import TopK


class MAP(TopK):
    """
    在链路预测任务中，Mean Average Precision (MAP，平均精度)是一种常用的评估指标，用于衡量模型预测链路排序的质量。下面我将详细介绍AP的计算方法和解释。

    AP的计算步骤
    1. 获取预测排序：模型为所有可能的链路(或测试集中的链路)分配一个分数，并根据分数降序排列。
    2. 确定相关项：在排序列表中标记哪些链路是真实存在的(正例)。
    3. 计算AP@k：对于排序列表中的每个正例位置k，计算前k项中的正例比例。
    4. 计算MAP：对所有正例位置的精度取平均。
    """

    def __matmul__(self, k: int) -> float:
        values = []

        for node, edges in self.predict.group('node1').items():
            if len(edges) > 1:
                edges = edges.sort(key=lambda x: x.score, reverse=True)
            edges = edges[:k]
            value, one = 0, 0
            for idx, item in enumerate(edges.items(), start=1):
                edge, flag = self.true.has_edge(item)
                # 只记录真实存在的链路
                if flag and edge.score == 1:
                    one += 1
                    value += one / idx

            ap = (value / one) if one else 0
            values.append(ap)

        return round(sum(values) / len(values), self.k)
