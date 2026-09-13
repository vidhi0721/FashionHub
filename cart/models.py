from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductSize


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    size = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    # =====================================================
    # SELECTED SIZE PRICE
    # =====================================================

    @property
    def item_price(self):

        # જો size select કરેલી હોય
        if self.size:

            size_obj = ProductSize.objects.filter(
                product=self.product,
                size=self.size
            ).first()

            if size_obj:
                return size_obj.price

        # જો size ના હોય તો Product ની default price
        return self.product.price

    # =====================================================
    # TOTAL PRICE
    # =====================================================

    @property
    def total_price(self):

        return self.item_price * self.quantity