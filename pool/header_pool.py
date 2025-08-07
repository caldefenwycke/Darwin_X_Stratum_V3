# pool/header_pool.py
import heapq

class HeaderPool:
    def __init__(self, config, stats):
        self.max_size = config['stratum']['header_pool_size']
        self.pool = []  # min-heap based on Darwin score
        self.header_set = set()
        self.stats = stats

    def add(self, header_data, score):
        header_hex = header_data['header']
        if header_hex in self.header_set:
            return

        if len(self.pool) < self.max_size:
            heapq.heappush(self.pool, (score, header_data))
            self.header_set.add(header_hex)
        else:
            if score > self.pool[0][0]:
                removed = heapq.heappushpop(self.pool, (score, header_data))
                self.header_set.remove(removed[1]['header'])
                self.header_set.add(header_hex)
                self.stats.discarded_headers += 1
            else:
                self.stats.discarded_headers += 1

    def get_top(self):
        if not self.pool:
            return None
        return max(self.pool, key=lambda x: x[0])[1]

    def discard(self, header_hex):
        self.pool = [(s, h) for s, h in self.pool if h['header'] != header_hex]
        heapq.heapify(self.pool)
        self.header_set.discard(header_hex)

    def clear(self):
        self.pool.clear()
        self.header_set.clear()

    def size(self):
        return len(self.pool)
