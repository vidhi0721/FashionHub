from django.db import models


# ================= CATEGORY =================

class Category(models.Model):
    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories"
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# ================= BRAND =================

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brands/", blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


# ================= PRODUCT =================

class Product(models.Model):

    STATUS = (
        ("In Stock", "In Stock"),
        ("Out of Stock", "Out of Stock"),
    )

    GENDER_CHOICES = (
        ("Men", "Men"),
        ("Women", "Women"),
        ("Unisex", "Unisex"),
    )

    STYLE_CHOICES = (
        ("Minimal", "Minimal"),
    ("Casual", "Casual"),
    ("Korean", "Korean"),
    ("Streetwear", "Streetwear"),
    ("Elegant", "Elegant"),
    ("Trendy", "Trendy"),
    ("Formal", "Formal"),
    )
    SEASON_CHOICES = (
    ("Summer", "Summer"),
    ("Winter", "Winter"),
    ("Monsoon", "Monsoon"),
    ("Spring", "Spring"),
    ("Any","Any"),
)

    OCCASION_CHOICES = (
        ("College", "College"),
    ("Office", "Office"),
    ("Party", "Party"),
    ("Wedding", "Wedding"),
    ("Vacation", "Vacation"),
    ("Casual", "Casual"),
    ("Date", "Date"),
    )

    name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="Unisex"
    )

    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default="Western"
    )

    occasion = models.CharField(
        max_length=30,
        choices=OCCASION_CHOICES,
        default="Casual"
    )
    season = models.CharField(
    max_length=20,
    choices=SEASON_CHOICES,
    default="Summer"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to="products/")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    short_description = models.TextField(blank=True)

    rating = models.FloatField(default=0)

    discount = models.IntegerField(default=0)

    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="In Stock"
    )
    size = models.CharField(
    max_length=200,
    blank=True,
    help_text="Example: XS,S,M,L,XL"
)

    color = models.CharField(
    max_length=300,
    blank=True,
    help_text="Example: Black,Red,Blue,Pink"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sizes"
    )
    size = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"
# ================= PRODUCT GALLERY =================

class ProductGallery(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(upload_to="product_gallery/")

    def __str__(self):
        return self.product.name


# ================= PRODUCT OFFER =================

class ProductOffer(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="offers"
    )

    offer = models.CharField(max_length=255)

    def __str__(self):
        return self.offer


# ================= PRODUCT HIGHLIGHT =================

class ProductHighlight(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="highlights"
    )

    highlight = models.CharField(max_length=255)

    def __str__(self):
        return self.highlight


# ================= PRODUCT SPECIFICATION =================

class ProductSpecification(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )

    title = models.CharField(max_length=100)

    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.product.name}"
    
# ================= BANNER =================

class Banner(models.Model):

    title = models.CharField(max_length=200)

    subtitle = models.CharField(
        max_length=300,
        blank=True
    )

    image = models.ImageField(
        upload_to="banners/"
    )

    button_text = models.CharField(
        max_length=50,
        default="Shop Now"
    )

    button_link = models.CharField(
        max_length=200,
        default="/shop/"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
# ================= WATCHLIST =================

class Watchlist(models.Model):

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"