# score/darwin_score.py
import hashlib

class DarwinScorer:
    def __init__(self, config):
        self.weight_entropy = config['stratum']['score_weights']['entropy']
        self.weight_hash = config['stratum']['score_weights']['hash']

    def score(self, header_obj):
        header_bytes = bytes.fromhex(header_obj['header'])
        hash_result = hashlib.sha256(hashlib.sha256(header_bytes).digest()).digest()

        # Entropy: count of 1s in binary of SHA256 hash
        entropy_score = bin(int.from_bytes(hash_result, 'big')).count('1') / 256

        # Hash score: inverse scaled (lower hash = better score)
        int_hash = int.from_bytes(hash_result, 'big')
        max_hash = 2**256
        hash_score = 1 - (int_hash / max_hash)

        # Final weighted score
        final = (self.weight_entropy * entropy_score) + (self.weight_hash * hash_score)
        return final
