class Strategy:
    """Base class for investment strategies."""
    def execute(self):
        raise NotImplementedError

class HoldStrategy(Strategy):
    """A simple hold strategy."""
    def execute(self):
        return "Holding assets."

class RebalanceStrategy(Strategy):
    """A simple rebalance strategy."""
    def execute(self):
        return "Rebalancing portfolio." 