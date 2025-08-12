from .normal import NormalStrategy
from .above_five import AboveFiveStrategy
from .delay_freq import DelayFreqStrategy
class StrategyFactory:
    def __init__(self, seed=None): self.seed=seed
    def get(self, name:str):
        name=(name or "normal").lower()
        if name in ("normal","default"): return NormalStrategy(self.seed)
        if name in ("acima5","above5","above_five"): return AboveFiveStrategy(self.seed)
        if name in ("atraso_freq","delay_freq"): return DelayFreqStrategy(self.seed)
        return NormalStrategy(self.seed)
