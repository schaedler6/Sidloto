from .base import BaseStrategy
class AboveFiveStrategy(BaseStrategy):
    def generate_one(self):
        high=list(range(6,26)); low=list(range(1,6))
        return self.draw_unique(high,12)+self.draw_unique(low,3)
