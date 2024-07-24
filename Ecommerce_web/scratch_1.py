order_items = {'Items': [{'price': 150, 'product_id': 2, 'product_name': 'Aluminum Extrusions', 'quantity': 1}, {'price': 450, 'product_id': 3, 'product_name': 'Tempered Glass Panels', 'quantity': 1}, {'price': 250, 'product_id': 4, 'product_name': 'Laminated Glass', 'quantity': 1}], 'Total': 850}

for items in order_items["Items"]:
    id = items['product_id']

print(order_items)