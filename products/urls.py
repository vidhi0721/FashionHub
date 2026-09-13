from django.urls import path
from . import views

urlpatterns = [

    path("", views.shop, name="shop"),

    path(
        "<int:id>/",
        views.product_details,
        name="product_details"
    ),

    path(
        "watchlist/",
        views.watchlist,
        name="watchlist"
    ),

    path(
        "watchlist/add/<int:id>/",
        views.add_to_watchlist,
        name="add_to_watchlist"
    ),
    path(
        "watchlist/remove/<int:id>/",
        views.remove_from_watchlist,
        name="remove_from_watchlist"
    ),
]