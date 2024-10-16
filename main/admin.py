from django.contrib import admin
from .models import News, Actions, Company

class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'published_at',)
    search_fields = ('name',)

class ActionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'published_at',)
    search_fields = ('name',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Company, CompanyAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Actions, ActionsAdmin)


