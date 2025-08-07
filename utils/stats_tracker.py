# utils/stats_tracker.py
import time
import math
from utils.logger import log

class StatsTracker:
    def __init__(self):
        self.reset_cycle()
        self.last_block_time = time.time()
        self.submissions = 0
        self.blocks_found = 0

    def reset_cycle(self):
        self.total_headers = 0
        self.hashed_headers = 0
        self.discarded_headers = 0

    def print_stats(self, header_pool):
        elapsed = time.time() - self.last_block_time
        top_header_score = header_pool.get_top()["score"] if header_pool.get_top() else 1.0
        pct_to_btc_diff = top_header_score * 100

        bar_len = int(min(40, (1.0 - top_header_score) * 1000))
        bar = "[" + "#" * bar_len + "-" * (40 - bar_len) + "]"

        print("\n===== Darwin X Pool Stats =====")
        print(f"Current Header Pool Size : {header_pool.size()}")
        print(f"Total Headers Generated  : {self.total_headers}")
        print(f"Headers Hashed this Cycle: {self.hashed_headers}")
        print(f"Headers Discarded        : {self.discarded_headers}")
        print(f"Top Header Score         : 10^{math.floor(math.log10(top_header_score))} away")
        print(f"% to BTC Difficulty      : {bar} {pct_to_btc_diff:.5f}%")
        print(f"Submissions              : {self.submissions}")
        print(f"Blocks Found             : {self.blocks_found}")
        print(f"Time Since Last BTC Block: {int(elapsed)}s")
        print("================================\n")
