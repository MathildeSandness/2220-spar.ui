class Item:
    def __init__(self, name, requested):
        self.name = name
        self.requested = requested
        self.available = 0
        self.up_button = None
        self.down_button = None


class ShoppingList:
    def __init__(self, worker_id, list_id, items):
        self.worker_id = worker_id
        self.list_id = list_id
        self.items = items
        self.completed = False

