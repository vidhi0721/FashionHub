from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from products.models import Product, Category

import random
import re
from .ai_config import (
    AI_CATEGORIES,
    CATEGORY_ALIASES,
    SUBCATEGORY_ALIASES,
    COLOR_ALIASES,
    DATABASE_CATEGORY_ALIASES,
    OCCASION_ALIASES,
    COMPLETE_OUTFIT_KEYWORDS,
    WOMEN_COLLAGE_OUTFIT,
    OCCASION_OUTFIT_CATEGORIES,
    COMPLETE_OUTFIT_CATEGORIES,
    MATCHING_PRODUCTS,
)




# =========================================================
# DETECT OCCASION
# =========================================================

def detect_occasion(text):

    if not text:
        return None

    text = text.strip().lower()

    for occasion, keywords in OCCASION_ALIASES.items():

        for keyword in keywords:

            if keyword in text:
                return occasion

    return None


# =========================================================
# DETECT COLLAGE
# =========================================================

def detect_collage(text):

    if not text:
        return False

    text = text.strip().lower()

    collage_words = [
        "collage",
        "collage outfit",
        "collage look",
    ]

    return any(
        word in text
        for word in collage_words
    )


# =========================================================
# DETECT COMPLETE OUTFIT
# =========================================================

def detect_complete_outfit(text):

    if not text:
        return False

    text = text.strip().lower()

    for keyword in COMPLETE_OUTFIT_KEYWORDS:

        if keyword in text:
            return True

    if (
        detect_occasion(text)
        and (
            "outfit" in text
            or "look" in text
        )
    ):
        return True

    if detect_collage(text):
        return True

    if (
        "outfit" in text
        or "outfite" in text
        or "look" in text
    ):
        return True

    return False


# =========================================================
# DETECT MAIN CATEGORY
# =========================================================

