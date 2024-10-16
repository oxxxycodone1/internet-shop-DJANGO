from django.shortcuts import render, get_object_or_404
from .models import Catalog, Category, SubCategory, Product, Filter

def catalog_view(request):
    catalogs = Catalog.objects.all()  # Получаем все каталоги
    catalogs = Catalog.objects.prefetch_related('categories__subcategories').all()
    
    for catalog in catalogs:
        catalog.product_count = Product.objects.filter(subcategory__category__catalog=catalog).count()

    context = {
        'catalogs': catalogs,
    }
    return render(request, 'goods/catalog.html', context)

def category_view(request, catalog_id):
    # Получаем конкретный каталог по его ID
    catalog = get_object_or_404(Catalog, id=catalog_id)
    
    # Получаем категории, связанные с данным каталогом
    categories = catalog.categories.all()

    # Получаем подкатегории для выбранного каталога
    subcategories = SubCategory.objects.filter(category__in=categories)

    # Получаем все продукты, относящиеся к подкатегориям
    products = Product.objects.filter(subcategory__in=subcategories)

    # Логика сортировки
    sort = request.GET.get('sort', 'price_asc')
    if sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('price')  # price_asc

    # Определяем название для отображения
    filter_names = {
        'price_asc': 'По цене (возрастание)',
        'price_desc': 'По цене (убывание)',
        'name_asc': 'По алфавиту (от А до Я)',
        'name_desc': 'По алфавиту (от Я до А)',
    }
    current_filter_name = filter_names.get(sort, 'По цене (возрастание)')

    # Передаем в контекст шаблона данные каталога, категорий и продуктов
    context = {
        'catalog': catalog,
        'categories': categories,
        'products': products,
        'current_filter_name': current_filter_name,
    }
    
    return render(request, 'goods/category.html', context)


def subcategory_view(request, catalog_id, subcategory_id):
    catalog = get_object_or_404(Catalog, id=catalog_id)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    
    # Получаем все продукты, относящиеся к выбранной подкатегории
    products = Product.objects.filter(subcategory=subcategory)
    
    # Получаем фильтры для текущей подкатегории
    filters = Filter.objects.filter(subcategory=subcategory)

    # Применяем фильтры, если они указаны в запросе
    selected_filter_values = request.GET.getlist('filter')  # Получаем выбранные фильтры
    if selected_filter_values:
        products = products.filter(filters__value__in=selected_filter_values).distinct()  # Фильтруем по выбранным фильтрам

    categories = catalog.categories.all()  # Для навигации по категориям и подкатегориям

    context = {
        'catalog': catalog,
        'subcategory': subcategory,
        'products': products,
        'categories': categories,
        'filters': filters,  # Передаем фильтры в шаблон
    }
    return render(request, 'goods/subcategory.html', context)



def product_detail_view(request, catalog_id, subcategory_id, product_id):
    product = get_object_or_404(Product, id=product_id)
    category = get_object_or_404(SubCategory, id=subcategory_id)
    
    return render(request, 'goods/product_detail.html', {
        'product': product,
        'category': category,
        'subcategory': category,
    })

