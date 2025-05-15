import requests

# "https://warframe.market/api_docs/items/{url_name}"
# "https://warframe.market/api_docs/items/{url_name}/orders"

item_info_start = "https://warframe.market/v1/items/" #you need to combine this with the name of the url/item
item_orders_start = "https://warframe.market/v1/items/" #you need to combine this with the name of the url/item and then add "/orders" after

class ItemInfo:
    def __init__(self, url_name, name, wiki_url, description):
        self.url_name = url_name
        self.name = name
        self.wiki_url = wiki_url
        self.description = description

class ItemOrder:
    def __init__(self, platinum, quantity, platform, ingame_name, status, region):
        self.platinum = platinum
        self.quantity = quantity
        self.platform = platform
        self.ingame_name = ingame_name
        self.status = status
        self.region = region

def getItemJsons(name):
    item_info = item_info_start + name # sets up the request url to the info api
    item_orders = item_orders_start + name + "/orders?include=item" # sets up the request url to the orders api
    info = requests.get(item_info)
    order = requests.get(item_orders)

    return (info, order)

def parseInfo(info_json) -> ItemInfo:
    data = info_json.json()

    desired_section =  data["payload"]["item"]["items_in_set"]
    entry = desired_section[0]["en"]
    urlName = desired_section[0]["url_name"]
    name = entry.get("item_name") 
    link = entry.get("wiki_link") #.get() is safer the doing entry["wiki_link"] cuz of error handling
    description = entry.get("description")
    
    item = ItemInfo(urlName, name, link, description)

    return item

def getPlatinum(order):
    return order.platinum

def parseOrders(orders_json, platform_wanted, region_wanted) -> list[ItemOrder]:
    data = orders_json.json()

    section = data["payload"]["orders"]
    orders = []
    for entry in section:
        platinum = entry.get("platinum")
        quantity = entry.get("quantity")
        platform_order = entry.get("user").get("platform")
        username = entry.get("user").get("ingame_name")
        status = entry.get("user").get("status")
        region_order = entry.get("user").get("region")

        if (platform_order == platform_wanted) and (region_order == region_wanted):
            order = ItemOrder(platinum, quantity, platform_order, username, status, region_order)
            orders.append(order)
        
    orders.sort(key=getPlatinum)
    return orders
