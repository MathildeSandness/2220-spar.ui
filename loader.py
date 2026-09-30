import json
from models import Item, ShoppingList

WORKER_ID = "WORKER-001"  # fast verdi eller hent fra egen fil senere

def load_all_lists(path="lists.json"):
    with open(path, "r") as f:
        raw = json.load(f)

    lists = []
    for entry in raw:
        items = [Item(i["name"], i["requested"]) for i in entry["items"]]
        lists.append(
            ShoppingList(
                worker_id=WORKER_ID,
                list_id=entry["list_id"],
                items=items
            )
        )
    return lists


