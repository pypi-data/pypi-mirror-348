from .topk import TopK


class HR(TopK):
    """

    """

    def __matmul__(self, k: int) -> float:
        values = []

        for node, edges in self.predict.group('node1').items():
            edges = edges[:k]

            has = 0
            for item in edges.items():
                # 判断是正样本
                edge, flag = self.true.has_edge(item)
                if flag and edge.score == 1:
                    has = 1
                    break
            values.append(has)
        return round(sum(values) / len(values), self.k)
