from collections import deque


class QueueManager:

    def __init__(self):

        self.queue = deque()
        self.visited = set()

    def add(self, url):

        if url not in self.visited:

            self.queue.append(url)
            self.visited.add(url)

    def get(self):

        if self.queue:
            return self.queue.popleft()

        return None