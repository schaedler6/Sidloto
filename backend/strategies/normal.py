from .base import BaseStrategy
class NormalStrategy(BaseStrategy):
    def generate_one(self): return self.draw_unique()
