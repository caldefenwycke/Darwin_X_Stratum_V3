# core/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
import threading
from utils.stats_tracker import StatsTracker
from rpc.block_template import BlockTemplateManager
from header.header_generator import HeaderGenerator
from score.darwin_score import DarwinScorer
from pool.header_pool import HeaderPool
from asic.asic_interface import AsicInterface
from rpc.rpc_interface import BlockSubmitter
from utils.logger import log
from utils.webhook import send_discord

# Load config
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

stats = StatsTracker()
block_template = BlockTemplateManager(config, stats)
header_generator = HeaderGenerator(config, block_template, stats)
darwin_scorer = DarwinScorer(config)
header_pool = HeaderPool(config, stats)
asics = AsicInterface(config, stats)
submitter = BlockSubmitter(config, stats)


def update_cycle():
    while True:
        if block_template.needs_refresh():
            block_template.refresh_template()
            header_pool.clear()
            stats.reset_cycle()
            log("[TEMPLATE] Refreshed for new block")

        new_header = header_generator.generate()
        score = darwin_scorer.score(new_header)
        header_pool.add(new_header, score)
        stats.total_headers += 1
        time.sleep(0.001)


def mining_cycle():
    while True:
        top = header_pool.get_top()
        if not top:
            time.sleep(0.1)
            continue

        log(f"[DISPATCH] Top header score: {top['score']:.6f}")
        asics.send_header(top["header"])
        result = asics.wait_for_result()

        if result and result.get("block_found"):
            log("[BLOCK] Block found! Submitting...")
            submitter.submit(result)
            send_discord("BLOCK FOUND! Reward: 6.25 BTC (if valid)")
            block_template.refresh_template()
            header_pool.clear()
            stats.reset_cycle()

        header_pool.discard(top["header"])
        stats.hashed_headers += 1


def stats_cycle():
    while True:
        time.sleep(config["logging"]["update_interval"])
        stats.print_stats(header_pool)


if __name__ == "__main__":
    threading.Thread(target=update_cycle, daemon=True).start()
    threading.Thread(target=mining_cycle, daemon=True).start()
    threading.Thread(target=stats_cycle, daemon=True).start()

    while True:
        time.sleep(1)
