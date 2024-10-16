from django.db import models

class Catalog(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    catalog = models.ForeignKey(Catalog, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='goods/', blank=True, null=True)
    filters = models.ManyToManyField('FilterOption', related_name='products', blank=True)  # Используем строковое имя

    def __str__(self):
        return self.name

class Filter(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, related_name='filters', on_delete=models.CASCADE)
    filter_type = models.CharField(max_length=50, choices=[('range', 'Range'), ('select', 'Select')])

    def __str__(self):
        return self.name

class FilterOption(models.Model):
    filter = models.ForeignKey(Filter, related_name='options', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value