def detect_main_category(text):

    if not text:
        return None

    text = text.strip().lower()

    if text in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[text]

    aliases = sorted(
        CATEGORY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, value in aliases:

        if re.search(
            r"\b" + re.escape(key) + r"\b",
            text
        ):
            return value

    return None


# =========================================================
# DETECT SUBCATEGORY
# =========================================================

def detect_subcategory(text):

    if not text:
        return None

    text = text.strip().lower()

    # =====================================================
    # MEN JEANS
    # =====================================================

    men_jeans_patterns = [

        "men's jeans",
        "mens jeans",
        "men jeans",

        "men's jean",
        "mens jean",
        "men jean",

        "jeans men",
        "jeans mens",
        "jeans men's",

        "jean men",
        "jean mens",
    ]

    for pattern in men_jeans_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Men Jeans"

    # =====================================================
    # MEN T-SHIRT
    # =====================================================

    men_tshirt_patterns = [

        "men's t-shirts",
        "mens t-shirts",
        "men t-shirts",

        "men's t-shirt",
        "mens t-shirt",
        "men t-shirt",

        "men's t shirts",
        "mens t shirts",
        "men t shirts",

        "men's t shirt",
        "mens t shirt",
        "men t shirt",

        "t-shirt men",
        "t-shirts men",
        "t shirt men",
        "t shirts men",
    ]

    for pattern in men_tshirt_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "T-Shirts"

    # =====================================================
    # MEN SHIRT
    # =====================================================

    men_shirt_patterns = [

        "men's shirts",
        "mens shirts",
        "men shirts",

        "men's shirt",
        "mens shirt",
        "men shirt",

        "shirt men",
        "shirts men",

        "shirt of men",
        "shirt for men",
    ]

    for pattern in men_shirt_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Shirt"

    # =====================================================
    # MEN WATCH
    # =====================================================

    men_watch_patterns = [
        "men's watch",
        "mens watch",
        "men watch",
    ]

    for pattern in men_watch_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Watch"

    # =====================================================
    # MEN BELT
    # =====================================================

    men_belt_patterns = [
        "men's belt",
        "mens belt",
        "men belt",
    ]

    for pattern in men_belt_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Belt"

    # =====================================================
    # HANDBAG
    # =====================================================

    handbag_patterns = [
        "handbag",
        "handbags",
        "hand bag",
        "hand bags",
        "purse",
        "purses",
    ]

    for pattern in handbag_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Handbag"

    # =====================================================
    # WALLET
    # =====================================================

    wallet_patterns = [
        "wallet",
        "wallets",
    ]

    for pattern in wallet_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Wallet"

    # =====================================================
    # BACKPACK
    # =====================================================

    backpack_patterns = [
        "backpack",
        "backpacks",
        "back pack",
        "back packs",
    ]

    for pattern in backpack_patterns:

        if re.search(
            r"\b" + re.escape(pattern) + r"\b",
            text
        ):
            return "Backpack"

    # =====================================================
    # EXACT
    # =====================================================

    if text in SUBCATEGORY_ALIASES:
        return SUBCATEGORY_ALIASES[text]

    # =====================================================
    # LONGEST FIRST
    # =====================================================

    aliases = sorted(
        SUBCATEGORY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, value in aliases:

        if re.search(
            r"\b" + re.escape(key) + r"\b",
            text
        ):
            return value

    return None


# =========================================================
# DETECT COLOR
# =========================================================

def detect_color(text):

    if not text:
        return None

    text = text.strip().lower()

    if text in COLOR_ALIASES:
        return COLOR_ALIASES[text]

    aliases = sorted(
        COLOR_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, value in aliases:

        if key in text:
            return value

    return None


# =========================================================
# DETECT BUDGET
# =========================================================

def detect_budget(text):

    if not text:
        return None

    text = text.lower().replace(",", "")

    # =====================================================
    # 5000+
    # =====================================================

    if (
        "5000+" in text
        or "5000 above" in text
        or "above 5000" in text
        or "5000 or more" in text
        or "5000 and above" in text
        or "5k+" in text
        or "5k above" in text
        or "above 5k" in text
    ):
        return "5000+"

    # =====================================================
    # UNDER / BELOW / UP TO
    # =====================================================

    match = re.search(
        r"(?:under|below|upto|up to|within|max|maximum|"
        r"less than|not more than)"
        r"\s*(?:₹|rs\.?|inr)?\s*"
        r"(\d+(?:\.\d+)?)\s*(k)?\b",
        text
    )

    if match:

        value = float(
            match.group(1)
        )

        if match.group(2):
            value *= 1000

        return str(int(value))

    # =====================================================
    # ₹ / RS / INR
    # =====================================================

    match = re.search(
        r"(?:₹|rs\.?|inr)\s*"
        r"(\d+(?:\.\d+)?)\s*(k)?\b",
        text
    )

    if match:

        value = float(
            match.group(1)
        )

        if match.group(2):
            value *= 1000

        return str(int(value))

    # =====================================================
    # NORMAL NUMBER
    # =====================================================

    match = re.search(
        r"\b(\d{3,6})\b",
        text
    )

    if match:
        return match.group(1)

    return None


# =========================================================
# FIND MAIN CATEGORY FROM SUBCATEGORY
# =========================================================

def get_category_from_subcategory(subcategory):

    if not subcategory:
        return None

    if subcategory in [
        "Shirt",
        "T-Shirts",
        "Men Jeans",
        "Watch",
        "Belt",
    ]:
        return "Men"

    if subcategory in [
        "Dress",
        "Tops",
        "Saree",
        "Ethnic Wear",
        "Jeans",
    ]:
        return "Women"

    if subcategory in [
        "Makeup",
        "Haircare",
        "Skincare",
    ]:
        return "Beauty"

    if subcategory in [
        "Handbag",
        "Wallet",
        "Backpack",
    ]:
        return "Bags"

    return None


# =========================================================
# SET CATEGORY SESSION
# =========================================================

def set_category_session(request, category):

    request.session["main_category"] = category

    if category == "Women":

        request.session["gender"] = "Female"

    elif category == "Men":

        request.session["gender"] = "Male"

    else:

        request.session["gender"] = "Any"


# =========================================================
# PRODUCT TO DICT
# =========================================================

def product_to_dict(product):

    image_url = ""

    try:

        if product.image:
            image_url = product.image.url

    except Exception:

        image_url = ""

    return {

        "id": product.id,

        "name": product.name,

        "price": float(
            product.price
        ),

        "image": image_url,

        "category": (
            product.category.name
            if product.category
            else ""
        ),
    }


# =========================================================
# CLEAR AI SESSION
# =========================================================

def clear_ai_session(request):

    keys = [

        "main_category",
        "subcategory",
        "gender",
        "color",
        "budget",
        "occasion",
        "chat_messages",
        "outfit",
        "ai_mode",
    ]

    for key in keys:

        request.session.pop(
            key,
            None
        )

    request.session.modified = True


# =========================================================
# CURRENT AI STEP
# =========================================================

def get_current_step(request):

    main_category = request.session.get(
        "main_category"
    )

    subcategory = request.session.get(
        "subcategory"
    )

    color = request.session.get(
        "color"
    )

    budget = request.session.get(
        "budget"
    )

    ai_mode = request.session.get(
        "ai_mode",
        "normal"
    )

    outfit = request.session.get(
        "outfit"
    )

    if (
        outfit is not None
        and ai_mode in [
            "normal",
            "complete_outfit"
        ]
        and budget
    ):
        return "result"

    if not main_category:
        return "category"

    if not subcategory:

        if ai_mode == "complete_outfit":
            return "result"

        return "subcategory"

    if main_category != "Beauty":

        if not color:
            return "color"

    if not budget:
        return "budget"

    return "result"


# =========================================================
# GET MAX PRICE
# =========================================================

def get_max_price(request):

    budget = request.session.get(
        "budget"
    )

    if budget == "5000+":
        return 999999999

    if not budget:
        return 999999999

    try:

        return float(
            budget
        )

    except (
        TypeError,
        ValueError
    ):

        return 999999999


# =========================================================
# DATABASE CATEGORY QUERY
# =========================================================

def category_query(
    category_name,
    main_category=None
):

    query = Q()

    # =====================================================
    # MEN JEANS
    # =====================================================

    if (
        main_category == "Men"
        and category_name == "Men Jeans"
    ):

        names = [
            "Jeans Men's",
            "Jeans Mens",
            "Men's Jeans",
            "Mens Jeans",
            "Men Jeans",
        ]

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        # Extra flexible matching
        query |= Q(
            category__name__icontains="men"
        ) & Q(
            category__name__icontains="jean"
        )

        return query

    # =====================================================
    # WOMEN JEANS
    # =====================================================

    if (
        main_category == "Women"
        and category_name == "Jeans"
    ):

        names = [
            "Jeans",
            "Women's Jeans",
            "Womens Jeans",
            "Women Jeans",
        ]

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        return query

    # =====================================================
    # T-SHIRTS
    # =====================================================

    if category_name == "T-Shirts":

        # Exact aliases
        names = DATABASE_CATEGORY_ALIASES.get(
            "T-Shirts",
            []
        )

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        # Flexible database matching
        #
        # Matches:
        # T-Shirt
        # T-Shirts
        # T shirt
        # T shirts
        # Tshirt
        # Tshirts
        # Men T-Shirt
        # Men's T-Shirts
        #

        query |= Q(
            category__name__icontains="t-shirt"
        )

        query |= Q(
            category__name__icontains="t shirt"
        )

        query |= Q(
            category__name__icontains="tshirt"
        )

        # If category contains both men + t-shirt
        if main_category == "Men":

            query |= (
                Q(category__name__icontains="men")
                &
                (
                    Q(category__name__icontains="t-shirt")
                    |
                    Q(category__name__icontains="t shirt")
                    |
                    Q(category__name__icontains="tshirt")
                )
            )

        return query

    # =====================================================
    # SHIRT
    # =====================================================

    if category_name == "Shirt":

        names = DATABASE_CATEGORY_ALIASES.get(
            "Shirt",
            []
        )

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        query |= Q(
            category__name__icontains="shirt"
        )

        return query

    # =====================================================
    # WATCH
    # =====================================================

    if category_name == "Watch":

        names = DATABASE_CATEGORY_ALIASES.get(
            "Watch",
            []
        )

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        query |= Q(
            category__name__icontains="watch"
        )

        return query

    # =====================================================
    # BELT
    # =====================================================

    if category_name == "Belt":

        names = DATABASE_CATEGORY_ALIASES.get(
            "Belt",
            []
        )

        for name in names:
            query |= Q(
                category__name__iexact=name
            )

        query |= Q(
            category__name__icontains="belt"
        )

        return query

    # =====================================================
    # OTHER CATEGORIES
    # =====================================================

    names = DATABASE_CATEGORY_ALIASES.get(
        category_name,
        [category_name]
    )

    for name in names:

        query |= Q(
            category__name__iexact=name
        )

    # =====================================================
    # BAGS PARENT
    # =====================================================

    if category_name == "Bags":

        query |= Q(
            category__parent__name__iexact="Bags"
        )

    # =====================================================
    # HANDBAG
    # =====================================================

    elif category_name == "Handbag":

        query |= Q(
            category__name__icontains="handbag"
        )

        query |= Q(
            category__name__icontains="hand bag"
        )

        query |= Q(
            category__name__icontains="purse"
        )

    # =====================================================
    # WALLET
    # =====================================================

    elif category_name == "Wallet":

        query |= Q(
            category__name__icontains="wallet"
        )

    # =====================================================
    # BACKPACK
    # =====================================================

    elif category_name == "Backpack":

        query |= Q(
            category__name__icontains="backpack"
        )

        query |= Q(
            category__name__icontains="back pack"
        )

    return query


# =========================================================
# GET BASE PRODUCTS
# =========================================================

def get_base_products(request):

    subcategory = request.session.get(
        "subcategory"
    )

    main_category = request.session.get(
        "main_category"
    )

    color = request.session.get(
        "color"
    )

    max_price = get_max_price(
        request
    )

    products = Product.objects.filter(
        stock__gt=0,
        price__lte=max_price
    )

    # =====================================================
    # SUBCATEGORY
    # =====================================================

    if subcategory:

        products = products.filter(
            category_query(
                subcategory,
                main_category
            )
        )

    # =====================================================
    # MAIN CATEGORY
    # =====================================================

    elif main_category in [
        "Women",
        "Men",
        "Bags",
    ]:

        category_list = AI_CATEGORIES.get(
            main_category,
            []
        )

        combined_query = Q()

        for category_name in category_list:

            combined_query |= category_query(
                category_name,
                main_category
            )

        products = products.filter(
            combined_query
        )

    # =====================================================
    # COLOR
    # =====================================================

    if (
        color
        and color != "Any"
        and main_category != "Beauty"
    ):

        products = products.filter(
            color__icontains=color
        )

    return products.distinct()


# =========================================================
# NORMAL RECOMMENDATIONS
# =========================================================

def generate_recommendations(
    request,
    exclude_ids=None,
    category_names=None,
    limit=4
):

    if exclude_ids is None:
        exclude_ids = set()

    max_price = get_max_price(
        request
    )

    products = Product.objects.filter(
        stock__gt=0,
        price__lte=max_price
    )

    main_category = request.session.get(
        "main_category"
    )

    color = request.session.get(
        "color"
    )

    # =====================================================
    # CATEGORY-SPECIFIC RECOMMENDATIONS
    # =====================================================

    if category_names:

        combined_query = Q()

        for category_name in category_names:

            combined_query |= category_query(
                category_name,
                main_category
            )

        products = products.filter(
            combined_query
        )

    else:

        products = get_base_products(
            request
        )

    # =====================================================
    # EXCLUDE COMPLETE OUTFIT PRODUCTS
    # =====================================================

    if exclude_ids:

        products = products.exclude(
            id__in=exclude_ids
        )

    # =====================================================
    # COLOR PREFERENCE
    # =====================================================

    if (
        color
        and color != "Any"
        and main_category != "Beauty"
    ):

        same_color = products.filter(
            color__icontains=color
        )

        if same_color.exists():
            products = same_color

    products = list(
        products.distinct()
    )

    random.shuffle(
        products
    )

    return [
        product_to_dict(product)
        for product in products[:limit]
    ]


# =========================================================
# FIND PRODUCT FOR CATEGORY
# =========================================================

def find_product_for_category(
    request,
    category_name,
    used_product_ids=None,
    apply_color=True
):

    if used_product_ids is None:
        used_product_ids = set()

    main_category = request.session.get(
        "main_category"
    )

    color = request.session.get(
        "color"
    )

    max_price = get_max_price(
        request
    )

    query = category_query(
        category_name,
        main_category
    )

    products = Product.objects.filter(
        query,
        stock__gt=0,
        price__lte=max_price
    ).exclude(
        id__in=used_product_ids
    ).distinct()

    # =====================================================
    # COLOR
    # =====================================================

    if (
        apply_color
        and color
        and color != "Any"
        and main_category != "Beauty"
    ):

        same_color = products.filter(
            color__icontains=color
        )

        if same_color.exists():

            products = same_color

    products = products.exclude(
        id__in=used_product_ids
    )

    products = list(
        products
    )

    random.shuffle(
        products
    )

    if not products:
        return None

    return products[0]


# =========================================================
# GENERATE COMPLETE OUTFIT
# =========================================================

def generate_complete_outfit(request):

    main_category = request.session.get(
        "main_category"
    )

    subcategory = request.session.get(
        "subcategory"
    )

    occasion = request.session.get(
        "occasion"
    )

    # =====================================================
    # DETERMINE OUTFIT CATEGORIES
    # =====================================================

    if occasion:

        gender_outfits = (
            OCCASION_OUTFIT_CATEGORIES.get(
                main_category,
                {}
            )
        )

        outfit_categories = (
            gender_outfits.get(
                occasion,
                []
            )
        )

    elif subcategory:

        outfit_categories = (
            COMPLETE_OUTFIT_CATEGORIES.get(
                subcategory,
                [subcategory]
            )
        )

    else:

        if main_category == "Men":

            outfit_categories = [
                "Shirt",
                "Men Jeans",
                "Watch",
            ]

        elif main_category == "Beauty":

            outfit_categories = [
                "Makeup",
                "Skincare",
                "Haircare",
            ]

        elif main_category == "Bags":

            outfit_categories = [
                "Handbag",
                "Tops",
                "Jeans",
            ]

        else:

            # =================================================
            # WOMEN DEFAULT = COLLAGE
            # =================================================

            outfit_categories = [
                "Tops",
                "Jeans",
                "Handbag",
            ]

    # =====================================================
    # BEAUTY
    # =====================================================

    if main_category == "Beauty":

        beauty_outfit = {

            "Makeup": [
                "Makeup",
                "Skincare",
                "Haircare",
            ],

            "Skincare": [
                "Skincare",
                "Haircare",
                "Makeup",
            ],

            "Haircare": [
                "Haircare",
                "Skincare",
                "Makeup",
            ],
        }

        outfit_categories = beauty_outfit.get(
            subcategory,
            [
                "Makeup",
                "Skincare",
                "Haircare",
            ]
        )

    # =====================================================
    # WOMEN COLLAGE FORCE
    # =====================================================

    # If no occasion is selected and user is in Women,
    # always Tops + Jeans + Handbag.

    if (
        main_category == "Women"
        and not occasion
    ):

        outfit_categories = [
            "Tops",
            "Jeans",
            "Handbag",
        ]

    # =====================================================
    # SELECT PRODUCTS
    # =====================================================

    complete_products = []

    used_product_ids = set()

    used_category_names = set()

    for category_name in outfit_categories:

        product = find_product_for_category(
            request=request,
            category_name=category_name,
            used_product_ids=used_product_ids,
            apply_color=True
        )

        if not product:
            continue

        actual_category = (
            product.category.name
            if product.category
            else ""
        )

        # =================================================
        # AVOID DUPLICATE PRODUCT
        # =================================================

        if product.id in used_product_ids:
            continue

        # =================================================
        # AVOID SAME ACTUAL CATEGORY
        # =================================================

        if actual_category in used_category_names:
            continue

        complete_products.append(
            product
        )

        used_product_ids.add(
            product.id
        )

        used_category_names.add(
            actual_category
        )

        if len(complete_products) >= 4:
            break

    # =====================================================
    # NO PRODUCTS
    # =====================================================

    if not complete_products:

        outfit = {

            "products": [],

            "matching_products": [],

            "complete_outfit_products": [],

            "recommendations": [],

            "is_complete_outfit": True,

            "no_products": True,
        }

        request.session["outfit"] = outfit

        request.session.modified = True

        return outfit

    # =====================================================
    # COMPLETE DATA
    # =====================================================

    complete_outfit_data = [

        product_to_dict(product)

        for product in complete_products

    ]

    # =====================================================
    # RECOMMENDATIONS
    #
    # VERY IMPORTANT:
    # Recommendations use SAME outfit categories.
    #
    # Example:
    # Wedding:
    # Saree + Ethnic Wear + Jewelry + Handbag
    #
    # Collage:
    # Tops + Jeans + Handbag
    #
    # No Dress/Wallet randomly.
    # =====================================================

    complete_ids = {
        product.id
        for product in complete_products
    }

    recommendations = generate_recommendations(
        request,
        exclude_ids=complete_ids,
        category_names=outfit_categories,
        limit=4
    )

    # =====================================================
    # SAVE RESULT
    # =====================================================

    outfit = {

        "products": complete_outfit_data,

        "matching_products": [],

        "complete_outfit_products":
            complete_outfit_data,

        "recommendations":
            recommendations,

        "is_complete_outfit": True,

        "no_products": False,
    }

    request.session["outfit"] = outfit

    request.session.modified = True

    return outfit


# =========================================================
# NORMAL RESULT
# =========================================================

def generate_normal_result(request):

    recommendations = generate_recommendations(
        request
    )

    subcategory = request.session.get(
        "subcategory"
    )

    # =====================================================
    # NO PRODUCTS
    # =====================================================

    if not recommendations:

        outfit = {

            "products": [],

            "matching_products": [],

            "complete_outfit_products": [],

            "recommendations": [],

            "is_complete_outfit": False,

            "no_products": True,
        }

        request.session["outfit"] = outfit

        request.session.modified = True

        return outfit

    # =====================================================
    # MATCHING PRODUCTS
    # =====================================================

    matching_categories = MATCHING_PRODUCTS.get(
        subcategory,
        []
    )

    matching_products = []

    used_product_ids = {
        product["id"]
        for product in recommendations
    }

    for category_name in matching_categories:

        product = find_product_for_category(
            request=request,
            category_name=category_name,
            used_product_ids=used_product_ids,
            apply_color=True
        )

        if not product:
            continue

        matching_products.append(
            product
        )

        used_product_ids.add(
            product.id
        )

        if len(matching_products) >= 3:
            break

    matching_products_data = [

        product_to_dict(product)

        for product in matching_products

    ]

    outfit = {

        "products": recommendations,

        "matching_products":
            matching_products_data,

        "complete_outfit_products": [],

        "recommendations":
            recommendations,

        "is_complete_outfit": False,

        "no_products": False,
    }

    request.session["outfit"] = outfit

    request.session.modified = True

    return outfit


# =========================================================
# AI STYLE ASSISTANT
# =========================================================

@login_required(login_url="login")
def style_assistant(request):

    # =====================================================
    # RESET
    # =====================================================

    if request.GET.get("reset"):

        clear_ai_session(
            request
        )

        return redirect(
            "style_assistant"
        )

    # =====================================================
    # CHAT
    # =====================================================

    chat_messages = request.session.get(
        "chat_messages",
        []
    )

    if not chat_messages:

        chat_messages = [

            {
                "sender": "ai",
                "text": (
                    "Hi! 👋 I'm your AI Fashion Stylist. "
                    "Tell me what you're looking for and "
                    "I'll help you find the perfect products."
                ),
            }

        ]

        request.session[
            "chat_messages"
        ] = chat_messages

        request.session.modified = True

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        posted_step = request.POST.get(
            "step"
        )

        # =================================================
        # CHAT MESSAGE
        # =================================================

        message = request.POST.get(
            "message"
        )

        if message:

            message = message.strip()

            if message:

                chat_messages.append({
                    "sender": "user",
                    "text": message,
                })

                # =================================================
                # DETECTION
                # =================================================

                detected_complete = detect_complete_outfit(
                    message
                )

                detected_collage = detect_collage(
                    message
                )

                detected_category = detect_main_category(
                    message
                )

                detected_subcategory = detect_subcategory(
                    message
                )

                detected_color = detect_color(
                    message
                )

                detected_budget = detect_budget(
                    message
                )

                detected_occasion = detect_occasion(
                    message
                )

                message_lower = message.lower()

                # =================================================
                # STRONG MEN / WOMEN DETECTION
                # =================================================

                has_men_word = bool(
                    re.search(
                        r"\b(men|mens|men's|man|male|boy|boys)\b",
                        message_lower
                    )
                )

                has_women_word = bool(
                    re.search(
                        r"\b(women|womens|women's|woman|female|ladies|girl|girls)\b",
                        message_lower
                    )
                )

                # =================================================
                # MEN JEANS
                # =================================================

                if (
                    detected_subcategory == "Men Jeans"
                    or (
                        "jeans" in message_lower
                        and has_men_word
                    )
                ):

                    detected_subcategory = "Men Jeans"

                    detected_category = "Men"

                # =================================================
                # MEN T-SHIRT
                # =================================================

                elif (
                    detected_subcategory == "T-Shirts"
                    and has_men_word
                ):

                    detected_category = "Men"

                # =================================================
                # MEN SHIRT
                # =================================================

                elif (
                    detected_subcategory == "Shirt"
                    and has_men_word
                ):

                    detected_category = "Men"

                # =================================================
                # MEN WATCH
                # =================================================

                elif (
                    detected_subcategory == "Watch"
                    and has_men_word
                ):

                    detected_category = "Men"

                # =================================================
                # MEN BELT
                # =================================================

                elif (
                    detected_subcategory == "Belt"
                    and has_men_word
                ):

                    detected_category = "Men"

                # =================================================
                # WOMEN JEANS
                # =================================================

                elif (
                    detected_subcategory == "Jeans"
                    and has_women_word
                ):

                    detected_category = "Women"

                # =================================================
                # BAG CATEGORY
                # =================================================

                if detected_subcategory in [
                    "Handbag",
                    "Wallet",
                    "Backpack",
                ]:

                    detected_category = "Bags"

                # =================================================
                # COMPLETE / COLLAGE OUTFIT
                # =================================================

                if detected_complete:

                    # -------------------------------------------------
                    # COLLAGE ALWAYS WOMEN
                    # -------------------------------------------------

                    if detected_collage:

                        main_category = "Women"

                        request.session[
                            "subcategory"
                        ] = None

                        request.session[
                            "occasion"
                        ] = None

                    # -------------------------------------------------
                    # MEN
                    # -------------------------------------------------

                    elif has_men_word:

                        main_category = "Men"

                    # -------------------------------------------------
                    # WOMEN
                    # -------------------------------------------------

                    elif has_women_word:

                        main_category = "Women"

                    # -------------------------------------------------
                    # CATEGORY
                    # -------------------------------------------------

                    elif detected_category in [
                        "Women",
                        "Men",
                        "Bags",
                        "Beauty",
                    ]:

                        main_category = detected_category

                    # -------------------------------------------------
                    # SUBCATEGORY
                    # -------------------------------------------------

                    elif detected_subcategory:

                        main_category = (
                            get_category_from_subcategory(
                                detected_subcategory
                            )
                        )

                    else:

                        main_category = "Women"

                    set_category_session(
                        request,
                        main_category
                    )

                    # =================================================
                    # SUBCATEGORY
                    # =================================================

                    if detected_collage:

                        request.session[
                            "subcategory"
                        ] = None

                    elif detected_occasion:

                        request.session[
                            "subcategory"
                        ] = None

                    else:

                        request.session[
                            "subcategory"
                        ] = detected_subcategory

                    # =================================================
                    # OCCASION
                    # =================================================

                    if detected_collage:

                        request.session[
                            "occasion"
                        ] = None

                    else:

                        request.session[
                            "occasion"
                        ] = detected_occasion

                    # =================================================
                    # COLOR
                    # =================================================

                    if main_category == "Beauty":

                        request.session[
                            "color"
                        ] = "Any"

                    else:

                        request.session[
                            "color"
                        ] = (
                            detected_color
                            if detected_color
                            else "Any"
                        )

                    # =================================================
                    # BUDGET
                    # =================================================

                    request.session[
                        "budget"
                    ] = (
                        detected_budget
                        if detected_budget
                        else "5000+"
                    )

                    # =================================================
                    # MODE
                    # =================================================

                    request.session[
                        "ai_mode"
                    ] = "complete_outfit"

                    request.session[
                        "outfit"
                    ] = None

                    # =================================================
                    # GENERATE
                    # =================================================

                    outfit = generate_complete_outfit(
                        request
                    )

                    if outfit.get("no_products"):

                        response_text = (
                            "😔 No matching products found"
                        )

                    else:

                        if detected_collage:

                            response_text = (
                                "Perfect! ✨ "
                                "I created a women collage outfit "
                                "with Tops, Jeans and Handbag. 💖"
                            )

                        elif detected_occasion:

                            response_text = (
                                "Perfect! ✨ I created a "
                                f"complete {detected_occasion} "
                                f"outfit for {main_category}. 💖"
                            )

                        else:

                            response_text = (
                                "Perfect! ✨ "
                                "I created a complete outfit for you. 💖"
                            )

                        if detected_color:

                            response_text += (
                                f" Color: {detected_color}."
                            )

                        if detected_budget:

                            response_text += (
                                f" Budget: ₹{detected_budget}."
                            )

                    chat_messages.append({
                        "sender": "ai",
                        "text": response_text,
                    })

                # =================================================
                # NORMAL SUBCATEGORY
                # =================================================

                elif detected_subcategory:

                    if detected_subcategory in [
                        "Shirt",
                        "T-Shirts",
                        "Men Jeans",
                        "Watch",
                        "Belt",
                    ]:

                        main_category = "Men"

                    elif detected_subcategory in [
                        "Dress",
                        "Tops",
                        "Saree",
                        "Ethnic Wear",
                        "Jeans",
                    ]:

                        main_category = "Women"

                    elif detected_subcategory in [
                        "Handbag",
                        "Wallet",
                        "Backpack",
                    ]:

                        main_category = "Bags"

                    elif detected_category:

                        main_category = detected_category

                    else:

                        main_category = (
                            get_category_from_subcategory(
                                detected_subcategory
                            )
                        )

                    if main_category:

                        set_category_session(
                            request,
                            main_category
                        )

                        request.session[
                            "subcategory"
                        ] = detected_subcategory

                        request.session[
                            "occasion"
                        ] = None

                        request.session[
                            "ai_mode"
                        ] = "normal"

                        if main_category == "Beauty":

                            request.session[
                                "color"
                            ] = "Any"

                        else:

                            request.session[
                                "color"
                            ] = (
                                detected_color
                                if detected_color
                                else "Any"
                            )

                        request.session[
                            "budget"
                        ] = (
                            detected_budget
                            if detected_budget
                            else "5000+"
                        )

                        request.session[
                            "outfit"
                        ] = None

                        outfit = generate_normal_result(
                            request
                        )

                        if outfit.get("no_products"):

                            response_text = (
                                "😔 No matching products found"
                            )

                        else:

                            count = len(
                                outfit.get(
                                    "products",
                                    []
                                )
                            )

                            response_text = (
                                f"Perfect! ✨ I found "
                                f"{detected_subcategory}"
                            )

                            if (
                                detected_color
                                and main_category != "Beauty"
                            ):

                                response_text += (
                                    f" in {detected_color}"
                                )

                            if detected_budget:

                                response_text += (
                                    f" under ₹{detected_budget}"
                                )

                            response_text += (
                                f". Here are {count} "
                                f"recommendation"
                                f"{'s' if count != 1 else ''} "
                                "for you. 🛍️"
                            )

                        chat_messages.append({
                            "sender": "ai",
                            "text": response_text,
                        })

                # =================================================
                # OCCASION ONLY
                # =================================================

                elif detected_occasion:

                    if has_men_word:

                        main_category = "Men"

                    elif has_women_word:

                        main_category = "Women"

                    elif detected_category in [
                        "Women",
                        "Men",
                        "Bags",
                    ]:

                        main_category = detected_category

                    else:

                        main_category = "Women"

                    set_category_session(
                        request,
                        main_category
                    )

                    request.session[
                        "subcategory"
                    ] = None

                    request.session[
                        "occasion"
                    ] = detected_occasion

                    request.session[
                        "color"
                    ] = (
                        detected_color
                        if detected_color
                        else "Any"
                    )

                    request.session[
                        "budget"
                    ] = (
                        detected_budget
                        if detected_budget
                        else "5000+"
                    )

                    request.session[
                        "ai_mode"
                    ] = "complete_outfit"

                    request.session[
                        "outfit"
                    ] = None

                    outfit = generate_complete_outfit(
                        request
                    )

                    if outfit.get("no_products"):

                        response_text = (
                            "😔 No matching products found"
                        )

                    else:

                        response_text = (
                            "Perfect! ✨ I created a "
                            f"complete {detected_occasion} "
                            f"outfit for {main_category}. 💖"
                        )

                        if detected_color:

                            response_text += (
                                f" Color: {detected_color}."
                            )

                        if detected_budget:

                            response_text += (
                                f" Budget: ₹{detected_budget}."
                            )

                    chat_messages.append({
                        "sender": "ai",
                        "text": response_text,
                    })

                                    # ================================================= 
                # MAIN CATEGORY 
                # ================================================= 

                elif detected_category: 

                    set_category_session( 
                        request, 
                        detected_category 
                    ) 
 
                    request.session["subcategory"] = None
                    request.session["color"] = None
                    request.session["budget"] = None
                    request.session["occasion"] = None
                    request.session["ai_mode"] = "normal"
                    request.session["outfit"] = None

                    chat_messages.append({ 
                        "sender": "ai", 
                        "text": ( 
                            f"Great! ✨ "
                            f"{detected_category} selected. "
                            "Now choose a product type." 
                        ), 
                    })

                # =================================================
                # COLOR
                # =================================================

                elif detected_color:

                    request.session[
                        "color"
                    ] = detected_color

                    chat_messages.append({
                        "sender": "ai",
                        "text": (
                            f"Nice! 🎨 "
                            f"{detected_color} selected. "
                            "What product would you like?"
                        ),
                    })

                # =================================================
                # BUDGET
                # =================================================

                elif detected_budget:

                    request.session[
                        "budget"
                    ] = detected_budget

                    chat_messages.append({
                        "sender": "ai",
                        "text": (
                            f"₹{detected_budget} budget noted. 💰 "
                            "What product would you like?"
                        ),
                    })

                                    # =================================================
                # NOTHING / UNKNOWN INPUT
                # =================================================

                else:

                    chat_messages.append({
                        "sender": "ai",
                        "text": (
                            "Sorry, I couldn't understand that. "
                            "Please try again."
                        ),
                    })

                    chat_messages.append({
                        "sender": "ai",
                        "text": "Select from this category:",
                    })

                    # Reset selection
                    request.session["main_category"] = None
                    request.session["subcategory"] = None
                    request.session["gender"] = None
                    request.session["color"] = None
                    request.session["budget"] = None
                    request.session["occasion"] = None
                    request.session["ai_mode"] = "normal"
                    request.session["outfit"] = None

                request.session[
                    "chat_messages"
                ] = chat_messages

                request.session.modified = True

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # STOP
        # =====================================================

        if posted_step == "stop":

            clear_ai_session(
                request
            )

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # SKIP
        # =====================================================

        if posted_step == "skip":

            skip_step = request.POST.get(
                "skip_step"
            )

            # -------------------------------------------------
            # SKIP COLOR
            # -------------------------------------------------

            if skip_step == "color":

                request.session[
                    "color"
                ] = "Any"

                chat_messages.append({
                    "sender": "user",
                    "text": "Any color",
                })

                chat_messages.append({
                    "sender": "ai",
                    "text": (
                        "No problem! 🎨 Any color selected. "
                        "Now choose your budget."
                    ),
                })

            # -------------------------------------------------
            # SKIP BUDGET
            # -------------------------------------------------

            elif skip_step == "budget":

                request.session[
                    "budget"
                ] = "5000+"

                chat_messages.append({
                    "sender": "user",
                    "text": "Any budget",
                })

                if (
                    request.session.get(
                        "ai_mode"
                    )
                    == "complete_outfit"
                ):

                    outfit = generate_complete_outfit(
                        request
                    )

                else:

                    outfit = generate_normal_result(
                        request
                    )

                if outfit.get("no_products"):

                    response_text = (
                        "😔 No matching products found"
                    )

                else:

                    response_text = (
                        "Perfect! 🤖 "
                        "Here are your recommendations."
                    )

                chat_messages.append({
                    "sender": "ai",
                    "text": response_text,
                })

            request.session[
                "chat_messages"
            ] = chat_messages

            request.session.modified = True

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # CURRENT STEP
        # =====================================================

        step = get_current_step(
            request
        )

        # =====================================================
        # CATEGORY
        # =====================================================

        if step == "category":

            selected = request.POST.get(
                "category"
            )

            if selected in AI_CATEGORIES:

                set_category_session(
                    request,
                    selected
                )

                request.session[
                    "subcategory"
                ] = None

                request.session[
                    "color"
                ] = None

                request.session[
                    "budget"
                ] = None

                request.session[
                    "occasion"
                ] = None

                request.session[
                    "ai_mode"
                ] = "normal"

                request.session[
                    "outfit"
                ] = None

                chat_messages.append({
                    "sender": "user",
                    "text": selected,
                })

                chat_messages.append({
                    "sender": "ai",
                    "text": (
                        f"Great! ✨ "
                        f"{selected} selected. "
                        "Now choose a product type."
                    ),
                })

                request.session[
                    "chat_messages"
                ] = chat_messages

                request.session.modified = True

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # SUBCATEGORY
        # =====================================================

        if step == "subcategory":

            selected = request.POST.get(
                "subcategory"
            )

            main_category = request.session.get(
                "main_category"
            )

            valid_options = AI_CATEGORIES.get(
                main_category,
                []
            )

            if selected in valid_options:

                request.session[
                    "subcategory"
                ] = selected

                request.session[
                    "occasion"
                ] = None

                request.session[
                    "ai_mode"
                ] = "normal"

                request.session[
                    "budget"
                ] = None

                request.session[
                    "outfit"
                ] = None

                if main_category == "Beauty":

                    request.session[
                        "color"
                    ] = "Any"

                else:

                    request.session[
                        "color"
                    ] = None

                chat_messages.append({
                    "sender": "user",
                    "text": selected,
                })

                if main_category == "Beauty":

                    chat_messages.append({
                        "sender": "ai",
                        "text": (
                            f"Nice choice! 👌 "
                            f"{selected} selected. "
                            "Now choose your budget. 💰"
                        ),
                    })

                else:

                    chat_messages.append({
                        "sender": "ai",
                        "text": (
                            f"Nice choice! 👌 "
                            f"{selected} selected. "
                            "Now choose your preferred color."
                        ),
                    })

                request.session[
                    "chat_messages"
                ] = chat_messages

                request.session.modified = True

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # COLOR
        # =====================================================

        if step == "color":

            selected = request.POST.get(
                "color"
            )

            valid_colors = [
                "Black",
                "White",
                "Brown",
                "Blue",
                "Pink",
                "Green",
                "Purple",
                "Any",
            ]

            if selected in valid_colors:

                request.session[
                    "color"
                ] = selected

                chat_messages.append({
                    "sender": "user",
                    "text": selected,
                })

                chat_messages.append({
                    "sender": "ai",
                    "text": (
                        f"Great color choice! 🎨 "
                        f"{selected} selected. "
                        "Now choose your budget."
                    ),
                })

                request.session[
                    "chat_messages"
                ] = chat_messages

                request.session.modified = True

            return redirect(
                "style_assistant"
            )

        # =====================================================
        # BUDGET
        # =====================================================

        if step == "budget":

            selected = request.POST.get(
                "budget"
            )

            valid_budgets = [
                "1000",
                "2000",
                "3000",
                "5000",
                "5000+",
            ]

            if selected in valid_budgets:

                request.session[
                    "budget"
                ] = selected

                chat_messages.append({
                    "sender": "user",
                    "text": f"₹{selected}",
                })

                # =================================================
                # GENERATE
                # =================================================

                if (
                    request.session.get(
                        "ai_mode"
                    )
                    == "complete_outfit"
                ):

                    outfit = generate_complete_outfit(
                        request
                    )

                else:

                    outfit = generate_normal_result(
                        request
                    )

                # =================================================
                # RESULT MESSAGE
                # =================================================

                if outfit.get("no_products"):

                    response_text = (
                        "😔 No matching products found"
                    )

                else:

                    count = len(
                        outfit.get(
                            "products",
                            []
                        )
                    )

                    response_text = (
                        "Perfect! ✨\n"
                        "I found the best products for you."
                    )

                    if count:

                        response_text += (
                            f" {count} recommendation"
                            f"{'s' if count != 1 else ''} "
                            "available. 🛍️"
                        )

                chat_messages.append({
                    "sender": "ai",
                    "text": response_text,
                })

                request.session[
                    "chat_messages"
                ] = chat_messages

                request.session.modified = True

                return redirect(
                    "style_assistant"
                )

    # =========================================================
    # SESSION DATA
    # =========================================================

    main_category = request.session.get(
        "main_category"
    )

    subcategory = request.session.get(
        "subcategory"
    )

    gender = request.session.get(
        "gender"
    )

    color = request.session.get(
        "color"
    )

    budget = request.session.get(
        "budget"
    )

    occasion = request.session.get(
        "occasion"
    )

    outfit = request.session.get(
        "outfit"
    )

    ai_mode = request.session.get(
        "ai_mode",
        "normal"
    )

    # =========================================================
    # SUBCATEGORY OPTIONS
    # =========================================================

    subcategory_options = AI_CATEGORIES.get(
        main_category,
        []
    )
    category_icons = {
        "Women": "👗",
        "Men": "👕",
        "Beauty": "💄",
        "Bags": "👜",
    }

    category_options = [
        {
            "value": category,
            "name": category,
            "icon": category_icons.get(category, "")
        }
        for category in AI_CATEGORIES.keys()
    ]
    color_options = [
        {"value": "Black", "name": "Black", "icon": "⚫"},
        {"value": "White", "name": "White", "icon": "⚪"},
        {"value": "Brown", "name": "Brown", "icon": "🟤"},
        {"value": "Blue", "name": "Blue", "icon": "🔵"},
        {"value": "Pink", "name": "Pink", "icon": "🩷"},
        {"value": "Green", "name": "Green", "icon": "🟢"},
        {"value": "Purple", "name": "Purple", "icon": "🟣"},
        {"value": "Any", "name": "Any", "icon": "🌈"},
    ]
    budget_options = [
        {"value": "1000", "name": "₹1000"},
        {"value": "2000", "name": "₹2000"},
        {"value": "3000", "name": "₹3000"},
        {"value": "5000", "name": "₹5000"},
        {"value": "5000+", "name": "₹5000+"},
    ]
    subcategory_icons = {
            "Dress": "👗",
            "Tops": "👚",
            "Saree": "🥻",
            "Ethnic Wear": "👘",
            "Jeans": "👖",
            "T-Shirts": "👕",
            "Shirt": "👔",
            "Watch": "⌚",
            "Belt": "🪢",
            "Makeup": "💄",
            "Haircare": "💇",
            "Skincare": "🧴",
            "Handbag": "👜",
            "Wallet": "👛",
            "Backpack": "🎒",
        }

    subcategory_options = [
            {
                "name": item,
                "icon": subcategory_icons.get(item, "")
            }
            for item in subcategory_options
        ]
    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "step": get_current_step(
            request
        ),

        "main_category": main_category,

        "subcategory": subcategory,

        "gender": gender,

        "color": color,

        "budget": budget,

        "occasion": occasion,

        "ai_mode": ai_mode,

        "chat_messages": chat_messages,

        "outfit": outfit,

        "subcategory_options":
            subcategory_options,
        "category_options": category_options,
        "color_options": color_options,
        "budget_options": budget_options,
    }

    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "ai_assistant/assistant.html",
        context
    )