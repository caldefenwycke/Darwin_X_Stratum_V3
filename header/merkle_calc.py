# header/merkle_calc.py
import hashlib

def double_sha256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def build_merkle_root(template, extra_nonce):
    coinbase_script = bytes.fromhex(template['coinbaseaux']['flags'])
    coinbase_tx = (
        bytes.fromhex(template['coinbasevalue'].to_bytes(8, 'little').hex()) +
        extra_nonce.to_bytes(4, 'little') +
        coinbase_script
    )
    coinbase_hash = double_sha256(coinbase_tx)

    merkle_branch = [bytes.fromhex(h) for h in template['merkle_branch']]
    merkle_root = coinbase_hash
    for h in merkle_branch:
        merkle_root = double_sha256(merkle_root + h)

    return merkle_root[::-1].hex()  # Bitcoin expects it in little-endian
