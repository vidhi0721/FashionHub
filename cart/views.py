from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Product, ProductSize


# =========================================================
# ADD TO CART
# =========================================================

@login_required(login_url="login")
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Selected options
    size = request.POST.get("size")
    color = request.POST.get("color")

    quantity = request.POST.get(
        "quantity",
        1
    )

    # Safe quantity
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    # =====================================================
    # SIZE CHECK
    # =====================================================

    product_size = None

    if size:

        product_size = ProductSize.objects.filter(
            product=product,
            size=size
        ).first()

    # =====================================================
    # STOCK CHECK
    # =====================================================

    if product_size:

        if product_size.stock <= 0:
            return redirect(
                "product_detail",
                id=product.id
            )

        if quantity > product_size.stock:
            quantity = product_size.stock

    else:

        if product.stock <= 0:
            return redirect(
                "product_detail",
                id=product.id
            )

        if quantity > product.stock:
            quantity = product.stock

    # =====================================================
    # GET OR CREATE CART ITEM
    # =====================================================

    cart_item, created = Cart.objects.get_or_create(

        user=request.user,

        product=product,

        size=size,

        color=color,

        defaults={
            "quantity": quantity
        }
    )

    # =====================================================
    # EXISTING CART ITEM
    # =====================================================

    if not created:

        new_quantity = cart_item.quantity + quantity

        # Size-specific stock
        if product_size:

            if new_quantity > product_size.stock:
                new_quantity = product_size.stock

        else:

            if new_quantity > product.stock:
                new_quantity = product.stock

        cart_item.quantity = new_quantity

        cart_item.save()

    return redirect("cart")


# =========================================================
# CART
# =========================================================

@login_required(login_url="login")
def cart(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        # Cart model ની @property item_price
        # automatically selected size ની price લેશે
        total += item.total_price

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "cart/cart.html",
        context
    )

# =========================================================
# REMOVE FROM CART
# =========================================================

@login_required(login_url="login")
def remove_from_cart(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("cart")


# =========================================================
# INCREASE QUANTITY
# =========================================================

@login_required(login_url="login")
def increase_quantity(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    # Size-specific stock
    if item.size:

        product_size = ProductSize.objects.filter(
            product=item.product,
            size=item.size
        ).first()

        if product_size:

            if item.quantity < product_size.stock:
                item.quantity += 1
                item.save()

    else:

        if item.quantity < item.product.stock:
            item.quantity += 1
            item.save()

    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

@login_required(login_url="login")
def decrease_quantity(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.quantity > 1:

        item.quantity -= 1
        item.save()

    else:

        item.delete()

    return redirect("cart")