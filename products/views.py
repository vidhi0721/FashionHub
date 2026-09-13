from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import (
    Product,
    Category,
    Watchlist,
    ProductOffer,
    ProductHighlight,
)


# =========================================================
# SHOP
# =========================================================

def shop(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    # ================= SEARCH =================

    search = request.GET.get("search", "").strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    # ================= CATEGORY =================

    category = request.GET.get("category", "").strip()

    if category:

        try:

            category_id = int(category)

            selected_cat = Category.objects.get(
                id=category_id
            )

            # Parent category selected
            if selected_cat.parent is None:

                subcategory_ids = Category.objects.filter(
                    parent=selected_cat
                ).values_list(
                    "id",
                    flat=True
                )

                products = products.filter(
                    category_id__in=list(subcategory_ids) + [
                        selected_cat.id
                    ]
                )

            # Subcategory selected
            else:

                products = products.filter(
                    category_id=selected_cat.id
                )

        except (ValueError, Category.DoesNotExist):

            # Old category name links
            products = products.filter(
                category__name__iexact=category
            )

    # ================= PRICE =================

    price = request.GET.get("price", "").strip()

    if price:

        try:

            products = products.filter(
                price__lte=float(price)
            )

        except ValueError:

            pass

    # ================= RATING =================

    rating = request.GET.get("rating", "").strip()

    if rating:

        try:

            products = products.filter(
                rating__gte=float(rating)
            )

        except ValueError:

            pass

    # ================= DISCOUNT =================

    discount = request.GET.get("discount", "").strip()

    if discount:

        try:

            products = products.filter(
                discount__gte=int(discount)
            )

        except ValueError:

            pass

    # ================= SORT =================

    sort = request.GET.get(
        "sort",
        "newest"
    )

    if sort == "newest":

        products = products.order_by(
            "-id"
        )

    elif sort == "price_low":

        products = products.order_by(
            "price"
        )

    elif sort == "price_high":

        products = products.order_by(
            "-price"
        )

    elif sort == "rating":

        products = products.order_by(
            "-rating"
        )

    elif sort == "az":

        products = products.order_by(
            "name"
        )

    elif sort == "za":

        products = products.order_by(
            "-name"
        )

    else:

        products = products.order_by(
            "-id"
        )

    # =========================================================
    # PAGINATION
    # 12 PRODUCTS PER PAGE
    # =========================================================

    paginator = Paginator(
        products,
        12
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ================= CONTEXT =================

    context = {

        "products": page_obj,

        "page_obj": page_obj,

        "paginator": paginator,

        "categories": categories,

        "selected_category": category,

        "selected_price": price,

        "selected_rating": rating,

        "selected_discount": discount,

        "selected_sort": sort,

        "search": search,

    }

    return render(
        request,
        "shop.html",
        context
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_details(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )
# ================= WATCHLIST CHECK =================

    is_in_watchlist = False

    if request.user.is_authenticated:

            is_in_watchlist = Watchlist.objects.filter(
                user=request.user,
                product=product
            ).exists()

    # ================= RELATED PRODUCTS =================

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    # ================= SIZES =================

    sizes = []

    if product.size:

        sizes = [
            size.strip()
            for size in product.size.split(",")
            if size.strip()
        ]

    # ================= COLORS =================

    colors = []

    if product.color:

        colors = [
            color.strip()
            for color in product.color.split(",")
            if color.strip()
        ]

    # ================= OFFERS =================

    offers = ProductOffer.objects.filter(
        product=product
    )

    # ================= HIGHLIGHTS =================

    highlights = ProductHighlight.objects.filter(
        product=product
    )

    # ================= CONTEXT =================

    context = {

        "product": product,

        "related_products": related_products,

        "sizes": sizes,

        "colors": colors,

        "offers": offers,

        "highlights": highlights,

    }

    return render(
        request,
        "products/product_details.html",
        context
    )


# =========================================================
# ADD TO WATCHLIST
# =========================================================

@login_required
def add_to_watchlist(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    watchlist_item, created = Watchlist.objects.get_or_create(

        user=request.user,

        product=product

    )

    if created:

        messages.success(
            request,
            f"{product.name} added to your watchlist ❤️"
        )

    else:

        messages.info(
            request,
            f"{product.name} is already in your watchlist ❤️"
        )

    return redirect(
        "product_details",
        id=id
    )


# =========================================================
# WATCHLIST
# =========================================================

@login_required
def watchlist(request):

    items = Watchlist.objects.filter(
        user=request.user
    ).select_related(
        "product"
    )

    return render(
        request,
        "products/watchlist.html",
        {
            "watchlist_items": items
        }
    )

@login_required
def remove_from_watchlist(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    Watchlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect("shop")