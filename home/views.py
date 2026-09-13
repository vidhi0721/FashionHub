from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product, Category, Banner


# =========================================================
# HOME
# =========================================================

def home(request):

    # -----------------------------------------------------
    # Categories
    # -----------------------------------------------------

    categories = Category.objects.all()

    # -----------------------------------------------------
    # All products
    # Stock > 0 રાખ્યું છે
    # -----------------------------------------------------

    products = (
        Product.objects
        .filter(stock__gt=0)
        .select_related("category")
        .order_by("-id")
    )

    featured_products = []

    # =====================================================
    # Helper Function
    # =====================================================

    def get_product(category_words):

        for product in products:

            if not product.category:
                continue

            category_name = product.category.name.lower().strip()

            for word in category_words:

                if word in category_name:

                    if product not in featured_products:
                        return product

        return None

    # =====================================================
    # WOMEN PRODUCTS
    # =====================================================

    women_categories = [
        ["saree", "sarees"],
        ["top", "tops"],
        ["bag", "bags", "handbag", "hand bag"],
        ["makeup", "make up", "cosmetic", "cosmetics"],
    ]

    # =====================================================
    # MEN PRODUCTS
    # =====================================================

    men_categories = [
        ["shirt", "shirts"],
        ["watch", "watches"],
        ["belt", "belts"],
        ["t-shirt", "tshirts", "t shirt", "t-shirts"],
    ]

    # =====================================================
    # Add Women Products
    # =====================================================

    for category_words in women_categories:

        product = get_product(category_words)

        if product:
            featured_products.append(product)

    # =====================================================
    # Add Men Products
    # =====================================================

    for category_words in men_categories:

        product = get_product(category_words)

        if product:
            featured_products.append(product)

    # =====================================================
    # BANNERS
    # =====================================================

    banners = Banner.objects.filter(is_active=True)

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "categories": categories,
        "featured_products": featured_products,
        "banners": banners,
    }

    return render(
        request,
        "home/index.html",
        context
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@login_required
def edit_profile(request):

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # -------------------------------------------------
        # Password Change
        # -------------------------------------------------

        if new_password or confirm_password:

            if new_password != confirm_password:

                messages.error(
                    request,
                    "Passwords do not match!"
                )

                return redirect("edit_profile")

            user.set_password(new_password)

        user.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "edit_profile.html"
    )