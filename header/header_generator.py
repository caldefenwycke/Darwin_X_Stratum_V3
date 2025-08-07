# header/header_generator.py
import time
import random
import hashlib
from header.merkle_calc import build_merkle_root

class HeaderGenerator:
    def __init__(self, config, block_template_mgr, stats):
        self.config = config
        self.block_template_mgr = block_template_mgr
        self.stats = stats
        self.extra_nonce = 0

    def generate(self):
        tpl = self.block_template_mgr.get()

        version = tpl['version']
        prevhash = tpl['previousblockhash']
        merkle = build_merkle_root(tpl, self.extra_nonce)
        ntime = int(time.time()) + random.randint(-120, 120)
        bits = tpl['bits']
        nonce = 0

        header = self.serialize_header(version, prevhash, merkle, ntime, bits, nonce)
        self.extra_nonce += 1

        return {
            'header': header,
            'merkle_root': merkle,
            'ntime': ntime,
            'bits': bits,
            'extra_nonce': self.extra_nonce
        }

    def serialize_header(self, version, prevhash, merkle_root, ntime, bits, nonce):
        def swap_endian(h): return bytes.fromhex(h)[::-1].hex()

        return (
            version.to_bytes(4, 'little').hex() +
            bytes.fromhex(swap_endian(prevhash)).hex() +
            bytes.fromhex(swap_endian(merkle_root)).hex() +
            ntime.to_bytes(4, 'little').hex() +
            bytes.fromhex(bits).hex() +
            nonce.to_bytes(4, 'little').hex()
        )
