# rpc/block_template.py
import time
import requests
import hashlib
from utils.logger import log

class BlockTemplateManager:
    def __init__(self, config, stats):
        self.config = config
        self.stats = stats
        self.template = None
        self.last_template_time = 0
        self.template_valid_secs = 20
        self.prev_block_hash = ""
        self._getblocktemplate_url = f"http://{config['bitcoin_rpc']['host']}:{config['bitcoin_rpc']['port']}"
        self._auth = (config['bitcoin_rpc']['user'], config['bitcoin_rpc']['password'])

    def get(self):
        if not self.template:
            self.refresh_template()
        return self.template

    def needs_refresh(self):
        if not self.template:
            return True
        if time.time() - self.last_template_time > self.template_valid_secs:
            return True
        current_prevhash = self._fetch_prevhash()
        if current_prevhash != self.prev_block_hash:
            log("[BLOCK] New Bitcoin block detected – refreshing template.")
            return True
        return False

    def refresh_template(self):
        payload = {
            "method": "getblocktemplate",
            "params": [{}],
            "id": 0
        }
        try:
            r = requests.post(self._getblocktemplate_url, auth=self._auth, json=payload)
            result = r.json()["result"]
            self.template = result
            self.prev_block_hash = result["previousblockhash"]
            self.last_template_time = time.time()
            self.stats.last_block_time = self.last_template_time
        except Exception as e:
            log(f"[ERROR] Failed to fetch block template: {e}")
            self.template = None

    def _fetch_prevhash(self):
        payload = {
            "method": "getblocktemplate",
            "params": [{}],
            "id": 1
        }
        try:
            r = requests.post(self._getblocktemplate_url, auth=self._auth, json=payload)
            result = r.json()["result"]
            return result["previousblockhash"]
        except:
            return ""
