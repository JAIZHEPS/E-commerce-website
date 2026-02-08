from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open(os.path.join(os.path.dirname(__file__), 'products.json')) as f:
    PRODUCTS = json.load(f)

def get_product(pid):
    for p in PRODUCTS:
        if p['id'] == pid:
            return p
    return None

@app.route('/')
def home():
    featured = PRODUCTS[:3]
    return render_template('home.html', products=featured)

@app.route('/products')
def products():
    return render_template('products.html', products=PRODUCTS)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    cart_items = []
    total = 0
    for item in cart:
        product = get_product(item['id'])
        if product:
            subtotal = product['price'] * item['qty']
            total += subtotal
            cart_items.append({'product': product, 'qty': item['qty'], 'subtotal': subtotal})
    recommended = [p for p in PRODUCTS if p['id'] not in [i['id'] for i in cart]][:2]
    return render_template('cart.html', cart=cart_items, total=total, recommended=recommended)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pid = int(request.form['product_id'])
    qty = int(request.form.get('qty', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == pid:
            item['qty'] += qty
            break
    else:
        cart.append({'id': pid, 'qty': qty})
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    pid = int(request.form['product_id'])
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != pid]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    pid = int(request.form['product_id'])
    qty = int(request.form['qty'])
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == pid:
            item['qty'] = qty
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/bill', methods=['GET', 'POST'])
def bill():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        cart = session.get('cart', [])
        cart_items = []
        total = 0
        for item in cart:
            product = get_product(item['id'])
            if product:
                subtotal = product['price'] * item['qty']
                total += subtotal
                cart_items.append({'product': product, 'qty': item['qty'], 'subtotal': subtotal})
        return render_template('bill.html', cart=cart_items, total=total, name=name, phone=phone, address=address)
    else:
        return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')