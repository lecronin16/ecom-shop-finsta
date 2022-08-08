import requests
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import User, db, Shop, finsta_shop

shop = Blueprint('shop', __name__, template_folder='shop_templates')

@shop.route('/shop', methods=["GET", "POST"])
@login_required
def goToShop():
    items = Shop.query.all()
    return render_template('shop.html', items=items)

@shop.route('/cart', methods=["GET", "POST"])
def goToCart():
    user = User.query.get(current_user.id)
    cart = user.cart.all()
    new_list = []
    for c in cart:
        new_list.append(int(c.price))
    total_price = sum(new_list)
    total_items = len(cart)
    return render_template('cart.html', cart=cart,total_items=total_items, total_price=total_price)

@shop.route('/item', methods=["GET", "POST"])
def goToItem():
    user = User.query.get(current_user.id)
    cart = user.cart.all()
    return render_template('single_item.html', cart=cart)

@shop.route('/add/<string:item>')
def addToCart(item):
    items = Shop.query.filter_by(item=item).first()
    current_user.cart.append(items)
    db.session.commit()
    flash('Item added to cart.', 'success')
    return redirect(url_for('shop.goToCart'))

@shop.route('/remove/<string:item>')
def removeFromCart(item):
    purchase = Shop.query.filter_by(item=item).first()
    current_user.cart.remove(purchase)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    return redirect(url_for('shop.goToCart'))

@shop.route('/remove')
def removeAll():
    purchase = current_user.cart.all()
    for p in purchase:
        current_user.cart.remove(p)
    db.session.commit()
    return redirect(url_for('shop.goToCart'))

# @shop.route('/cost')
# def totalCost():
#     purchase = current_user.cart.all()
#     for p in purchase:
#         sum(p.price)
#     return redirect(url_for('shop.goToCart'))



