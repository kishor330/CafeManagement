import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime



app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cafe_secret")

from datetime import datetime


ORDERS = []

MENU = {
    "Coffee": 80,
    "Tea": 40,
    "Cold Coffee": 120,
    "Sandwich": 150,
    "Burger": 180,
    "Pizza": 250
}

# ---------------- CUSTOMER PAGE ----------------
@app.route('/')
def index():
    cart = session.get('cart', {})
    total = sum(MENU[item] * qty for item, qty in cart.items())
    return render_template('index.html', menu=MENU, order=cart, total=total)

# ---------------- MANAGER VIEW ----------------
@app.route('/manager')
def manager():
    return render_template('manager.html')

# ---------------- ADD TO CART ----------------
@app.route('/add', methods=['POST'])
def add():
    item = request.form.get('item')
    qty = int(request.form.get('qty', 1))

    cart = session.get('cart', {})

    if item in cart:
        cart[item] += qty
    else:
        cart[item] = qty

    session['cart'] = cart
    return redirect(url_for('index'))

# ---------------- CLEAR CART ----------------
@app.route('/clear')
def clear():
    session.pop('cart', None)
    return redirect(url_for('index'))

# ---------------- CHECKOUT ----------------
@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})

    if not cart:
        return redirect(url_for('index'))

    total = sum(MENU[item] * qty for item, qty in cart.items())
    order_id = random.randint(1000, 9999)

    # Save order for manager
    order = {
        "id": order_id,
        "table": "1",
        "items": cart,
        "total": total,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    ORDERS.append(order)

    # Prepare receipt data
    receipt = {
        "order_id": order_id,
        "order_list": cart,
        "total": total
    }

    session.pop('cart', None)

    return render_template('receipt.html', receipt=receipt, menu=MENU)



# ---------------- API: GET ORDERS ----------------
@app.route('/api/orders')
def get_orders():
    return jsonify(ORDERS)

# ---------------- API: COMPLETE ORDER ----------------
@app.route('/api/complete_order/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    global ORDERS
    ORDERS = [o for o in ORDERS if o['id'] != order_id]
    return jsonify({"status": "done"})

# ---------------- RUN ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)