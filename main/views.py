
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Actions, Cart, CartItem, Company
from goods.models import Category, Catalog, Product
from django.contrib.contenttypes.models import ContentType

def index(request):
    return render(request, 'main/index.html')

def news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'main/news.html', {'news': news_item})

def news_list(request):
    news_list = News.objects.all()  # Получаем все новости
    return render(request, 'main/news_list.html', {'news_list': news_list})

def contacts(request):
    return render(request, 'main/contacts.html')

def company(request):
    company_item = get_object_or_404(Company)
    news_list = News.objects.order_by('-published_at')[:5]  
    return render(request, 'main/company.html', {
        'company': company_item,
        'news_list': news_list  # Объединяем словари
    })

def actions(request, actions_id):
    actions_item = get_object_or_404(Actions, id=actions_id)
    return render(request, 'main/actions.html', {'actions': actions_item})

def actions_list(request):
    actions_list = Actions.objects.all()  # Получаем все новости
    return render(request, 'main/actions_list.html', {'actions_list': actions_list})

def index(request):
    catalogs = Catalog.objects.all()  # Получаем все каталоги
    categories = Category.objects.prefetch_related('subcategories')  # Получаем категории с подкатегориями
    
    context = {
        'catalogs': catalogs,
        'categories': categories,
    }
    
    return render(request, 'main/index.html', context)

def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    valid_content_types = ContentType.objects.get_for_models(Product).values()
    items = items.filter(content_type__in=valid_content_types)
    return render(request, 'main/cart_detail.html', {'cart': cart, 'items': items})

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

def add_to_cart(request, type, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)  # Получаем продукт
        cart, created = Cart.objects.get_or_create(user=request.user)  # Получаем или создаем корзину

        # Получаем content type для продукта
        product_content_type = ContentType.objects.get_for_model(Product)

        # Проверяем, есть ли уже этот продукт в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=product_content_type,
            object_id=product.id  # Здесь используем object_id вместо product
        )

        if not created:
            cart_item.quantity += 1  # Увеличиваем количество, если товар уже в корзине
        else:
            cart_item.quantity = 1  # Устанавливаем количество 1, если это новый товар

        cart_item.save()  # Сохраняем изменения
        return redirect('cart_detail')  # Перенаправляем на страницу корзины
    return redirect('catalog')  # Если метод не POST, перенаправляем на каталог