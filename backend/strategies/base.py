from abc import ABC, abstractmethod
import random
class BaseStrategy(ABC):
    def __init__(self, seed=None): self.rng = random.Random(seed)
    @abstractmethod
    def generate_one(self): ...
    def draw_unique(self, population=range(1,26), k=15):
        return self.rng.sample(list(population), k)
