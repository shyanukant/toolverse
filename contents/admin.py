from django.contrib import admin
from .models import ResponseModel


# class ContentModelAdmin(admin.ModelAdmin):
#     list_display = ('id', 'response', 'created_at', 'user')

# Register your models here.
admin.site.register(ResponseModel)