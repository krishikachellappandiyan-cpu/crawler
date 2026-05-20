class Store:

    def __init__(self):

        self.endpoints = []

    def add_endpoint(self, endpoint):

        if endpoint not in self.endpoints:
            self.endpoints.append(endpoint)