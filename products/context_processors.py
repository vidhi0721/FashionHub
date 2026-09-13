from .models import Category
def categories(request):
    from .models import Category

    return {
        "categories": Category.objects.all()
    }