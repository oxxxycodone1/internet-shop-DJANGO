from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main.views import (
    news_list,
    news,
    contacts,
    index,
    company,
    actions_list,
    actions,
    cart_detail,
    remove_from_cart,
    add_to_cart,
)

from goods.views import (
    catalog_view,
    category_view,
    subcategory_view,
    product_detail_view
)

from users.views import (
    register,
    profile,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('news/', news_list, name='news_list'),  # Список всех новостей
    path('news/<int:news_id>/', news, name='news'), # Определенная новость
    path('contacts/', contacts, name='contacts'),
    path('company/', company, name='company'),
    path('actions/', actions_list, name='actions_list'),   # Список всех акций
    path('actions/<int:actions_id>/', actions, name='actions'), # Определенная акция
    path('catalog/', catalog_view, name='catalog'),
    path('catalog/<int:catalog_id>/', category_view, name='category'), 
    path('catalog/<int:catalog_id>/<int:subcategory_id>/', subcategory_view, name='subcategory'), 
    path('catalog/<int:catalog_id>/<int:subcategory_id>/<int:product_id>/', product_detail_view, name='product'),  
    path('cart/', cart_detail, name='cart_detail'),
    path('add-to-cart/<str:type>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
]

# Добавление статических файлов (если нужно)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
