from .correlation_stats_analyzer import correlation_r, interpret_r

class CorrelationAnalyzer:
    def __init__(self):
        self.correlation_r = correlation_r
        self.interpret_r = interpret_r

import sys
sys.modules[__name__] = CorrelationAnalyzer()