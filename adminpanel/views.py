from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from products.models import (Product, Category,Brand,Banner,ProductOffer,ProductHighlight,ProductSpecification,ProductSize,)

from cart.models import Cart
from checkout.models import Order, OrderItem


# =========================================================
# ADMIN ACCESS PROTECTION
# =========================================================
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
def staff_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        admin_id = request.session.get("admin_user_id")

        if not admin_id:
            return redirect("admin_login")

        user = User.objects.filter(
            id=admin_id,
            is_staff=True
        ).first()

        if not user:

            request.session.pop(
                "admin_user_id",
                None
            )

            return redirect("admin_login")

        request.admin_user = user
        request.user = user

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.session.get("admin_user_id"):

        admin_id = request.session.get(
            "admin_user_id"
        )

        admin_user = User.objects.filter(
            id=admin_id,
            is_staff=True
        ).first()

        if admin_user:
            return redirect("dashboard")

        request.session.pop(
            "admin_user_id",
            None
        )

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            request.session[
                "admin_user_id"
            ] = user.id

            messages.success(
                request,
                "Admin Login Successful!"
            )

            return redirect(
                "dashboard"
            )

        messages.error(
            request,
            "Invalid Username or Password"
        )

    return render(
        request,
        "adminpanel/login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

def admin_logout(request):

    request.session.pop(
        "admin_user_id",
        None
    )

    messages.success(
        request,
        "Admin Logged Out Successfully!"
    )

    return redirect(
        "admin_login"
    )


# =========================================================
# DASHBOARD
# =========================================================

@staff_required
def dashboard(request):

    context = {

        "total_products":
            Product.objects.count(),

        "total_categories":
            Category.objects.count(),

        "total_customers":
            User.objects.filter(
                is_staff=False
            ).count(),

        "total_cart":
            Cart.objects.count(),

        "total_orders":
            Order.objects.count(),
    }

    return render(
        request,
        "adminpanel/index.html",
        context
    )


# =========================================================
# PRODUCTS
# =========================================================

@staff_required
def admin_products(request):

    products = Product.objects.all().order_by(
        "-id"
    )

    return render(
        request,
        "adminpanel/products.html",
        {
            "products": products
        }
    )


# =========================================================
# ADD PRODUCT
# =========================================================

@staff_required
def add_product(request):

    categories = Category.objects.all()

    if request.method == "POST":

        # =========================
        # PRODUCT DATA
        # =========================

        name = request.POST.get(
            "name"
        )

        category = request.POST.get(
            "category"
        )

        # =========================
        # BRAND NAME
        # =========================

        brand_name = request.POST.get(
            "brand",
            ""
        ).strip()

        brand = None

        if brand_name:

            brand = Brand.objects.filter(
                name__iexact=brand_name
            ).first()

            if not brand:

                brand = Brand.objects.create(
                    name=brand_name
                )

        # =========================
        # PRICE
        # =========================
        # Default Product.price
        # first size price thi update thase
        # =========================

        price = request.POST.get(
            "price"
        ) or 0

        discount = request.POST.get(
            "discount"
        ) or 0

        rating = request.POST.get(
            "rating"
        ) or 0

        # =========================
        # SAFE STOCK
        # =========================

        stock_value = request.POST.get(
            "stock"
        )

        try:

            stock = (
                int(stock_value)
                if stock_value
                else 1
            )

        except (
            ValueError,
            TypeError
        ):

            stock = 1

        if stock < 0:
            stock = 0

        # =========================
        # OTHER DATA
        # =========================

        size = request.POST.get(
            "size",
            ""
        )

        color = request.POST.get(
            "color",
            ""
        )

        status = request.POST.get(
            "status",
            "In Stock"
        )

        short_description = request.POST.get(
            "short_description",
            ""
        )

        description = request.POST.get(
            "description",
            ""
        )

        image = request.FILES.get(
            "image"
        )

        # =========================
        # CREATE PRODUCT
        # =========================

        product = Product.objects.create(

            name=name,

            category_id=category,

            brand=brand,

            price=price,

            discount=discount,

            rating=rating,

            stock=stock,

            size=size,

            color=color,

            status=status,

            short_description=short_description,

            description=description,

            image=image,
        )

        # =====================================================
        # PRODUCT SIZES
        # =====================================================

        size_names = request.POST.getlist(
            "size_name"
        )

        size_prices = request.POST.getlist(
            "size_price"
        )

        size_stocks = request.POST.getlist(
            "size_stock"
        )

        first_size_price = None

        for size_name, size_price, size_stock in zip(
            size_names,
            size_prices,
            size_stocks
        ):

            size_name = size_name.strip()

            if not size_name:
                continue

            # SAFE PRICE
            try:

                size_price = (
                    float(size_price)
                    if size_price
                    else 0
                )

            except (
                ValueError,
                TypeError
            ):

                size_price = 0

            # SAFE STOCK
            try:

                size_stock = (
                    int(size_stock)
                    if size_stock
                    else 0
                )

            except (
                ValueError,
                TypeError
            ):

                size_stock = 0

            if size_stock < 0:
                size_stock = 0

            ProductSize.objects.create(

                product=product,

                size=size_name,

                price=size_price,

                stock=size_stock
            )

            # First size price
            if first_size_price is None:
                first_size_price = size_price

        # =====================================================
        # SET PRODUCT PRICE FROM FIRST SIZE
        # =====================================================

        if first_size_price is not None:

            product.price = first_size_price
            product.save(
                update_fields=["price"]
            )

        # =========================
        # HIGHLIGHTS
        # =========================

        highlights = request.POST.getlist(
            "highlights"
        )

        for highlight in highlights:

            highlight = highlight.strip()

            if highlight:

                ProductHighlight.objects.create(
                    product=product,
                    highlight=highlight
                )

        # =========================
        # OFFERS
        # =========================

        offers = request.POST.getlist(
            "offers"
        )

        for offer in offers:

            offer = offer.strip()

            if offer:

                ProductOffer.objects.create(
                    product=product,
                    offer=offer
                )

        # =========================
        # SUCCESS
        # =========================

        messages.success(
            request,
            "Product Added Successfully"
        )

        return redirect(
            "admin_products"
        )

    # =========================
    # GET
    # =========================

    return render(
        request,
        "adminpanel/add_product.html",
        {
            "categories": categories,
        }
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@staff_required
def edit_product(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    categories = Category.objects.all()

    if request.method == "POST":

        # =====================================================
        # PRODUCT DATA
        # =====================================================

        product.name = request.POST.get(
            "name"
        )

        product.category_id = request.POST.get(
            "category"
        )

        # =====================================================
        # BRAND NAME
        # =====================================================

        brand_name = request.POST.get(
            "brand",
            ""
        ).strip()

        brand = None

        if brand_name:

            brand = Brand.objects.filter(
                name__iexact=brand_name
            ).first()

            if not brand:

                brand = Brand.objects.create(
                    name=brand_name
                )

        product.brand = brand

        # =====================================================
        # DISCOUNT
        # =====================================================

        product.discount = request.POST.get(
            "discount"
        ) or 0

        # =====================================================
        # RATING
        # =====================================================

        product.rating = request.POST.get(
            "rating"
        ) or 0

        # =====================================================
        # SAFE STOCK
        # =====================================================

        stock_value = request.POST.get(
            "stock",
            ""
        ).strip()

        try:

            stock = (
                int(stock_value)
                if stock_value
                else product.stock
            )

        except (
            ValueError,
            TypeError
        ):

            stock = product.stock

        if stock < 0:
            stock = 0

        product.stock = stock

        # =====================================================
        # OTHER DATA
        # =====================================================

        product.size = request.POST.get(
            "size",
            ""
        )

        product.color = request.POST.get(
            "color",
            ""
        )

        product.status = request.POST.get(
            "status",
            "In Stock"
        )

        product.short_description = request.POST.get(
            "short_description",
            ""
        )

        product.description = request.POST.get(
            "description",
            ""
        )

        # =====================================================
        # IMAGE
        # =====================================================

        if request.FILES.get("image"):

            product.image = request.FILES.get(
                "image"
            )

        # =====================================================
        # PRODUCT SIZES
        # =====================================================

        # Old sizes delete
        ProductSize.objects.filter(
            product=product
        ).delete()

        size_names = request.POST.getlist(
            "size_name"
        )

        size_prices = request.POST.getlist(
            "size_price"
        )

        size_stocks = request.POST.getlist(
            "size_stock"
        )

        first_size_price = None

        # =====================================================
        # CREATE NEW SIZES
        # =====================================================

        for size_name, size_price, size_stock in zip(
            size_names,
            size_prices,
            size_stocks
        ):

            size_name = size_name.strip()

            if not size_name:
                continue

            # -------------------------
            # SAFE PRICE
            # -------------------------

            try:

                size_price = (
                    float(size_price)
                    if size_price
                    else 0
                )

            except (
                ValueError,
                TypeError
            ):

                size_price = 0

            # -------------------------
            # SAFE STOCK
            # -------------------------

            try:

                size_stock = (
                    int(size_stock)
                    if size_stock
                    else 0
                )

            except (
                ValueError,
                TypeError
            ):

                size_stock = 0

            if size_stock < 0:
                size_stock = 0

            # -------------------------
            # CREATE SIZE
            # -------------------------

            ProductSize.objects.create(

                product=product,

                size=size_name,

                price=size_price,

                stock=size_stock
            )

            # -------------------------
            # FIRST SIZE PRICE
            # -------------------------

            if first_size_price is None:

                first_size_price = size_price

        # =====================================================
        # PRODUCT PRICE
        # =====================================================

        # IMPORTANT:
        # Separate Product Price field nathi.
        # First size ni price Product.price ma save thase.

        if first_size_price is not None:

            product.price = first_size_price

        # Existing price retain
        # if no size entered

        elif product.price is None:

            product.price = 0

        # =====================================================
        # SAVE PRODUCT
        # =====================================================

        product.save()

        # =====================================================
        # OFFERS
        # =====================================================

        ProductOffer.objects.filter(
            product=product
        ).delete()

        offers = request.POST.getlist(
            "offers"
        )

        for offer in offers:

            offer = offer.strip()

            if offer:

                ProductOffer.objects.create(
                    product=product,
                    offer=offer
                )

        # =====================================================
        # HIGHLIGHTS
        # =====================================================

        ProductHighlight.objects.filter(
            product=product
        ).delete()

        highlights = request.POST.getlist(
            "highlights"
        )

        for highlight in highlights:

            highlight = highlight.strip()

            if highlight:

                ProductHighlight.objects.create(
                    product=product,
                    highlight=highlight
                )

        # =====================================================
        # SUCCESS
        # =====================================================

        messages.success(
            request,
            "Product Updated Successfully"
        )

        return redirect(
            "admin_products"
        )

    # =========================================================
    # GET
    # =========================================================

    return render(
        request,
        "adminpanel/edit_product.html",
        {
            "product": product,
            "categories": categories,
        }
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

@staff_required
def delete_product(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    product.delete()

    messages.success(
        request,
        "Product Deleted Successfully"
    )

    return redirect(
        "admin_products"
    )


# =========================================================
# CATEGORIES
# =========================================================

@staff_required
def admin_categories(request):

    categories = Category.objects.all().order_by(
        "-id"
    )

    return render(
        request,
        "adminpanel/categories.html",
        {
            "categories": categories
        }
    )


# =========================================================
# ADD CATEGORY
# =========================================================

@staff_required
def add_category(request):

    categories = Category.objects.filter(
        parent__isnull=True
    )

    if request.method == "POST":

        parent_id = request.POST.get(
            "parent"
        )

        Category.objects.create(

            name=request.POST.get(
                "name"
            ),

            image=request.FILES.get(
                "image"
            ),

            parent_id=(
                parent_id
                if parent_id
                else None
            ),
        )

        messages.success(
            request,
            "Category Added Successfully"
        )

        return redirect(
            "admin_categories"
        )

    return render(
        request,
        "adminpanel/add_category.html",
        {
            "categories": categories
        }
    )


# =========================================================
# EDIT CATEGORY
# =========================================================

@staff_required
def edit_category(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    categories = Category.objects.filter(
        parent__isnull=True
    ).exclude(
        id=category.id
    )

    if request.method == "POST":

        category.name = request.POST.get(
            "name"
        )

        parent_id = request.POST.get(
            "parent"
        )

        if parent_id:

            category.parent_id = parent_id

        else:

            category.parent = None

        if request.FILES.get(
            "image"
        ):

            category.image = request.FILES.get(
                "image"
            )

        category.save()

        messages.success(
            request,
            "Category Updated Successfully"
        )

        return redirect(
            "admin_categories"
        )

    return render(
        request,
        "adminpanel/edit_category.html",
        {
            "category": category,
            "categories": categories,
        }
    )


# =========================================================
# DELETE CATEGORY
# =========================================================

@staff_required
def delete_category(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    category.delete()

    messages.success(
        request,
        "Category Deleted Successfully"
    )

    return redirect(
        "admin_categories"
    )


# =========================================================
# BRANDS
# =========================================================

@staff_required
def admin_brands(request):

    brands = Brand.objects.all()

    return render(
        request,
        "adminpanel/brands.html",
        {
            "brands": brands
        }
    )


# =========================================================
# ADD BRAND
# =========================================================

@staff_required
def add_brand(request):

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        image = request.FILES.get(
            "image"
        )

        Brand.objects.create(

            name=name,

            image=image
        )

        messages.success(
            request,
            "Brand Added Successfully"
        )

        return redirect(
            "admin_brands"
        )

    return render(
        request,
        "adminpanel/add_brand.html"
    )


# =========================================================
# EDIT BRAND
# =========================================================

@staff_required
def edit_brand(request, id):

    brand = get_object_or_404(
        Brand,
        id=id
    )

    if request.method == "POST":

        brand.name = request.POST.get(
            "name"
        )

        if request.FILES.get(
            "image"
        ):

            brand.image = request.FILES.get(
                "image"
            )

        brand.save()

        messages.success(
            request,
            "Brand Updated Successfully"
        )

        return redirect(
            "admin_brands"
        )

    return render(
        request,
        "adminpanel/edit_brand.html",
        {
            "brand": brand
        }
    )


# =========================================================
# DELETE BRAND
# =========================================================

@staff_required
def delete_brand(request, id):

    brand = get_object_or_404(
        Brand,
        id=id
    )

    brand.delete()

    messages.success(
        request,
        "Brand Deleted Successfully"
    )

    return redirect(
        "admin_brands"
    )


# =========================================================
# ORDERS
# =========================================================

@staff_required
def admin_orders(request):

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "adminpanel/orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# ORDER DETAIL
# =========================================================

@staff_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    items = OrderItem.objects.filter(
        order=order
    )

    return render(
        request,
        "adminpanel/order_detail.html",
        {
            "order": order,
            "items": items
        }
    )


# =========================================================
# CUSTOMERS
# =========================================================

@staff_required
def admin_customers(request):

    customers = User.objects.filter(
        is_staff=False
    ).order_by(
        "-id"
    )

    return render(
        request,
        "adminpanel/customers.html",
        {
            "customers": customers
        }
    )


# =========================================================
# CUSTOMER DETAIL
# =========================================================

@staff_required
def customer_detail(request, id):

    customer = get_object_or_404(
        User,
        id=id,
        is_staff=False
    )

    orders = Order.objects.filter(
        user=customer
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "adminpanel/customer_detail.html",
        {
            "customer": customer,
            "orders": orders
        }
    )


# =========================================================
# BANNERS
# =========================================================

@staff_required
def admin_banners(request):

    banners = Banner.objects.all()

    return render(
        request,
        "adminpanel/banners.html",
        {
            "banners": banners
        }
    )


# =========================================================
# ADD BANNER
# =========================================================

@staff_required
def add_banner(request):

    if request.method == "POST":

        Banner.objects.create(

            title=request.POST.get(
                "title"
            ),

            subtitle=request.POST.get(
                "subtitle"
            ),

            image=request.FILES.get(
                "image"
            ),

            button_text=request.POST.get(
                "button_text"
            ),

            button_link=request.POST.get(
                "button_link"
            ),

            is_active=(
                True
                if request.POST.get(
                    "is_active"
                )
                else False
            ),
        )

        messages.success(
            request,
            "Banner Added Successfully"
        )

        return redirect(
            "admin_banners"
        )

    return render(
        request,
        "adminpanel/add_banner.html"
    )


# =========================================================
# EDIT BANNER
# =========================================================

@staff_required
def edit_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )

    if request.method == "POST":

        banner.title = request.POST.get(
            "title"
        )

        banner.subtitle = request.POST.get(
            "subtitle"
        )

        banner.button_text = request.POST.get(
            "button_text"
        )

        banner.button_link = request.POST.get(
            "button_link"
        )

        banner.is_active = (
            True
            if request.POST.get(
                "is_active"
            )
            else False
        )

        if request.FILES.get(
            "image"
        ):

            banner.image = request.FILES.get(
                "image"
            )

        banner.save()

        messages.success(
            request,
            "Banner Updated Successfully"
        )

        return redirect(
            "admin_banners"
        )

    return render(
        request,
        "adminpanel/edit_banner.html",
        {
            "banner": banner
        }
    )


# =========================================================
# DELETE BANNER
# =========================================================

@staff_required
def delete_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )

    banner.delete()

    messages.success(
        request,
        "Banner Deleted Successfully"
    )

    return redirect(
        "admin_banners"
    )