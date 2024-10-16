from django.contrib import admin
from .models import Catalog, Category, SubCategory, Product, Filter, FilterOption

# TabularInline для продуктов
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

# TabularInline для подкатегорий
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

# Inline для опций фильтров
class FilterOptionInline(admin.TabularInline):
    model = FilterOption
    extra = 1

# Inline для фильтров
class FilterInline(admin.TabularInline):
    model = Filter
    extra = 1

# Admin для категорий с изменённым шаблоном
class CategoryAdmin(admin.ModelAdmin):
    # Убираем change_list_template, чтобы не отображать его
    list_display = ('name', 'catalog')

    def get_urls(self):
        urls = super().get_urls()
        return urls  # Просто возвращаем стандартные URL без дополнительных

# Admin для каталога
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin для подкатегорий
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [FilterInline]  # Возможность добавлять фильтры прямо из подкатегорий

# Admin для продуктов
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price',)
    search_fields = ('name',)
    list_filter = ('subcategory',)
    filter_horizontal = ('filters',)  # Используем для выбора фильтров

# Admin для фильтров
class FilterAdmin(admin.ModelAdmin):
    inlines = [FilterOptionInline]  # Возможность добавлять опции фильтров

# Регистрация моделей
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Filter, FilterAdmin)
