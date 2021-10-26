from django.contrib import admin
# from .models import related models

from .models import CarMake, CarModel


# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name','type']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ['name','description']


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)