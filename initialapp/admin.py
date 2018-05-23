from django.contrib import admin
from initialapp.models import *

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
		pass
admin.site.register(Item, ItemAdmin)