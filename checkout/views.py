from .models import Order, OrderItem
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "checkout/checkout.html", context)



@login_required
def review_order(request):

    if request.method == "POST":

        cart_items = Cart.objects.filter(user=request.user)

        total = sum(item.total_price for item in cart_items)

        # Empty cart check
        if not cart_items.exists():
            return redirect("cart")

        # Create Order
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
            payment_method=request.POST.get("payment"),
            total=total,
        )

        # Create Order Items
        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Save Order ID
        request.session["order_id"] = order.id

        # IMPORTANT: Delete Cart Items
        cart_items.delete()

        return render(
            request,
            "checkout/review_order.html",
            {
                "order": order,
                "cart_items": OrderItem.objects.filter(order=order),
                "total": total,
            }
        )

    return redirect("checkout")

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "checkout/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def order_success(request):

    return render(
        request,
        "checkout/success.html"
    )