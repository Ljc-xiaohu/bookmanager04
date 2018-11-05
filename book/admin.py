from django.contrib import admin
from .models import BookInfo
# Register your models here.

class BookInfoAdmin(admin.ModelAdmin):

    list_display = ['id','name']

    list_filter = ['name']

admin.site.register(BookInfo,BookInfoAdmin)