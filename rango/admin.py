from django.contrib import admin
from rango.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display=("category", "title", "url")

admin.site.register(Page, PageAdmin)
admin.site.register(Category,CategoryAdmin)
# Register your models here.
