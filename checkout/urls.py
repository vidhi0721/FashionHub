from django.urls import path
from . import views

urlpatterns = [

    path("",views.checkout,name="checkout"),

    path("review/",views.review_order,name="review_order"),

    path("success/",views.order_success,name="order_success"),

    path("my-orders/",views.my_orders,name="my_orders"),

]