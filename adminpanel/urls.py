from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # ADMIN LOGIN / LOGOUT
    # =====================================================

    path(
        "login/",
        views.admin_login,
        name="admin_login"
    ),

    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # PRODUCTS
    # =====================================================

    path(
        "products/",
        views.admin_products,
        name="admin_products"
    ),

    path(
        "products/add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "products/edit/<int:id>/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "products/delete/<int:id>/",
        views.delete_product,
        name="delete_product"
    ),


    # =====================================================
    # CATEGORIES
    # =====================================================

    path(
        "categories/",
        views.admin_categories,
        name="admin_categories"
    ),

    path(
        "categories/add/",
        views.add_category,
        name="add_category"
    ),

    path(
        "categories/edit/<int:id>/",
        views.edit_category,
        name="edit_category"
    ),

    path(
        "categories/delete/<int:id>/",
        views.delete_category,
        name="delete_category"
    ),


    # =====================================================
    # BRANDS
    # =====================================================

    path(
        "brands/",
        views.admin_brands,
        name="admin_brands"
    ),

    path(
        "brands/add/",
        views.add_brand,
        name="add_brand"
    ),

    path(
        "brands/edit/<int:id>/",
        views.edit_brand,
        name="edit_brand"
    ),

    path(
        "brands/delete/<int:id>/",
        views.delete_brand,
        name="delete_brand"
    ),


    # =====================================================
    # ORDERS
    # =====================================================

    path(
        "orders/",
        views.admin_orders,
        name="admin_orders"
    ),

    path(
        "orders/<int:id>/",
        views.order_detail,
        name="order_detail"
    ),


    # =====================================================
    # CUSTOMERS
    # =====================================================

    path(
        "customers/",
        views.admin_customers,
        name="admin_customers"
    ),

    path(
        "customers/<int:id>/",
        views.customer_detail,
        name="customer_detail"
    ),


    # =====================================================
    # BANNERS
    # =====================================================

    path(
        "banners/",
        views.admin_banners,
        name="admin_banners"
    ),

    path(
        "banners/add/",
        views.add_banner,
        name="add_banner"
    ),

    path(
        "banners/edit/<int:id>/",
        views.edit_banner,
        name="edit_banner"
    ),

    path(
        "banners/delete/<int:id>/",
        views.delete_banner,
        name="delete_banner"
    ),

]