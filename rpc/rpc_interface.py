# rpc/rpc_interface.py
import requests
import json
from utils.logger import log

class BlockSubmitter:
    def __init__(self, config, stats):
        self.rpc_host = config['bitcoin_rpc']['host']
        self.rpc_port = config['bitcoin_rpc']['port']
        self.rpc_user = config['bitcoin_rpc']['user']
        self.rpc_password = config['bitcoin_rpc']['password']
        self.wallet = config['bitcoin_rpc'].get('wallet', None)
        self.url = f"http://{self.rpc_host}:{self.rpc_port}"
        self.auth = (self.rpc_user, self.rpc_password)
        self.stats = stats

    def submit(self, result):
        # Submit full block here if ASIC returned one
        full_block_hex = result.get("block_hex")
        if not full_block_hex:
            log("[SUBMIT] No block hex received from ASIC")
            return

        payload = {
            "method": "submitblock",
            "params": [full_block_hex],
            "id": 1
        }

        try:
            r = requests.post(self.url, auth=self.auth, json=payload)
            res = r.json()
            if res.get("error"):
                log(f"[SUBMIT] Block rejected: {res['error']}")
            else:
                log("[SUBMIT] Block submitted successfully!")
                self.stats.blocks_found += 1
        except Exception as e:
            log(f"[SUBMIT] Exception during block submission: {e}")
