from .base import BaseStrategy
class DelayFreqStrategy(BaseStrategy):
    def generate_one(self):
        prefer=[3,4,7,8,9,12,13,17,18,19,20,21]
        base=list(dict.fromkeys([d for d in prefer if 1<=d<=25]))[:10]
        rest=[d for d in range(1,26) if d not in base]
        from random import sample
        return base + sample(rest, 15-len(base))
