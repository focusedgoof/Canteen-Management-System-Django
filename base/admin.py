from django.contrib import admin
from .models import Employees, Items,Purchases

admin.site.register(Employees)
admin.site.register(Items)
admin.site.register(Purchases)