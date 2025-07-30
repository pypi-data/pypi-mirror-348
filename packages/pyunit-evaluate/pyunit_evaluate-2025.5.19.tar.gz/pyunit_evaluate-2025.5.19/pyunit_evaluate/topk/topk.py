from abc import ABCMeta, abstractmethod

from .edges import Edges


class TopK(metaclass=ABCMeta):

    def __init__(self, predict: Edges, true: Edges, keep):
        self.predict = predict
        self.true = true
        self.k = keep

    @abstractmethod
    def __matmul__(self, k: int) -> float:
        raise NotImplementedError
