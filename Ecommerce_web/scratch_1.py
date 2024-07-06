session = {'product_name': 'Aluminum Extrusions', 'price': 150, 'quantity': 3}

total_price = 0
cart_items = []

total_price += session['price'] * session['quantity']
cart_items.append({
    'product_name': session['product_name'],
    'price': session['price'],
    'quantity': session['quantity']
})

print(cart_items, total_price)